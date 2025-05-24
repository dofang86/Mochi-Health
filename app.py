from flask import Flask, render_template, request, jsonify
from datetime import datetime
import gspread
import matplotlib  
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__, static_folder='static', template_folder='templates')

SHEET_KEY = "1KyMNYteO_OcUIIGRemAbuayVfRMVAkScZGAyrAm_zkI"
CREDENTIALS = "credentials.json"

CHART_SAVE_PATH = os.path.join(os.path.dirname(__file__), 'mood_history')
os.makedirs(CHART_SAVE_PATH, exist_ok=True)

def generate_chart(data, timestamp):
    plt.figure(figsize=(10, 6))
    moods = list(data.keys())
    counts = list(data.values())
    
    bars = plt.bar(moods, counts, color=['#4CAF50', '#4CAF50', '#4CAF50', '#4CAF50'])
    plt.ylabel('Count', fontsize=12)
    plt.title(f"Mood Distribution - {timestamp.split()[0]}", pad=20)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}',
                 ha='center', va='bottom')
    
    filename = f"mood_chart_{timestamp.replace(':', '-').replace(' ', '_')}.png"
    save_path = os.path.join(CHART_SAVE_PATH, filename)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=120, bbox_inches='tight')
    plt.close()
    print(f"Chart saved to：{save_path}")

def get_sheet():
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_KEY).sheet1

@app.route('/today_moods')
def today_moods():
    data = get_mood_data()
    return jsonify(data)

def get_mood_data():
    try:
        sheet = get_sheet()
        records = sheet.get_all_values()
        today = datetime.now().date()
        mood_counts = {'😊':0, '😠':0, '😕':0, '❤️':0}
        
        for row in records:
            try:
                record_time = datetime.strptime(row[0].strip(), "%Y-%m-%d %H:%M:%S").date()
                mood = row[1].strip()
                if record_time == today and mood in mood_counts:
                    mood_counts[mood] += 1
            except (IndexError, ValueError) as e:
                continue
        return mood_counts
    except Exception as e:
        print(f"Fail to get data: {str(e)}")
        return {}
    
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/log', methods=['POST'])
def log():
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": request.form.get('mood'),
        "note": request.form.get('note', '')
    }
    
    try:
        sheet = get_sheet()
        sheet.append_row([data['time'], data['mood'], data['note']])
        today_data = get_mood_data()
        generate_chart(today_data, data['time'])
        return "Record Successful"
    except Exception as e:
        return f"Error", 500

if __name__ == '__main__':
    app.run(port=5002)



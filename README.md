# Mochi-Health Assignment
## Overview
This web application is designed specifically for Mochi Health as a mood logging tool. 

Google Sheet: https://docs.google.com/spreadsheets/d/1KyMNYteO_OcUIIGRemAbuayVfRMVAkScZGAyrAm_zkI/edit?usp=sharing

Requirements:
```
install flask gspread matplotlib oauth2client
```

## Operating Instructions
### 1. Download Credentials.json
Download the credentials file from my submission or this link: https://drive.google.com/file/d/1gZx5YUE3kuErhROH2GW1z-She7EF630P/view?usp=drive_link

### 2. Run Locally
Download the whole zip file from Github and place the credentials.json file in the root directory as `credentials.json`. The folder structure should look like this:
```
Mochi-Health repo/ 
    ├── app.py  
    ├── README.md  
    ├── credentials.json  
    └── ...
```
Navigate to the folder in terminal and run app.py. Then open a browser and go to link http://127.0.0.1:5002
```
# Run this in terminal
pip install flask gspread matplotlib oauth2client
python app.py

# When this message shows up, go to link http://127.0.0.1:5002
* Running on http://127.0.0.1:5002
```
### 3. Log Data
Select one emoji, add notes (optional) and click 'submit'
### 4. Chart Display (HTML)
The bar chart at the bottom of the page will automatically update based on the latest data after each refresh or submission
### 5. Chart local backup (matplotlib)
After each refresh or logging , the latest bar chart will be stored in the local /mood_history folder
```
Mochi-Health repo/ 
    ├── app.py  
    └── mood_history
        └── mood_chart.png
    └── ...
```
## Tools
**1. Language**: Python

**2. UI**: Flask + HTML + CSS

**3. Storage**: Google Sheets

**4. Charting**: matplotlib

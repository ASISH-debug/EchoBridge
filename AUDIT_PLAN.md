# EchoBridge Project Audit Plan

## Issues Identified:

### 1. Manual Emotion Save Bug (HIGH PRIORITY)
- **Problem**: templete/manual.html has `proceedToMatching()` that only shows an alert, doesn't save to database
- **Fix**: Connect to `/manual-save` endpoint properly

### 2. Emotion Mismatch (HIGH PRIORITY)
- **Problem**: Manual options (stressed, anxious, calm) don't match model emotions (angry, disgust, fear, happy, neutral, sad, surprise)
- **Fix**: Update manual.html emotion options to match model

### 3. Dashboard Charts Missing (MEDIUM PRIORITY)
- **Problem**: dashboard.html shows only list, no charts
- **Fix**: Add Chart.js for emotion analytics

### 4. Duplicate auto.html (LOW PRIORITY)
- **Problem**: auto.html exists in both root and templete/
- **Fix**: Remove root auto.html (Flask uses templete/)

### 5. Deployment Settings (MEDIUM PRIORITY)
- **Problem**: debug=True, no host setting
- **Fix**: Set debug=False, host='0.0.0.0'

### 6. requirements.txt (MEDIUM PRIORITY)
- **Problem**: Missing requirements.txt
- **Fix**: Create requirements.txt

## Execution Order:
1. Fix manual.html - connect to /manual-save endpoint
2. Fix emotion options in manual.html to match model
3. Add Chart.js to dashboard.html
4. Remove duplicate auto.html from root
5. Update app.py deployment settings
6. Create requirements.txt
7. Test server startup


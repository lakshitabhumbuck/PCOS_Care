# Installation and Setup Guide

Follow these steps to set up the PCOS Prediction Application with your trained ML model.

## Prerequisites

1. **Node.js** (v14 or higher)
   - Download from: https://nodejs.org/
   - Verify installation: `node --version`

2. **Python** (3.7 or higher)
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version` (or `python3 --version` on Mac/Linux)

3. **Python Packages**
   - scikit-learn
   - pandas
   - numpy
   - joblib

## Step-by-Step Setup

### Step 1: Install Node.js Dependencies

Open terminal in the `pcos-main` directory:

```bash
npm install
```

This installs:
- Express (web server)
- CORS (for API requests)

### Step 2: Install Python Dependencies

```bash
pip install scikit-learn pandas numpy joblib
```

Or if you have both Python 2 and 3:
```bash
pip3 install scikit-learn pandas numpy joblib
```

### Step 3: Add Your Trained Model Files

1. **Download from Google Colab:**
   - In your Colab notebook, after training, run:
   ```python
   from google.colab import files
   files.download("pcos_model.pkl")
   files.download("feature_order.pkl")
   ```

2. **Create the models directory:**
   ```bash
   mkdir -p backend/ml/models
   ```

3. **Copy the downloaded files:**
   - Copy `pcos_model.pkl` to `backend/ml/models/pcos_model.pkl`
   - Copy `feature_order.pkl` to `backend/ml/models/feature_order.pkl`

### Step 4: Verify File Structure

Your project should look like:
```
pcos-main/
├── backend/
│   ├── server.js
│   └── ml/
│       ├── pcosModel.js
│       ├── predict.py
│       └── models/
│           ├── pcos_model.pkl      ← Your trained model
│           ├── feature_order.pkl  ← Feature names
│           └── README.md
├── package.json
└── ... (other files)
```

### Step 5: Start the Backend Server

```bash
npm start
```

You should see:
```
Server running on http://localhost:3000
API endpoint: http://localhost:3000/api/predict
```

### Step 6: Test the Setup

1. **Test the API directly:**
   ```bash
   curl -X POST http://localhost:3000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"age": 25, "weight": 70, "height": 165, "cycle": "Irregular", "symptoms": ["Hair Growth"], "exerciseFrequency": "Weekly", "dietType": "Normal", "sleepHours": 7}'
   ```

2. **Or open the frontend:**
   - Open `index.html` in your browser
   - Navigate to Assessment
   - Fill out the form and submit

## Troubleshooting

### "Python not found" Error

**Windows:**
- Ensure Python is installed and added to PATH
- Try using `py` instead of `python`:
  - Edit `backend/ml/pcosModel.js` line 8: change `'python'` to `'py'`

**Mac/Linux:**
- Use `python3` instead of `python`
- Edit `backend/ml/pcosModel.js` line 8: change `'python'` to `'python3'`

### "Model file not found" Error

- Verify `pcos_model.pkl` exists in `backend/ml/models/`
- Check file permissions
- Ensure file name is exactly `pcos_model.pkl` (case-sensitive)

### "Module not found" Python Error

- Install missing packages: `pip install scikit-learn pandas numpy joblib`
- Verify Python environment is correct

### Port Already in Use

- Change port in `backend/server.js`:
  ```javascript
  const PORT = process.env.PORT || 3001;  // Change 3000 to 3001
  ```
- Update API URL in `assessment.js`:
  ```javascript
  const API_URL = 'http://localhost:3001/api/predict';
  ```

## Verification Checklist

- [ ] Node.js installed and working
- [ ] Python installed and working
- [ ] Python packages installed (scikit-learn, pandas, numpy, joblib)
- [ ] Model files in `backend/ml/models/` directory
- [ ] Backend server starts without errors
- [ ] API endpoint responds to test requests
- [ ] Frontend can connect to backend

## Next Steps

Once everything is set up:
1. Test with various input combinations
2. Adjust feature mappings in `predict.py` if needed
3. Consider adding more frontend fields to collect additional clinical data
4. Deploy to production (Heroku, AWS, etc.)


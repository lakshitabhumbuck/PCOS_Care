# PCOS Prediction Application

A full-stack application for PCOS (Polycystic Ovary Syndrome) risk assessment with ML model integration.

## Project Structure

```
pcos-main/
├── backend/
│   ├── server.js          # Express server and API endpoints
│   └── ml/
│       └── pcosModel.js    # ML model integration module
├── assessment.html         # Assessment form (frontend)
├── assessment.js           # Frontend logic
├── result.html             # Results page
├── result.js               # Results display logic
├── package.json            # Node.js dependencies
└── README.md               # This file
```

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Start the Backend Server

```bash
npm start
```

Or for development with auto-reload:

```bash
npm run dev
```

The server will run on `http://localhost:3000`

### 3. Open the Frontend

Open `index.html` or `assessment.html` in your browser, or use a local server:

```bash
# Using Python
python -m http.server 8000

# Using Node.js http-server
npx http-server
```

Then navigate to `http://localhost:8000`

## API Endpoints

### POST `/api/predict`

Submit assessment data and get PCOS prediction.

**Request Body:**
```json
{
  "age": 25,
  "weight": 65,
  "height": 165,
  "cycle": "Irregular",
  "cycleDuration": 35,
  "cycleGap": 10,
  "symptoms": ["Acne", "Hair Growth", "Weight Gain"],
  "exerciseFrequency": "Weekly",
  "dietType": "Normal",
  "sleepHours": 7
}
```

**Response:**
```json
{
  "success": true,
  "score": 75,
  "riskLevel": "High",
  "probability": 0.75
}
```

### GET `/api/health`

Health check endpoint.

**Response:**
```json
{
  "status": "OK",
  "message": "PCOS Prediction API is running"
}
```

## ML Model Integration

The current implementation uses a placeholder scoring system. To integrate your actual ML model:

### Option 1: TensorFlow.js Model

1. Save your trained model in TensorFlow.js format (`.json` and `.bin` files)
2. Update `backend/ml/pcosModel.js`:

```javascript
const tf = require('@tensorflow/tfjs-node');

let model = null;

async function loadModel() {
    if (!model) {
        model = await tf.loadLayersModel('file://./backend/ml/models/pcos-model.json');
    }
    return model;
}

async function predictPCOS(assessmentData) {
    const features = extractFeatures(assessmentData);
    const normalizedFeatures = normalizeFeatures(features);
    
    const loadedModel = await loadModel();
    const input = tf.tensor2d([normalizedFeatures], [1, normalizedFeatures.length]);
    const prediction = loadedModel.predict(input);
    const probability = (await prediction.data())[0];
    
    const score = Math.round(probability * 100);
    // ... rest of the logic
}
```

### Option 2: Python Model (scikit-learn, etc.)

1. Create a Python script `backend/ml/predict.py`:

```python
import sys
import json
import pickle
import numpy as np

# Load your trained model
with open('pcos_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get features from command line
features = json.loads(sys.argv[1])
features_array = np.array([features])

# Predict
probability = model.predict_proba(features_array)[0][1]
score = int(probability * 100)

print(json.dumps({
    "score": score,
    "probability": float(probability)
}))
```

2. Update `backend/ml/pcosModel.js`:

```javascript
const { spawn } = require('child_process');
const path = require('path');

async function predictPCOS(assessmentData) {
    const features = extractFeatures(assessmentData);
    const normalizedFeatures = normalizeFeatures(features);
    
    return new Promise((resolve, reject) => {
        const python = spawn('python', [
            path.join(__dirname, 'predict.py'),
            JSON.stringify(normalizedFeatures)
        ]);
        
        let output = '';
        python.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                const result = JSON.parse(output);
                // ... process result
                resolve({
                    score: result.score,
                    probability: result.probability,
                    riskLevel: determineRiskLevel(result.score)
                });
            } else {
                reject(new Error('Python script failed'));
            }
        });
    });
}
```

### Option 3: Pre-trained Model Weights

If you have model weights in JSON format, you can load and use them directly in JavaScript.

## Features

- Multi-step assessment form
- Real-time BMI calculation
- ML-powered PCOS risk prediction
- Risk level classification (Low/Moderate/High)
- Personalized recommendations
- Modern, responsive UI

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Node.js, Express
- **ML**: Placeholder system (ready for TensorFlow.js, Python, or custom models)

## Notes

- The current ML model uses a weighted scoring system as a placeholder
- Replace the prediction logic in `backend/ml/pcosModel.js` with your actual trained model
- Ensure your model's input features match the normalized features array
- Adjust feature normalization ranges based on your training data

## Troubleshooting

**Backend not starting:**
- Check if port 3000 is available
- Ensure all dependencies are installed: `npm install`

**CORS errors:**
- Make sure the backend server is running
- Check that the API URL in `assessment.js` matches your server URL

**Prediction errors:**
- Verify all required fields are being sent from the frontend
- Check the console for detailed error messages
- Ensure your ML model is properly integrated


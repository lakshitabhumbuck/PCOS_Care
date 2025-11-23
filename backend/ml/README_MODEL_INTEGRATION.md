# ML Model Integration Guide

This guide explains how to integrate your trained PCOS prediction model into the backend.

## Current Implementation

The current `pcosModel.js` uses a placeholder weighted scoring system. You need to replace the `predictPCOS` function with your actual model inference.

## Feature Mapping

The frontend collects these inputs:
- Age, Weight, Height (BMI calculated automatically)
- Menstrual cycle regularity and details
- Symptoms (checkboxes)
- Lifestyle factors (exercise, diet, sleep)

These are converted to normalized features in the `normalizeFeatures()` function.

## Integration Steps

### Step 1: Understand Your Model's Input Format

Your model expects a specific input format. Check:
- Number of features
- Feature order
- Normalization/scaling method used during training
- Input shape (1D array, 2D array, etc.)

### Step 2: Update Feature Extraction

Modify `extractFeatures()` and `normalizeFeatures()` in `pcosModel.js` to match your model's expected input format.

### Step 3: Replace Prediction Logic

Replace the placeholder scoring in `predictPCOS()` with your model inference code.

## Example Integrations

### TensorFlow.js (SavedModel format)

```javascript
const tf = require('@tensorflow/tfjs-node');
const path = require('path');

let model = null;

async function loadModel() {
    if (!model) {
        const modelPath = path.join(__dirname, 'models', 'pcos-model.json');
        model = await tf.loadLayersModel(`file://${modelPath}`);
        console.log('Model loaded successfully');
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
    const riskLevel = score < 30 ? 'Low' : score < 60 ? 'Moderate' : 'High';
    
    return {
        score,
        probability: parseFloat(probability.toFixed(4)),
        riskLevel,
        features
    };
}
```

**Install TensorFlow.js:**
```bash
npm install @tensorflow/tfjs-node
```

### Python Model via Child Process

Create `backend/ml/predict.py`:

```python
import sys
import json
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

# Load model and scaler
with open('pcos_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Get features from stdin
features_json = sys.argv[1]
features = json.loads(features_json)
features_array = np.array([features])

# Scale features
features_scaled = scaler.transform(features_array)

# Predict
probability = model.predict_proba(features_scaled)[0][1]
score = int(probability * 100)

# Output JSON
result = {
    "score": score,
    "probability": float(probability)
}
print(json.dumps(result))
```

Update `pcosModel.js`:

```javascript
const { spawn } = require('child_process');
const path = require('path');

async function predictPCOS(assessmentData) {
    const features = extractFeatures(assessmentData);
    const normalizedFeatures = normalizeFeatures(features);
    
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, 'predict.py');
        const python = spawn('python', [pythonScript, JSON.stringify(normalizedFeatures)]);
        
        let output = '';
        let errorOutput = '';
        
        python.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        python.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });
        
        python.on('close', (code) => {
            if (code === 0) {
                try {
                    const result = JSON.parse(output.trim());
                    const riskLevel = result.score < 30 ? 'Low' : 
                                    result.score < 60 ? 'Moderate' : 'High';
                    
                    resolve({
                        score: result.score,
                        probability: result.probability,
                        riskLevel,
                        features
                    });
                } catch (e) {
                    reject(new Error('Failed to parse prediction result: ' + e.message));
                }
            } else {
                reject(new Error(`Python script failed: ${errorOutput}`));
            }
        });
    });
}
```

### REST API Model Service

If your model is deployed as a separate service:

```javascript
const axios = require('axios');

async function predictPCOS(assessmentData) {
    const features = extractFeatures(assessmentData);
    const normalizedFeatures = normalizeFeatures(features);
    
    try {
        const response = await axios.post('http://your-model-service:8000/predict', {
            features: normalizedFeatures
        });
        
        const probability = response.data.probability;
        const score = Math.round(probability * 100);
        const riskLevel = score < 30 ? 'Low' : score < 60 ? 'Moderate' : 'High';
        
        return {
            score,
            probability,
            riskLevel,
            features
        };
    } catch (error) {
        throw new Error(`Model service error: ${error.message}`);
    }
}
```

## Testing Your Integration

1. Test with sample data:
```javascript
const testData = {
    age: 25,
    weight: 70,
    height: 165,
    cycle: 'Irregular',
    cycleDuration: 35,
    cycleGap: 10,
    symptoms: ['Acne', 'Hair Growth'],
    exerciseFrequency: 'Weekly',
    dietType: 'Normal',
    sleepHours: 7
};

predictPCOS(testData).then(result => {
    console.log('Prediction:', result);
});
```

2. Verify output format matches expected response structure
3. Test edge cases (missing values, extreme values)
4. Check performance (prediction time)

## Important Notes

- **Feature Order**: Ensure features are in the same order as your training data
- **Normalization**: Use the same scaling/normalization method as training
- **Error Handling**: Add proper error handling for model loading and prediction
- **Performance**: Consider caching loaded models to avoid reloading on each request
- **Validation**: Validate input data before passing to model

## Model File Organization

Recommended structure:
```
backend/ml/
├── pcosModel.js          # Main prediction module
├── models/               # Model files directory
│   ├── pcos-model.json   # TensorFlow.js model
│   ├── pcos-model.bin    # TensorFlow.js weights
│   └── pcos_model.pkl    # Python model (if using)
├── predict.py            # Python prediction script (if using)
└── scaler.pkl            # Feature scaler (if using)
```

Add `models/` to `.gitignore` if model files are large.


# Model Files Directory

Place your trained model files here:

## Required Files

1. **pcos_model.pkl** - Your trained Gradient Boosting model (saved with joblib)
2. **feature_order.pkl** - List of feature names in the order expected by the model

## How to Add Model Files

### Step 1: Download from Google Colab

After running your training code in Colab, download the files:
```python
from google.colab import files
files.download("pcos_model.pkl")
files.download("feature_order.pkl")
```

### Step 2: Place Files in This Directory

Copy the downloaded files to:
```
pcos-main/backend/ml/models/
```

Your directory structure should look like:
```
backend/ml/models/
├── pcos_model.pkl
├── feature_order.pkl
└── README.md (this file)
```

### Step 3: Verify Python Dependencies

Make sure you have the required Python packages installed:
```bash
pip install scikit-learn pandas numpy joblib
```

### Step 4: Test the Model

The backend will automatically use these files when making predictions.

## Troubleshooting

**"Model file not found" error:**
- Ensure `pcos_model.pkl` is in `backend/ml/models/` directory
- Check file name spelling (case-sensitive)

**"Feature order file not found" error:**
- Ensure `feature_order.pkl` is in `backend/ml/models/` directory
- This file should contain the list of feature names from your training

**Python import errors:**
- Install required packages: `pip install scikit-learn pandas numpy joblib`
- Verify Python version (3.7+ recommended)


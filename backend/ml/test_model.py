"""
Test script to verify model loading and feature order
Run this to check if your model files are set up correctly
"""

import sys
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import traceback

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / 'models' / 'pcos_model.pkl'
FEATURE_ORDER_PATH = SCRIPT_DIR / 'models' / 'feature_order.pkl'

def test_model_setup():
    """Test if model files can be loaded correctly"""
    print("=" * 60)
    print("Testing PCOS Model Setup")
    print("=" * 60)
    
    # Test 1: Check if files exist
    print("\n1. Checking model files...")
    if not MODEL_PATH.exists():
        print(f"   ❌ ERROR: Model file not found at {MODEL_PATH}")
        print(f"   Please ensure pcos_model.pkl is in backend/ml/models/")
        return False
    else:
        print(f"   ✅ Model file found: {MODEL_PATH}")
    
    if not FEATURE_ORDER_PATH.exists():
        print(f"   ❌ ERROR: Feature order file not found at {FEATURE_ORDER_PATH}")
        print(f"   Please ensure feature_order.pkl is in backend/ml/models/")
        return False
    else:
        print(f"   ✅ Feature order file found: {FEATURE_ORDER_PATH}")
    
    # Test 2: Load model
    print("\n2. Loading model...")
    try:
        model = joblib.load(MODEL_PATH)
        print(f"   ✅ Model loaded successfully")
        print(f"   Model type: {type(model).__name__}")
    except Exception as e:
        print(f"   ❌ ERROR loading model:")
        traceback.print_exc()
        return False
    
    # Test 3: Load feature order
    print("\n3. Loading feature order...")
    try:
        feature_order = joblib.load(FEATURE_ORDER_PATH)
        print(f"   ✅ Feature order loaded successfully")
        print(f"   Number of features: {len(feature_order)}")
        print(f"   First 5 features: {feature_order[:5]}")
        print(f"   Last 5 features: {feature_order[-5:]}")
    except Exception as e:
        print(f"   ❌ ERROR loading feature order:")
        traceback.print_exc()
        return False
    
    # Test 4: Verify feature order matches expected
    print("\n4. Verifying feature order...")
    expected_features = [
        'Age_yrs', 'Weight_Kg', 'HeightCm', 'BMI', 'Blood_Group', 'Pulse_ratebpm',
        'RR_breathsmin', 'Hbgdl', 'CycleRI', 'Cycle_lengthdays', 'Marraige_Status_Yrs',
        'PregnantYN', 'No_of_abortions', 'I_betaHCGmIUmL', 'II_betaHCGmIUmL',
        'FSHmIUmL', 'LHmIUmL', 'FSHLH', 'Hipinch', 'Waistinch', 'WaistHip_Ratio',
        'TSH_mIUL', 'AMHngmL', 'PRLngmL', 'Vit_D3_ngmL', 'PRGngmL', 'RBSmgdl',
        'Weight_gainYN', 'hair_growthYN', 'Skin_darkening_YN', 'Hair_lossYN',
        'PimplesYN', 'Fast_food_YN', 'RegExerciseYN', 'BP_Systolic_mmHg',
        'BP_Diastolic_mmHg', 'Follicle_No_L', 'Follicle_No_R', 'Avg_F_size_L_mm',
        'Avg_F_size_R_mm', 'Endometrium_mm', 'LH_FSH_Ratio', 'Total_Follicle_Count'
    ]
    
    if len(feature_order) != len(expected_features):
        print(f"   ⚠️  WARNING: Feature count mismatch!")
        print(f"   Expected: {len(expected_features)}, Got: {len(feature_order)}")
    else:
        print(f"   ✅ Feature count matches: {len(feature_order)}")
    
    missing = set(expected_features) - set(feature_order)
    extra = set(feature_order) - set(expected_features)
    
    if missing:
        print(f"   ⚠️  Missing features: {missing}")
    if extra:
        print(f"   ⚠️  Extra features: {extra}")
    if not missing and not extra:
        print(f"   ✅ All expected features present")
    
    # Test 5: Create sample data and test prediction
    print("\n5. Testing prediction with sample data...")
    try:
        # Create sample feature dictionary
        sample_features = {
            'Age_yrs': 25, 'Weight_Kg': 70, 'HeightCm': 165, 'BMI': 25.7,
            'Blood_Group': 15, 'Pulse_ratebpm': 72, 'RR_breathsmin': 18,
            'Hbgdl': 12.0, 'CycleRI': 1, 'Cycle_lengthdays': 35,
            'Marraige_Status_Yrs': 0.0, 'PregnantYN': 0, 'No_of_abortions': 0,
            'I_betaHCGmIUmL': 1.99, 'II_betaHCGmIUmL': 1.99,
            'FSHmIUmL': 5.0, 'LHmIUmL': 10.0, 'FSHLH': 0.5,
            'Hipinch': 40, 'Waistinch': 35, 'WaistHip_Ratio': 0.875,
            'TSH_mIUL': 2.5, 'AMHngmL': 8.0, 'PRLngmL': 15.0,
            'Vit_D3_ngmL': 30.0, 'PRGngmL': 0.5, 'RBSmgdl': 90,
            'Weight_gainYN': 1, 'hair_growthYN': 1, 'Skin_darkening_YN': 0,
            'Hair_lossYN': 1, 'PimplesYN': 1, 'Fast_food_YN': 1,
            'RegExerciseYN': 0, 'BP_Systolic_mmHg': 120, 'BP_Diastolic_mmHg': 80,
            'Follicle_No_L': 15, 'Follicle_No_R': 18, 'Avg_F_size_L_mm': 6.0,
            'Avg_F_size_R_mm': 6.5, 'Endometrium_mm': 5.0,
            'LH_FSH_Ratio': 2.0, 'Total_Follicle_Count': 33
        }
        
        # Create DataFrame in correct order
        features_df = pd.DataFrame([sample_features])
        for feat in feature_order:
            if feat not in features_df.columns:
                features_df[feat] = 0
        
        features_ordered = features_df[feature_order]
        features_ordered = features_ordered.replace([np.inf, -np.inf], np.nan)
        features_ordered = features_ordered.fillna(features_ordered.max())
        
        # Make prediction
        prediction = model.predict(features_ordered)[0]
        probability = model.predict_proba(features_ordered)[0]
        
        pcos_prob = probability[1] if len(probability) > 1 else probability[0]
        score = int(pcos_prob * 100)
        
        print(f"   ✅ Prediction successful!")
        print(f"   Predicted class: {prediction} ({'PCOS' if prediction == 1 else 'No PCOS'})")
        print(f"   PCOS probability: {pcos_prob:.4f} ({score}%)")
    except Exception as e:
        print(f"   ❌ ERROR during prediction test:")
        traceback.print_exc()
        return False

    print("\n" + "=" * 60)
    print("✅ All tests passed! Model is ready to use.")
    print("=" * 60)
    return True

if __name__ == "__main__":
    success = test_model_setup()
    sys.exit(0 if success else 1)

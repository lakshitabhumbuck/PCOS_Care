"""
PCOS Prediction Script
Loads the trained Gradient Boosting model and makes predictions
"""

import sys
import json
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
MODEL_PATH = SCRIPT_DIR / 'models' / 'pcos_model.pkl'
FEATURE_ORDER_PATH = SCRIPT_DIR / 'models' / 'feature_order.pkl'

def load_model():
    """Load the trained PCOS prediction model"""
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        error = {
            "error": f"Model file not found at {MODEL_PATH}. Please ensure pcos_model.pkl is in backend/ml/models/ directory."
        }
        print(json.dumps(error))
        sys.exit(1)
    except Exception as e:
        error = {
            "error": f"Error loading model: {str(e)}"
        }
        print(json.dumps(error))
        sys.exit(1)

def load_feature_order():
    """Load the feature order used during training"""
    try:
        feature_order = joblib.load(FEATURE_ORDER_PATH)
        return feature_order
    except FileNotFoundError:
        error = {
            "error": f"Feature order file not found at {FEATURE_ORDER_PATH}. Please ensure feature_order.pkl is in backend/ml/models/ directory."
        }
        print(json.dumps(error))
        sys.exit(1)
    except Exception as e:
        error = {
            "error": f"Error loading feature order: {str(e)}"
        }
        print(json.dumps(error))
        sys.exit(1)

def create_feature_dict(frontend_data):
    """
    Map frontend assessment data to model features.
    Uses defaults for features not collected by frontend.
    
    Expected features (42 total):
    Age_yrs, Weight_Kg, HeightCm, BMI, Blood_Group, Pulse_ratebpm, RR_breathsmin,
    Hbgdl, CycleRI, Cycle_lengthdays, Marraige_Status_Yrs, PregnantYN, No_of_abortions,
    I_betaHCGmIUmL, II_betaHCGmIUmL, FSHmIUmL, LHmIUmL, FSHLH, Hipinch, Waistinch,
    WaistHip_Ratio, TSH_mIUL, AMHngmL, PRLngmL, Vit_D3_ngmL, PRGngmL, RBSmgdl,
    Weight_gainYN, hair_growthYN, Skin_darkening_YN, Hair_lossYN, PimplesYN,
    Fast_food_YN, RegExerciseYN, BP_Systolic_mmHg, BP_Diastolic_mmHg,
    Follicle_No_L, Follicle_No_R, Avg_F_size_L_mm, Avg_F_size_R_mm, Endometrium_mm,
    LH_FSH_Ratio (derived), Total_Follicle_Count (derived)
    """
    # Calculate BMI
    height_cm = float(frontend_data.get('height', 165))
    weight_kg = float(frontend_data.get('weight', 60))
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    
    # Map cycle regularity
    cycle_ri = 2 if frontend_data.get('cycle') == 'Regular' else 1  # 1=Irregular, 2=Regular
    
    # Map symptoms
    symptoms = frontend_data.get('symptoms', [])
    weight_gain_yn = 1 if 'Weight Gain' in symptoms else 0
    hair_growth_yn = 1 if 'Hair Growth' in symptoms else 0
    hair_loss_yn = 1 if 'Hair Loss' in symptoms else 0
    pimples_yn = 1 if 'Acne' in symptoms else 0
    
    # Map exercise frequency
    exercise_freq = frontend_data.get('exerciseFrequency', 'None').lower()
    reg_exercise_yn = 1 if 'daily' in exercise_freq or 'weekly' in exercise_freq else 0
    
    # Map diet type
    diet_type = frontend_data.get('dietType', 'Normal').lower()
    fast_food_yn = 1 if 'fast' in diet_type or 'junk' in diet_type else 0
    
    # Create feature dictionary with defaults for missing clinical data
    # NOTE: Many features require lab tests/clinical measurements not in frontend
    # Using reasonable defaults based on typical values
    features = {
        'Age_yrs': float(frontend_data.get('age', 25)),
        'Weight_Kg': weight_kg,
        'HeightCm': height_cm,
        'BMI': bmi,
        'Blood_Group': 15,  # Default (not collected)
        'Pulse_ratebpm': 72,  # Default normal range
        'RR_breathsmin': 18,  # Default normal range
        'Hbgdl': 12.0,  # Default normal hemoglobin
        'CycleRI': cycle_ri,
        'Cycle_lengthdays': float(frontend_data.get('cycleDuration', 28)),
        'Marraige_Status_Yrs': 0.0,  # Default (not collected)
        'PregnantYN': 0,  # Default (not collected)
        'No_of_abortions': 0,  # Default (not collected)
        'I_betaHCGmIUmL': 1.99,  # Default (lab test)
        'II_betaHCGmIUmL': 1.99,  # Default (lab test)
        'FSHmIUmL': 5.0,  # Default normal FSH
        'LHmIUmL': 5.0,  # Default normal LH
        'FSHLH': 1.0,  # Default ratio
        'Hipinch': round(bmi * 1.5 + 30),  # Estimate from BMI
        'Waistinch': round(bmi * 1.2 + 25),  # Estimate from BMI
        'WaistHip_Ratio': 0.85,  # Default (will be recalculated)
        'TSH_mIUL': 2.5,  # Default normal TSH
        'AMHngmL': 3.0,  # Default (lab test - important for PCOS)
        'PRLngmL': 15.0,  # Default normal prolactin
        'Vit_D3_ngmL': 30.0,  # Default normal vitamin D
        'PRGngmL': 0.5,  # Default normal progesterone
        'RBSmgdl': 90,  # Default normal blood sugar
        'Weight_gainYN': weight_gain_yn,
        'hair_growthYN': hair_growth_yn,
        'Skin_darkening_YN': 0,  # Default (not collected in frontend)
        'Hair_lossYN': hair_loss_yn,
        'PimplesYN': pimples_yn,
        'Fast_food_YN': fast_food_yn,
        'RegExerciseYN': reg_exercise_yn,
        'BP_Systolic_mmHg': 120,  # Default normal
        'BP_Diastolic_mmHg': 80,  # Default normal
        'Follicle_No_L': 8,  # Default (ultrasound - important for PCOS)
        'Follicle_No_R': 8,  # Default (ultrasound - important for PCOS)
        'Avg_F_size_L_mm': 5.0,  # Default follicle size
        'Avg_F_size_R_mm': 5.0,  # Default follicle size
        'Endometrium_mm': 5.0  # Default endometrium thickness
    }
    
    # Recalculate WaistHip_Ratio
    features['WaistHip_Ratio'] = features['Waistinch'] / features['Hipinch'] if features['Hipinch'] > 0 else 0.85
    
    # Feature Engineering: Derived features
    features['LH_FSH_Ratio'] = features['LHmIUmL'] / features['FSHmIUmL'] if features['FSHmIUmL'] > 0 else 1.0
    features['Total_Follicle_Count'] = features['Follicle_No_L'] + features['Follicle_No_R']
    
    return features

def predict(frontend_data):
    """
    Main prediction function
    """
    try:
        # Load model and feature order
        model = load_model()
        feature_order = load_feature_order()
        
        # Create feature dictionary from frontend data
        features_dict = create_feature_dict(frontend_data)
        
        # Create DataFrame with features in correct order
        features_df = pd.DataFrame([features_dict])
        
        # Ensure all required features are present
        missing_features = set(feature_order) - set(features_df.columns)
        if missing_features:
            # Add missing features with default values
            for feat in missing_features:
                features_df[feat] = 0
        
        # Reorder columns to match training data
        features_ordered = features_df[feature_order]
        
        # Handle infinite values (from division operations)
        features_ordered = features_ordered.replace([np.inf, -np.inf], np.nan)
        # Fill NaN with column max (matching training preprocessing)
        features_ordered = features_ordered.fillna(features_ordered.max())
        
        # Make prediction
        prediction = model.predict(features_ordered)[0]
        probability = model.predict_proba(features_ordered)[0]
        
        # Get PCOS probability (class 1)
        pcos_probability = probability[1] if len(probability) > 1 else probability[0]
        score = int(pcos_probability * 100)
        
        # Determine risk level
        if score < 30:
            risk_level = 'Low'
        elif score < 60:
            risk_level = 'Moderate'
        else:
            risk_level = 'High'
        
        result = {
            "success": True,
            "score": score,
            "probability": round(float(pcos_probability), 4),
            "riskLevel": risk_level,
            "prediction": int(prediction)
        }
        
        return result
        
    except Exception as e:
        error = {
            "error": f"Prediction error: {str(e)}",
            "type": type(e).__name__
        }
        print(json.dumps(error))
        sys.exit(1)

def main():
    """Main function to handle command-line input"""
    if len(sys.argv) < 2:
        error = {
            "error": "Missing assessment data argument",
            "usage": "python predict.py '{\"age\": 25, \"weight\": 70, ...}'"
        }
        print(json.dumps(error))
        sys.exit(1)
    
    try:
        # Parse frontend data from command line
        frontend_data_json = sys.argv[1]
        frontend_data = json.loads(frontend_data_json)
        
        # Make prediction
        result = predict(frontend_data)
        
        # Output result as JSON
        print(json.dumps(result))
        
    except json.JSONDecodeError as e:
        error = {
            "error": f"Invalid JSON format: {str(e)}"
        }
        print(json.dumps(error))
        sys.exit(1)
    except Exception as e:
        error = {
            "error": f"Unexpected error: {str(e)}",
            "type": type(e).__name__
        }
        print(json.dumps(error))
        sys.exit(1)

if __name__ == "__main__":
    main()



# Quick Setup Guide

## Step 1: Install Dependencies

Open terminal in the `pcos-main` directory and run:

```bash
npm install
```

This will install:
- Express (web server)
- CORS (for cross-origin requests)
- Nodemon (for development, optional)

## Step 2: Start the Backend Server

```bash
npm start
```

You should see:
```
Server running on http://localhost:3000
API endpoint: http://localhost:3000/api/predict
```

## Step 3: Open the Frontend

### Option A: Direct File Opening
Simply open `index.html` in your web browser.

### Option B: Local Server (Recommended)
Use a local server to avoid CORS issues:

**Python:**
```bash
python -m http.server 8000
```

**Node.js:**
```bash
npx http-server
```

Then navigate to `http://localhost:8000`

## Step 4: Test the Application

1. Open the assessment page
2. Fill out all the steps
3. Click Submit
4. You should be redirected to the results page with a prediction score

## Integrating Your ML Model

The current implementation uses a placeholder scoring system. To use your actual ML model:

1. **If using TensorFlow.js:**
   - Save your model in TensorFlow.js format
   - Update `backend/ml/pcosModel.js` following the TensorFlow.js example in `backend/ml/README_MODEL_INTEGRATION.md`

2. **If using Python model:**
   - Copy `backend/ml/predict.py.example` to `backend/ml/predict.py`
   - Update it with your model loading and prediction code
   - The Node.js backend will automatically call this script

3. **If using a REST API:**
   - Update the `predictPCOS` function in `backend/ml/pcosModel.js` to call your API

See `backend/ml/README_MODEL_INTEGRATION.md` for detailed integration instructions.

## Troubleshooting

**"Cannot connect to backend" error:**
- Make sure the backend server is running (`npm start`)
- Check that port 3000 is not in use by another application

**CORS errors:**
- Use a local server (Option B in Step 3) instead of opening files directly
- The backend already has CORS enabled

**Port already in use:**
- Change the port in `backend/server.js`: `const PORT = process.env.PORT || 3001;`
- Update the API URL in `assessment.js` to match

## Project Structure

```
pcos-main/
├── backend/
│   ├── server.js              # Main server file
│   └── ml/
│       ├── pcosModel.js       # ML model integration
│       ├── predict.py.example # Python model template
│       └── README_MODEL_INTEGRATION.md
├── assessment.html            # Assessment form
├── assessment.js              # Frontend logic (updated)
├── result.html                # Results page
├── package.json               # Dependencies
└── README.md                  # Full documentation
```

## Next Steps

1. Replace the placeholder ML model with your trained model
2. Test with various input combinations
3. Adjust feature normalization if needed
4. Deploy to production (consider using environment variables for configuration)


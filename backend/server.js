const express = require('express');
const cors = require('cors');
const path = require('path');
const { predictPCOS } = require('./ml/pcosModel');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the parent directory (frontend)
app.use(express.static(path.join(__dirname, '..')));

// API Routes
app.post('/api/predict', async (req, res) => {
    try {
        const assessmentData = req.body;
        
        // Validate required fields
        if (!assessmentData.age || !assessmentData.weight || !assessmentData.height) {
            return res.status(400).json({ 
                error: 'Missing required fields: age, weight, height' 
            });
        }

        // Process the data and get prediction
        const prediction = await predictPCOS(assessmentData);
        
        res.json({
            success: true,
            score: prediction.score,
            riskLevel: prediction.riskLevel,
            probability: prediction.probability
        });
    } catch (error) {
        console.error('Prediction error:', error);
        res.status(500).json({ 
            error: 'Failed to process prediction',
            message: error.message 
        });
    }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
    res.json({ status: 'OK', message: 'PCOS Prediction API is running' });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
    console.log(`API endpoint: http://localhost:${PORT}/api/predict`);
});


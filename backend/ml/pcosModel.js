/**
 * PCOS Prediction Model
 * 
 * This module handles PCOS prediction using the trained Gradient Boosting model.
 * The model is called via Python script (predict.py) which loads the trained model.
 */

const { spawn } = require('child_process');
const path = require('path');

/**
 * PCOS Prediction Function
 * 
 * Calls the Python prediction script with the trained Gradient Boosting model
 */
async function predictPCOS(assessmentData) {
    return new Promise((resolve, reject) => {
        const pythonScript = path.join(__dirname, 'predict.py');
        const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
        
        // Convert assessment data to JSON string
        const dataJson = JSON.stringify(assessmentData);
        
        // Spawn Python process
        const python = spawn(pythonCommand, [pythonScript, dataJson]);
        
        let output = '';
        let errorOutput = '';
        
        // Collect stdout data
        python.stdout.on('data', (data) => {
            output += data.toString();
        });
        
        // Collect stderr data
        python.stderr.on('data', (data) => {
            errorOutput += data.toString();
        });
        
        // Handle process completion
        python.on('close', (code) => {
            if (code === 0) {
                try {
                    // Parse JSON output from Python script
                    const result = JSON.parse(output.trim());
                    
                    if (result.error) {
                        reject(new Error(result.error));
                        return;
                    }
                    
                    // Return prediction result
                    resolve({
                        score: result.score,
                        probability: result.probability,
                        riskLevel: result.riskLevel
                    });
                } catch (parseError) {
                    reject(new Error(`Failed to parse prediction result: ${parseError.message}\nOutput: ${output}\nError: ${errorOutput}`));
                }
            } else {
                // Python script failed
                const errorMsg = errorOutput || output || 'Unknown error';
                reject(new Error(`Python prediction script failed (code ${code}): ${errorMsg}`));
            }
        });
        
        // Handle spawn errors
        python.on('error', (error) => {
            if (error.code === 'ENOENT') {
                reject(new Error(`Python not found. Please ensure Python is installed and in your PATH. Tried: ${pythonCommand}`));
            } else {
                reject(new Error(`Failed to spawn Python process: ${error.message}`));
            }
        });
    });
}

module.exports = {
    predictPCOS
};


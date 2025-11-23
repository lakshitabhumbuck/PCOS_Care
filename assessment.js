/* ======================
   STEP LOGIC
======================= */

let currentStep = 1;
const totalSteps = 5;

const steps = document.querySelectorAll(".step");
const progressBar = document.getElementById("progressBar");
const progressText = document.getElementById("progressText");

function showStep(step) {
    steps.forEach(s => s.classList.remove("active"));
    document.getElementById(`step${step}`).classList.add("active");

    progressBar.style.width = ((step - 1) / (totalSteps - 1)) * 100 + "%";
    progressText.innerText = `Step ${step} of ${totalSteps}`;
}

document.querySelectorAll(".next-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        if (currentStep < totalSteps) currentStep++;
        showStep(currentStep);
    });
});

document.querySelectorAll(".prev-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        if (currentStep > 1) currentStep--;
        showStep(currentStep);
    });
});

showStep(1);


/* ======================
   BMI CALCULATION
======================= */

const weightInput = document.getElementById("weight");
const heightInput = document.getElementById("height");
const bmiValue = document.getElementById("bmiValue");

function calculateBMI() {
    let w = parseFloat(weightInput.value);
    let h = parseFloat(heightInput.value) / 100;

    if (w > 0 && h > 0) {
        let bmi = (w / (h * h)).toFixed(1);
        bmiValue.textContent = bmi;
    }
}

weightInput.addEventListener("input", calculateBMI);
heightInput.addEventListener("input", calculateBMI);


/* ======================
   MENSTRUAL EXTRA FIELDS
======================= */

const extraFields = document.getElementById("extraFields");

document.querySelectorAll("input[name='cycle']").forEach(radio => {
    radio.addEventListener("change", () => {
        if (radio.value === "Irregular") {
            extraFields.classList.remove("hidden");
        } else {
            extraFields.classList.add("hidden");
        }
    });
});


/* ======================
   FILE UPLOAD PREVIEW
======================= */

const uploadBox = document.getElementById("uploadBox");
const uploadInput = document.getElementById("uploadInput");
const previewImg = document.getElementById("previewImg");

uploadBox.addEventListener("click", () => uploadInput.click());

uploadInput.addEventListener("change", () => {
    const file = uploadInput.files[0];
    if (file) {
        previewImg.src = URL.createObjectURL(file);
        previewImg.classList.remove("hidden");
    }
});


/* ======================
   SUBMIT BUTTON
======================= */

document.querySelector(".submit-btn").addEventListener("click", async () => {
    // Collect all form data
    const assessmentData = {
        age: document.getElementById("age").value,
        weight: document.getElementById("weight").value,
        height: document.getElementById("height").value,
        cycle: document.querySelector("input[name='cycle']:checked")?.value || "Regular",
        cycleDuration: document.getElementById("cycleDuration")?.value || 28,
        cycleGap: document.getElementById("cycleGap")?.value || 0,
        symptoms: Array.from(document.querySelectorAll(".symptom-checkbox:checked"))
            .map(cb => cb.value),
        exerciseFrequency: document.getElementById("exerciseFrequency").value,
        dietType: document.getElementById("dietType").value,
        sleepHours: document.getElementById("sleepHours").value
    };

    // Validate required fields
    if (!assessmentData.age || !assessmentData.weight || !assessmentData.height) {
        alert("Please fill in all required fields in Step 1.");
        showStep(1);
        return;
    }

    if (!document.querySelector("input[name='cycle']:checked")) {
        alert("Please select your cycle regularity in Step 2.");
        showStep(2);
        return;
    }

    if (!assessmentData.exerciseFrequency || !assessmentData.dietType || !assessmentData.sleepHours) {
        alert("Please fill in all lifestyle details in Step 4.");
        showStep(4);
        return;
    }

    // Show loading state
    const submitBtn = document.querySelector(".submit-btn");
    const originalText = submitBtn.textContent;
    submitBtn.textContent = "Processing...";
    submitBtn.disabled = true;

    try {
        // Send data to backend API
        const API_URL = 'http://localhost:3000/api/predict';
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(assessmentData)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        if (result.success) {
            // Store result in localStorage
            localStorage.setItem("pcosScore", result.score);
            localStorage.setItem("riskLevel", result.riskLevel);
            localStorage.setItem("probability", result.probability);

            // Redirect to result page
            window.location.href = "result.html";
        } else {
            throw new Error(result.error || "Prediction failed");
        }
    } catch (error) {
        console.error("Error submitting assessment:", error);
        alert(`Error: ${error.message}\n\nPlease make sure the backend server is running on port 3000.`);
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
    }
});

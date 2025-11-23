document.addEventListener("DOMContentLoaded", () => {
    const score = localStorage.getItem("pcosScore") || 0;

    animateScore(score);
    updateRisk(score);
    fillSummary(score);
    fillRecommendations(score);
});

/* Score Animation */
function animateScore(finalScore) {
    const circle = document.getElementById("scoreCircle");
    let count = 0;

    const interval = setInterval(() => {
        circle.innerHTML = count + "%";
        if (count == finalScore) {
            circle.classList.add("pop");
            clearInterval(interval);
        }
        count++;
    }, 20);
}

/* Risk Level Badge */
function updateRisk(score) {
    const risk = document.getElementById("riskLevel");

    if (score < 30) {
        risk.innerHTML = "Low Risk";
        risk.style.background = "#4CAF50";
    } 
    else if (score < 60) {
        risk.innerHTML = "Moderate Risk";
        risk.style.background = "#FFC107";
        risk.style.color = "#000";
    } 
    else {
        risk.innerHTML = "High Risk";
        risk.style.background = "#E53935";
    }
}

/* Summary text */
function fillSummary(score) {
    const summary = document.getElementById("summaryText");

    if (score < 30) {
        summary.innerHTML =
            "Your symptoms and lifestyle patterns show minimal indicators of PCOS. Keep maintaining a balanced routine!";
    } 
    else if (score < 60) {
        summary.innerHTML =
            "Some symptoms indicate mild-to-moderate chances of PCOS. Consider observing your cycles and maintaining a healthy routine.";
    } 
    else {
        summary.innerHTML =
            "Your symptoms strongly align with common PCOS indicators. A clinical consultation and ultrasound test is recommended.";
    }
}

/* Recommendations List */
function fillRecommendations(score) {
    const list = document.getElementById("recoList");
    list.innerHTML = "";

    let tips = [];

    if (score < 30) {
        tips = [
            "Maintain a healthy diet rich in fruits and vegetables.",
            "Continue light exercise like walking or yoga.",
            "Track your menstrual cycle regularly."
        ];
    } 
    else if (score < 60) {
        tips = [
            "Increase physical activity to 30–45 mins daily.",
            "Reduce sugar & processed food consumption.",
            "Practice stress reduction (meditation, journaling).",
            "Track cycle changes closely."
        ];
    } 
    else {
        tips = [
            "Consult a gynecologist for a detailed checkup.",
            "Consider taking an ultrasound & hormone test.",
            "Follow a structured workout routine.",
            "Limit sugar, oily foods, and refined carbs.",
            "Improve sleep quality (7–8 hrs)."
        ];
    }

    tips.forEach(t => {
        const li = document.createElement("li");
        li.innerText = t;
        list.appendChild(li);
    });
}

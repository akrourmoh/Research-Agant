const API_URL = window.location.origin + "/research";

async function submitQuestion() {
    const question = document.getElementById("question-input").value.trim();

    if (!question) {
        showError("Please enter a question.");
        return;
    }

    resetUI();
    showAgentStatus();
    disableButton(true);

    // simulate agent steps visually
    await setAgentRunning("planner");
    await delay(1500);
    await setAgentDone("planner");

    await setAgentRunning("searcher");
    await delay(1500);
    await setAgentDone("searcher");

    await setAgentRunning("writer");

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            const message = errorData.detail || "Server error: " + response.status;
            throw new Error(message);
        }

        const data = await response.json();

        await setAgentDone("writer");
        await setAgentRunning("critic");
        await delay(800);
        await setAgentDone("critic");

        showResult(data);

    } catch (error) {
        showError("Something went wrong: " + error.message);
    } finally {
        disableButton(false);
    }
}

function resetUI() {
    document.getElementById("result-box").style.display = "none";
    document.getElementById("error-box").style.display = "none";
    document.getElementById("agents-status").style.display = "none";

    ["planner", "searcher", "writer", "critic"].forEach(agent => {
        const statusEl = document.getElementById("status-" + agent);
        const stepEl = document.getElementById("step-" + agent);
        statusEl.textContent = "waiting";
        statusEl.className = "step-status";
        stepEl.className = "agent-step";
    });
}

function showAgentStatus() {
    document.getElementById("agents-status").style.display = "flex";
}

async function setAgentRunning(agent) {
    const statusEl = document.getElementById("status-" + agent);
    const stepEl = document.getElementById("step-" + agent);
    statusEl.textContent = "running";
    statusEl.className = "step-status running";
    stepEl.className = "agent-step active";
}

async function setAgentDone(agent) {
    const statusEl = document.getElementById("status-" + agent);
    const stepEl = document.getElementById("step-" + agent);
    statusEl.textContent = "done ✓";
    statusEl.className = "step-status done";
    stepEl.className = "agent-step done";
}

function showResult(data) {
    const resultBox = document.getElementById("result-box");
    document.getElementById("result-question").textContent = "Q: " + data.question;
    document.getElementById("result-answer").textContent = data.answer;
    document.getElementById("revisions-badge").textContent =
        data.revisions === 0 ? "Passed on first try" : `${data.revisions} revision(s)`;
    resultBox.style.display = "block";
}

function showError(message) {
    const errorBox = document.getElementById("error-box");
    document.getElementById("error-message").textContent = message;
    errorBox.style.display = "block";
}

function disableButton(disabled) {
    document.getElementById("submit-btn").disabled = disabled;
}

function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// allow submit with Ctrl+Enter
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("question-input").addEventListener("keydown", (e) => {
        if (e.key === "Enter" && e.ctrlKey) {
            submitQuestion();
        }
    });
});

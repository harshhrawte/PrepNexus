async function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    const chatWindow = document.getElementById("chatWindow");

    // Display user's message
    const userMsg = document.createElement("p");
    userMsg.className = "user-message";
    userMsg.textContent = message;
    chatWindow.appendChild(userMsg);

    // Clear input field and scroll down
    input.value = "";
    chatWindow.scrollTop = chatWindow.scrollHeight;

    // Send message to backend
    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ role: message })
        });

        const data = await response.json();

        // Display bot response
        const botMsg = document.createElement("p");
        botMsg.className = "bot-message";
        botMsg.innerHTML = `<strong>PrepNexus AI 🤖:</strong><br>${data.response.replace(/\n/g, "<br>")}`;
        chatWindow.appendChild(botMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;

    } catch (error) {
        const errorMsg = document.createElement("p");
        errorMsg.className = "bot-message error";
        errorMsg.textContent = "⚠️ PrepNexus AI couldn't connect. Please try again later.";
        chatWindow.appendChild(errorMsg);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
}

// Optional: Press "Enter" to send message
document.getElementById("userInput").addEventListener("keypress", function(e) {
    if (e.key === "Enter") sendMessage();
});
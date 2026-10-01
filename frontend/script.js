async function sendMessage() {
    const input = document.getElementById("messageInput");
    const message = input.value.trim();

    if (!message) return;

    addMessage(message, "user-message");
    input.value = "";

    document.getElementById("loading").style.display = "block";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        addMessage(data.reply, "bot-message");

    } catch (error) {
        addMessage(
            "மன்னிக்கவும். தற்போது சேவையை அணுக முடியவில்லை. தயவுசெய்து மீண்டும் முயற்சிக்கவும்.",
            "bot-message"
        );
    }

    document.getElementById("loading").style.display = "none";
}


function addMessage(text, className) {
    const chatBox = document.getElementById("chatBox");

    const messageDiv = document.createElement("div");
    messageDiv.className = className;
    messageDiv.innerText = text;

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}


function askQuestion(question) {
    document.getElementById("messageInput").value = question;
    sendMessage();
}


function startVoice() {
    if (!("webkitSpeechRecognition" in window)) {
        alert("மன்னிக்கவும். உங்கள் உலாவியில் குரல் மூலம் கேட்கும் வசதி இல்லை.");
        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "ta-IN";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = function(event) {
        const text = event.results[0][0].transcript;

        document.getElementById("messageInput").value = text;
        sendMessage();
    };
}

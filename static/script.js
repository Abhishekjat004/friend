// static/script.js
 // document.addEventListener("DOMContentLoaded", function () {
 //        const audio = document.querySelector("audio");

 //        // Wait for a click before playing (fix for autoplay restrictions)
 //        document.body.addEventListener("click", () => {
 //            audio.play().catch(e => {
 //                console.warn("Autoplay blocked. User interaction required.");
 //            });
 //        }, { once: true }); // run only once
 //    });
document.addEventListener("DOMContentLoaded", () => {
    const chatWindow = document.getElementById("chat-window");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    // This array will store the entire conversation history
    let chatHistory = [];

    // Function to add a message to the chat window
    const addMessage = (sender, text) => {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        messageDiv.innerText = text;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Auto-scroll to the bottom
    };

    // Function to handle sending a message
    const sendMessage = async () => {
        const messageText = userInput.value.trim();
        if (messageText === "") return;

        // Display user's message immediately
        addMessage("user", messageText);
        userInput.value = "";

        // Show a "thinking..." message
        const thinkingDiv = document.createElement("div");
        thinkingDiv.classList.add("message", "thinking-message");
        thinkingDiv.innerText = "Raju is thinking...";
        chatWindow.appendChild(thinkingDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;

        try {
            // Send message and history to the backend
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: messageText,
                    history: chatHistory // Send the current history
                }),
            });

            // Remove the "thinking..." message
            chatWindow.removeChild(thinkingDiv);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();

            // Display bot's reply
            addMessage("bot", data.reply);

            // Update the history with the new conversation turn
            chatHistory = data.history;

        } catch (error) {
            console.error("Error:", error);
            addMessage("bot", "Sorry, something went wrong. Please try again.");
        }
    };

    // Event listeners
    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            sendMessage();
        }
    });

    // Initial bot message
    addMessage("bot", "Ha bhai bol kya jana hai? tera bhai ready hai puri jankari ke sath ☺️");
});

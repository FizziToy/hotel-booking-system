const chatButton = document.getElementById('chat-button');
const chatWindow = document.getElementById('chat-window');
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatButton.addEventListener('click', () => {
    if (chatWindow.style.display === 'flex') {
        chatWindow.style.display = 'none';
    }
    else {
        chatWindow.style.display = 'flex';
    }
});

function addMessage(text, className) {
    const message = document.createElement('div');

    message.classList.add(className);
    message.textContent = text;

    chatMessages.appendChild(message);

    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const message = chatInput.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, 'user-message');

    chatInput.value = '';

    addMessage('AI думає...', 'ai-message');

    try {
        const response = await fetch('/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        const thinkingMessage = chatMessages.lastChild;
        thinkingMessage.textContent = data.answer;
    }
    catch (error) {
        const thinkingMessage = chatMessages.lastChild;
        thinkingMessage.textContent = 'Помилка з’єднання з AI.';
    }
});
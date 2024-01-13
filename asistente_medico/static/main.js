const messagesList = document.querySelector('.messages-list');
const messageForm = document.querySelector('.message-form');
const messageInput = document.querySelector('.message-input');
messageForm.addEventListener('submit', (event) => {
event.preventDefault();
const message = messageInput.value.trim();
if (message.length === 0) {
    return;
}
const messageItem = document.createElement('div');
messageItem.classList.add('message', 'sent');
messageItem.innerHTML = `
    <div class="message-text">
        <div>
          <b>Tu</b>
        </div>
        <div class="message-content">
            ${message}
        </div>
    </div>`;
messagesList.appendChild(messageItem);
messageInput.value = '';
fetch('', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
    'csrfmiddlewaretoken': document.querySelector('[name=csrfmiddlewaretoken]').value,
    'message': message
    })
})

    .then(response => response.json())
    .then(data => {
    const response = data.response;
    const messageItem = document.createElement('div');
    messageItem.classList.add('message', 'response');
    messageItem.innerHTML = `
    <div class="message-text">
        <div>
          <b>Chat Bot</b>
        </div>
        <div class="message-content">
            ${response}
        </div>
    </div>
        `;
    messagesList.appendChild(messageItem);
    });
});
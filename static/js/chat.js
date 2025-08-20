const socket = io();

// Send message on button click
document.getElementById('sendButton').addEventListener('click', function() {
    const yourMessage = document.getElementById('messageInput').value;
    if (yourMessage.trim()) {
        socket.emit('message', { 'message': yourMessage });
        document.getElementById('messageInput').value = '';
    }
});
// Send message on pressing Enter key
document.getElementById('messageInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && e.target.value.trim()) {
        const yourMessage = e.target.value;
        socket.emit('message', { 'message': yourMessage });
        e.target.value = '';
    }
});
// Display messages received from the server
socket.on('message', function(data) {
    const messageDisplay = document.getElementById('messages');
    const newMessage = document.createElement('li');
    newMessage.innerHTML = data.message;
    messageDisplay.appendChild(newMessage);
    // Auto-scroll to the bottom
    messageDisplay.scrollTop = messageDisplay.scrollHeight;
});
// Side bar toggle
function openNav() {
    document.getElementById("mySidenav").style.width = "250px";
    document.body.style.backgroundColor = "rgba(0,0,0,0.6)";
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    document.body.style.backgroundColor = "white";
}
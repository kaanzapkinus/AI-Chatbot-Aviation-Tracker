// Flight Search History
const flightForm = document.getElementById('flightForm');
const flightInput = document.getElementById('flight');

function loadSearchHistory() {
    let searches = JSON.parse(localStorage.getItem("flightSearches")) || [];
    const searchHistoryList = document.getElementById("searchHistory");
    
    searchHistoryList.innerHTML = "";
    searches.forEach(flight => {
        let li = document.createElement("li");
        li.innerHTML = `<a href='/search/?flight=${flight}' class="search-link">${flight}</a>`;
        searchHistoryList.appendChild(li);
    });
}

flightForm.addEventListener('submit', function(event) {
    if (flightInput.value.trim() === '') {
        event.preventDefault();
        return;
    }
    
    const flightID = flightInput.value.trim().toUpperCase();
    let searches = JSON.parse(localStorage.getItem("flightSearches")) || [];
    
    if (!searches.includes(flightID)) {
        searches.unshift(flightID);
        if (searches.length > 5) searches.pop();
        localStorage.setItem("flightSearches", JSON.stringify(searches));
        loadSearchHistory();
    }
});

// Chatbot Functionality
document.addEventListener('DOMContentLoaded', () => {
    // Chat Toggle
    const chatToggle = document.querySelector('.chat-toggle');
    const chatContainer = document.querySelector('.chat-container');
    const closeBtn = document.querySelector('.close-btn');

    chatToggle?.addEventListener('click', () => {
        chatContainer?.classList.toggle('active');
    });

    closeBtn?.addEventListener('click', () => {
        chatContainer?.classList.remove('active');
    });

    // Message Handling
    const sendBtn = document.querySelector('.send-btn');
    const chatInput = document.querySelector('.chat-input input');
    const chatBody = document.querySelector('.chat-body');

    let currentFlight = '';

    // Capture flight number from search
    document.querySelector('.search-input')?.addEventListener('change', (e) => {
        currentFlight = e.target.value.trim().toUpperCase();
    });

    async function sendMessage() {
        const message = chatInput.value.trim();
        if(message && currentFlight) {
            // Show user message
            const userDiv = document.createElement('div');
            userDiv.className = 'message user-message';
            userDiv.textContent = message;
            chatBody.appendChild(userDiv);

            // Show loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'message bot-message loading';
            loadingDiv.innerHTML = '<div class="loader"></div>';
            chatBody.appendChild(loadingDiv);
            chatBody.scrollTop = chatBody.scrollHeight;

            try {
                // Send to Django backend
                const response = await fetch('/chat/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    body: JSON.stringify({
                        callsign: currentFlight,
                        message: message
                    })
                });

                const data = await response.json();
                
                // Remove loading
                chatBody.removeChild(loadingDiv);

                // Show bot response
                const botDiv = document.createElement('div');
                botDiv.className = 'message bot-message';
                botDiv.textContent = data.response || "Couldn't get response";
                chatBody.appendChild(botDiv);

            } catch (error) {
                chatBody.removeChild(loadingDiv);
                const errorDiv = document.createElement('div');
                errorDiv.className = 'message bot-message error';
                errorDiv.textContent = "Connection error. Please try again.";
                chatBody.appendChild(errorDiv);
            }

            chatInput.value = '';
            chatBody.scrollTop = chatBody.scrollHeight;
        }
    }

    sendBtn?.addEventListener('click', sendMessage);
    chatInput?.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') sendMessage();
    });

    // CSRF Token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Initial load
document.addEventListener("DOMContentLoaded", () => {
    loadSearchHistory();
});
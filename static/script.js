const flightForm = document.getElementById('flightForm');
const flightInput = document.getElementById('flight');

// Geçmiş aramaları yükle
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

// Form gönderim işlemi
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

// Sayfa yüklendiğinde geçmişi göster
document.addEventListener("DOMContentLoaded", () => {
    loadSearchHistory();
    
    // (İsteğe bağlı) Tekrar aynı container eklemeyi önlemek için istersek burayı kaldırabiliriz.
    // Burada ekstra history-container eklemeye gerek yoksa yoruma alınabilir:
    /*
    const historyContainer = document.createElement("div");
    historyContainer.className = "history-container";
    historyContainer.innerHTML = `
        <h4>Recent Searches</h4>
        <ul id="searchHistory"></ul>
    `;
    document.querySelector(".container").appendChild(historyContainer);
    */
});

// static/script.js
document.addEventListener('DOMContentLoaded', () => {
  // Chat Toggle
  const chatToggle = document.querySelector('.chat-toggle');
  const chatContainer = document.querySelector('.chat-container');

  chatToggle?.addEventListener('click', () => {
    chatContainer?.classList.toggle('active');
  });

  // Progress Bar Animasyon
  document.querySelectorAll('progress').forEach(progress => {
    const value = parseInt(progress.value);
    progress.style.setProperty('--progress-value', `${value}%`);
  });
});

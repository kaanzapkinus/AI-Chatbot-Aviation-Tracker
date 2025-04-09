# Final Project Report: AI-Chatbot-Aviation-Tracker

**Submission Date:** April 9, 2024  
**Submitted by:** Kaan Yazıcıoğlu (97364) (SD4), Caner Akcasu (97334) (SD1)

---

## 0. Requirements & How to Run

GitHub Repository: [https://github.com/kaanzapkinus/AI-Chatbot-Aviation-Tracker](https://github.com/kaanzapkinus/AI-Chatbot-Aviation-Tracker)

To run the project locally:

1. Install **Python 3.10** or above on your system.  
2. Open a terminal in the project directory.  
3. Install dependencies with:  
   **pip install -r requirements.txt**  
4. Apply database migrations:  
   **python manage.py migrate**  
5. Start the Django development server:  
   **python manage.py runserver**  
6. Open your browser and navigate to:  
   **http://127.0.0.1:8000/**

---

## 1. Introduction

The AI Chatbot Aviation Tracker is an improved version of our Django-based flight tracking system. The original project offered basic flight data, but now it includes an AI chatbot powered by the DeepSeek-R1 API. This lets users ask questions about flights using natural language and get real-time information quickly.

The system combines a strong backend with live data from the Aerodatabox API. It supports flight status updates, delay checks, and route details through a user-friendly chat interface. This report covers the project’s goals, scope, technical setup, features, and challenges.

---

## 2. Objectives & Scope

### Objectives:
- **Conversational Flight Tracking**: Allow users to interact with the system using natural language to get flight information such as delays, arrival time, and status.
- **Real-Time Data Integration**: Collect live flight data through trusted APIs including departure, arrival, and route updates.
- **Improved Accessibility**: Make the system accessible on any modern browser without installations or setup.

### Scope:
- **Backend Integration**: Add DeepSeek-R1 (hosted on Groq) to the existing Django backend to handle flight-related user queries effectively.
- **Intuitive Chat Interface**: Build a smooth and interactive interface using HTML, CSS, and JavaScript with no full-page reloads.
- **Data Sources**: Use Aerodatabox API via MagicAPI proxy to fetch real-time data.
- **AI Integration & Context Management**: Integrate DeepSeek-R1 through API only, using structured prompts and response limits to keep answers relevant and short.
- **System Reliability**: Include fallback handling for API issues and ensure the system responds smoothly even with incomplete data.

---

## 3. Technology Stack

### Presentation Layer:
- **Django** – Web framework handling routing and backend logic.
- **HTML/CSS/JavaScript** – Frontend UI with custom Tailwind-inspired design (without using actual Tailwind).

### Intelligence Layer:
- **DeepSeek-R1-70B API** – Processes and responds to user queries.
- **Groq LPU** – Provides fast inference for real-time performance.

### Data Layer:
- **Aerodatabox API** – Main flight data provider.
- **Groq API** – Hosts the DeepSeek-R1 model for chatbot interaction.

---

## 4. Implementation

### User Interface & Experience:
- **Flight Search Form**: Validates flight number input (e.g., "TK123") and displays dynamic data like arrival time and progress.
- **Dynamic Chatbox**: Floating widget for asking questions like "Is TK1991 delayed?" and receiving smart, AI-powered responses.
- **Visual Flight Tracker**: Uses visual indicators like status badges and progress bars to display flight details clearly.

### AI Integration & Functionality

- **API-Based AI Integration**: The chatbot uses the pre-trained **DeepSeek-R1-distill-llama-70b** model hosted on **Groq**, connected via the **LangChain** framework.

- **Custom Endpoints**:
  - *search_flight* – *Fetches and formats real-time flight data from Aerodatabox via MagicAPI.*
  - *chat_assistant* – *Sends user queries and flight data to the AI, then returns structured responses.*

- **Prompt Engineering**:
  - Limit responses to 2 sentences  
  - Use consistent date/time formats  
  - Keep responses flight-specific  
  - Enforce clear language and measurement units

- **Data Handling**: Includes error handling for API failures and selects the most relevant flight when multiple matches exist. Also calculates progress and remaining time.

- **Response Processing**: Cleans AI output to remove unwanted formatting (e.g., markdown artifacts) for clarity and consistency.

### Performance Optimizations:
- **Low Latency Handling**: Groq LPU speeds up AI responses to meet real-time expectations.
- **Asynchronous Data Processing**: Frontend uses Fetch API for seamless data updates without reloading.

### Challenges Faced:
- **API Reliability**: Xmagic API issues limited its use, making Aerodatabox the main source.
- **Data Consistency**: Managing real-time updates across components required careful asynchronous handling.
- **User Experience Enhancements**: Continuous testing helped balance performance with advanced features in both backend and frontend.

---

## 5. Conclusion

The AI Chatbot Aviation Tracker successfully brings together a Django backend, real-time flight data, and natural language AI to deliver a modern flight tracking experience. The system allows users to ask simple questions about flights—such as delays, departure times, or arrival details—and receive clear and accurate answers instantly through an interactive chat interface.

Throughout the development process, we focused on stability, data accuracy, and a smooth user experience. By using trusted APIs and carefully structured prompts, the AI component was able to provide relevant responses without going off-topic. Features like visual flight progress, smooth data updates, and clean design helped create a better user experience overall.

All key objectives of the project have been met. The system works without the need for future updates or additions. It is complete, functional, and capable of supporting real-world usage. The AI Chatbot Aviation Tracker shows how modern technologies like large language models and live APIs can be combined effectively in a web-based application.

---

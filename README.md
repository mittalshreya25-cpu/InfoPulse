# Infopulse Live 🌍✨

Infopulse Live is an autonomous, AI-powered news aggregation and intelligence platform. It dynamically scrapes, categorizes, and summarizes the latest global news using generative AI, presenting it through a stunning, space-themed interactive user interface.

## 🚀 Key Features

*   **Autonomous News Ingestion**: Automatically pulls breaking news from top-tier RSS feeds across various genres (Tech, Startups, Markets & Forex, AI Research, Politics).
*   **AI-Powered Summaries**: Integrates with the Google Gemini API to instantly generate "TL;DR" bullet points and "Explain Like I'm 5" (ELI5) simplified breakdowns for every single article.
*   **Dynamic Engagement Tracking**: Features a custom-built analytics engine that tracks user views and reads, automatically bubbling the most engaging and viral stories up to the live "Trending News" sidebar.
*   **Financial Market Integrations**: Includes a live scrolling stock ticker and a real-time currency conversion widget built into the dashboard.
*   **Immersive UI/UX**: Features a highly interactive, animated React frontend with a procedural HTML5 Canvas-based twinkling starfield and a glowing, rotating Earth background.

## 🛠️ Technology Stack

### Backend
*   **Framework**: Python / FastAPI
*   **Database**: PostgreSQL via SQLAlchemy ORM
*   **Task Scheduling**: APScheduler (for background ingestion loops)
*   **AI Integration**: `google-genai` SDK (Gemini 3.1 Flash-Lite)
*   **Parsing**: Beautiful Soup 4 (BS4), Feedparser

### Frontend
*   **Framework**: React (Vite)
*   **Styling**: Pure CSS with advanced animations, flexbox/grid layouts, and glassmorphism UI components.
*   **HTTP Client**: Axios

## ⚙️ Setup & Installation

### 1. Backend Setup
Navigate to the root directory (`newsapp_backend`):
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create a .env file and add your configuration:
# DATABASE_URL=postgresql://user:password@localhost:5432/newsdb
# GEMINI_API_KEY=your_gemini_api_key

# Run the FastAPI server
uvicorn app.main:app --reload
```

### 2. Frontend Setup
Navigate to the frontend directory (`newsapp_frontend`):
```bash
cd newsapp_frontend

# Install dependencies
npm install

# Start the Vite development server
npm run dev
```

## 🧠 Architecture Overview
*   **`app/services/ingest.py`**: The heartbeat of the app. It scrapes RSS feeds, checks for duplicates, and pipelines content to the summarizer.
*   **`app/services/summarizer.py`**: Interacts with the Gemini API to break down complex articles into digestible insights.
*   **`app/routers/articles.py`**: Serves the REST API endpoints consumed by the React frontend, handling both article delivery and engagement tracking (clicks/reads).
*   **`newsapp_frontend/src/components/Starfield.jsx`**: A custom React component rendering a procedural math-driven HTML5 canvas to simulate a realistic space environment.

## 📝 License
This project is open-source and available under the MIT License.

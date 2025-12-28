# Vigile_devsprinthackathon
🛡️ VIGILE: Real-Time AI Chat Moderation Engine VIGILE is an intelligent moderation middleware designed to transform toxic digital environments into safe, constructive spaces. Unlike traditional keyword filters, VIGILE uses Large Language Models (LLMs) to understand intent, score toxicity on a granular scale, and provide real-time behavioral corrections.

🌟 The Problem Online communities often struggle with a binary "Allow or Block" approach that fails to catch nuanced toxicity or guide users toward better behavior.

💡 The VIGILE Solution VIGILE introduces a Dual-Threshold Logic Gate:

Warning Zone: Identifies mild unprofessionalism and warns the user without stopping the flow.

Hard-Gate Block: Intercepts high-toxicity messages and immediately suggests a polite, AI-generated alternative to help the user rephrase.

🛠️ Tech Stack Core Engine: Python 3.10+

AI Orchestration: Google Gemini 2.0 Flash (Multimodal-ready)

Interface: Streamlit (High-performance web UI)

Security: Environment-based secret management (python-dotenv & Streamlit Secrets)

🚀 Features Granular Toxicity Scoring: 0-10 scale analysis for every message.

Live Admin Audit Logs: Real-time visibility into moderation decisions in the sidebar.

Customizable Strictness: Dynamic sliders to adjust "Hard-Gate" and "Warning" sensitivities on the fly.

Bypass Logic: Local "Emergency Bypass" for common greetings to reduce API latency.

Resilient Architecture: Dual-model fallback system (Gemini 2.0 -> Fallback) to ensure uptime during high traffic.

📂 Project Structure Plaintext

├── vigile.py # Main Application Logic ├── .env # API Credentials (Local Only) ├── .gitignore # Security rules to prevent key leaks ├── requirements.txt # Dependency manifest └── README.md # Documentation 🔧 Installation & Setup Clone the Repo:

Bash

git clone https://github.com/your-username/vigile-moderator.git cd vigile-moderator Install Dependencies:

Bash

pip install -r requirements.txt Configure Environment: Create a .env file and add your Google AI Studio key:

Plaintext

Gemini_api_key="your_api_key_here" Run VIGILE:

Bash

streamlit run vigile.py

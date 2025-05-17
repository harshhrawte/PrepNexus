# PrepNexus

PrepNexus is an AI-powered Resume Analysis and Interview Preparation system designed to enhance job search and interview success.

Features
AI-driven Resume Analysis: Utilizes a fine-tuned RoBERTa model to recommend the best job roles tailored to candidate profiles.

Intelligent Interview Chatbot: Built with LangChain and ChromaDB, powered by LLaMA-3 (8B) to provide real-time, context-aware technical interview Q&A.

Automated Job Scraper: Uses BeautifulSoup to fetch up-to-date job listings from Indeed, improving job search efficiency by 40%.

Setup Instructions 

---

## Important Notes

### Large folders excluded from this repository:
- `env/` (Python environment) — Please create your own environment using the provided requirements.
- `roberta_resume/` (Model folder) — Download from [Google Drive link here].
- `final_qg_model/` (Model folder) — Download from [Google Drive link here].

These folders are excluded from the repo to keep it lightweight.

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/harshhrawte/PrepNexus.git
   cd PrepNexus
python -m venv env
# Windows
.\env\Scripts\activate

pip install -r requirements.txt

# macOS/Linux
source env/bin/activate

pip install -r requirements.txt

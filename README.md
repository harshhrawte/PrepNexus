# PrepNexus 

PrepNexus is an AI-powered Resume Analysis and Interview Preparation system designed to enhance job search and interview success.

I published an Article on my following project :

https://app.readytensor.ai/publications/cracking-the-interview-with-ai-how-prepnexus-predicts-roles-finds-jobs-and-prepares-you-with-qna-P8iyLvTGNvBw 

Features
AI-driven Resume Analysis: Utilizes a fine-tuned RoBERTa model to recommend the best job roles tailored to candidate profiles.

Intelligent Interview Chatbot: Built with LangChain and ChromaDB, powered by LLaMA-3 (8B) to provide real-time, context-aware technical interview Q&A.

Automated Job Scraper: Uses BeautifulSoup to fetch up-to-date job listings from Indeed, improving job search efficiency by 40%.



Setup Instructions 

---

## Important Notes

### Large folders excluded from this repository:
- `env/` (Python environment) — Please create your own environment using the provided requirements.
- `roberta_resume/` (Model folder) — Download from [[Google Drive link here](https://drive.google.com/drive/folders/14iv4NwmxIZd5urdG3k7zQXNcoaAGqkgH?usp=sharing)].
- `final_qg_model/` (Model folder) — Download from [[Google Drive link here](https://drive.google.com/drive/folders/14iv4NwmxIZd5urdG3k7zQXNcoaAGqkgH?usp=sharing)].

Colab NoteBook- https://colab.research.google.com/drive/1dBJYWoto6PAJHSz-CLj8o_gpTAVJ4spW?usp=sharing 
of RoBERTa for
resume role predictor.

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

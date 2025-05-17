from flask import Flask, render_template, request, jsonify
import os
import torch
import joblib
import PyPDF2
import requests
from bs4 import BeautifulSoup
from transformers import RobertaTokenizer, RobertaForSequenceClassification
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import chromadb
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Flask setup
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"

# Load RoBERTa model for role prediction
MODEL_DIR = r"C:\Harsh\Desktop\PrepNexus\roberta_resume\content\roberta_resume"
device = "cuda" if torch.cuda.is_available() else "cpu"
role_model = RobertaForSequenceClassification.from_pretrained(MODEL_DIR)
role_tokenizer = RobertaTokenizer.from_pretrained(MODEL_DIR)
role_label_mapping = joblib.load(os.path.join(MODEL_DIR, "label_mapping.pkl"))
role_model.to(device)
role_model.eval()

# Load environment and LLM
load_dotenv(override=True)
GROQ_KEY = os.getenv("GROQ_API_KEY", "").strip()
if not GROQ_KEY or not GROQ_KEY.startswith("gsk_") or len(GROQ_KEY) != 56:
    raise ValueError("Invalid or missing GROQ_API_KEY in .env")

llm = ChatGroq(
    groq_api_key=GROQ_KEY,
    model_name="Llama3-8b-8192",
    temperature=0.7,
    max_tokens=1024
)

interview_chain = (
    ChatPromptTemplate.from_template(
        "Act as a senior {role} hiring manager. Generate 10 technical interview questions along with detailed, correct answers for each. Format each question and answer pair as:\n\n1. Question: ...\n   Answer: ..."
    )
    | llm
    | StrOutputParser()
)

# Resume PDF extraction
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

# Predict role from resume
def predict_role_from_text(text):
    inputs = role_tokenizer(text, return_tensors="pt", truncation=True, padding='max_length', max_length=256)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = role_model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1).item()
    return list(role_label_mapping.keys())[prediction]

# Initialize Chroma vector store
def initialize_chroma():
    chroma_db_path = r"C:\Harsh\Desktop\PrepNexus\chroma_db"
    if not os.path.exists(chroma_db_path):
        os.makedirs(chroma_db_path)
    client = chromadb.Client()
    collection = client.get_or_create_collection(name="resume_collection")
    return collection

# Load Chroma collection
collection = initialize_chroma()

# Web Scraping Function
def fetch_jobs(query):
    headers = {"User-Agent": "Mozilla/5.0"}
    query = query.replace(" ", "+")
    url = f"https://in.indeed.com/jobs?q={query}&l="
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    job_cards = soup.find_all("a", attrs={"data-hide-spinner": "true"}, limit=5)
    jobs = []
    for job in job_cards:
        title = job.text.strip()
        link = f"https://in.indeed.com{job['href']}"
        jobs.append(f"{title} - {link}")
    return "\n\n".join(jobs) if jobs else "No current openings found."

# Flask Routes
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "resume" not in request.files:
        return "No file uploaded", 400
    resume = request.files["resume"]
    if resume.filename == "":
        return "No file selected", 400
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], resume.filename)
    resume.save(filepath)
    resume_text = extract_text_from_pdf(filepath)
    predicted_role = predict_role_from_text(resume_text)
    return render_template("main.html", predicted_role=predicted_role)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    role = data.get("role", "")
    if not role:
        return jsonify({"response": "Please specify a role to generate questions or search jobs."})

    # Job Search Trigger
    if any(kw in role.lower() for kw in ["company", "hiring", "available", "jobs", "openings"]):
        try:
            jobs = fetch_jobs(role)
            return jsonify({"response": f"Here are some current job openings:\n\n{jobs}"})
        except Exception as e:
            return jsonify({"response": f"Error fetching job listings: {str(e)}"})

    # Interview Question Generation
    try:
        response = interview_chain.invoke({"role": role})
        return jsonify({"response": response.strip()})
    except Exception as e:
        return jsonify({"response": f"Error generating questions and answers: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)

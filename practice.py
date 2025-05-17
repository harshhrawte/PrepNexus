import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# --- Environment Setup ---
print(f"🔄 Loading environment from: {os.getcwd()}")
load_dotenv(override=True)  # Force reload environment variables

# --- API Key Validation ---
GROQ_KEY = os.getenv("GROQ_API_KEY", "").strip()

# Validation checks
if not GROQ_KEY:
    raise ValueError("""
    ❌ GROQ_API_KEY not found in .env file!
    Create a .env file with:
    GROQ_API_KEY=your_actual_key_here
    """)

if not GROQ_KEY.startswith("gsk_") or len(GROQ_KEY) != 56:
    raise ValueError(f"""
    ❌ Invalid API key format!
    → Received: '{GROQ_KEY[:12]}...' (Length: {len(GROQ_KEY)})
    → Key should start with 'gsk_' and be 56 characters long
    → Get a valid key: https://console.groq.com/keys
    """)

# --- Model Configuration ---
LLM_CONFIG = {
    "groq_api_key": GROQ_KEY,
    "model_name": "Llama3-8b-8192",
    "temperature": 0.7,
    "max_tokens": 1024,
    "max_retries": 3,
    "request_timeout": 30
}

llm = ChatGroq(**LLM_CONFIG)

# --- Interview Chain ---
interview_chain = (
    ChatPromptTemplate.from_template(
        """Act as a senior {role} hiring manager. Generate 10 technical interview questions.
        Format as a numbered list with one question per line. Include both coding and system design questions.
        Role: {role}"""
    )
    | llm
    | StrOutputParser()
)

# --- Core Functionality ---
# --- CLI Interface ---
def main():
    print("\n🤖 Welcome! I’m PrepNexus – your personal AI Interview Guide 🤝")
    print("--------------------------------------------------------------")
    
    while True:
        try:
            cmd = input("\n📩 How can I assist you today? (Type 'questions' or 'exit'): ").lower().strip()
            
            if cmd in ('exit', 'quit'):
                print("\n🎉 Thank you for chatting with PrepNexus! Best of luck with your interviews! 🚀")
                print("💡 Remember: Confidence + Consistency = Success 💼")
                break
            
            elif cmd in ('questions', 'q'):
                generate_interview_questions()
            
            else:
                print("❔ Hmm, I didn’t get that. Try typing 'questions' to begin or 'exit' to quit.")

        except KeyboardInterrupt:
            print("\n👋 Session ended. Thank you for trusting PrepNexus!")
            break

# --- Core Functionality ---
def generate_interview_questions():
    """Generate and display interview questions with error handling"""
    try:
        role = input("\n🎯 Which role are you preparing for?\n💬 PrepNexus: I'm here to help! Just type the role: ").strip()
        if not role:
            print("⚠️ Oops! Please enter a valid role so I can guide you better.")
            return

        print(f"\n⏳ PrepNexus is preparing tailored questions for the role: {role}...")

        technical_roles = {'developer', 'engineer', 'programmer', 'swe', 'data scientist'}
        is_technical = any(term in role.lower() for term in technical_roles)

        prompt_template = """Act as a senior {role} hiring manager. Generate 10 {question_type} interview questions.
        Format as a numbered list with one question per line. Questions should be specific to {role} responsibilities.
        Role: {role}"""

        raw_questions = interview_chain.invoke({
            "role": role,
            "question_type": "technical" if is_technical else "role-specific competency-based"
        })

        questions = []
        for q in raw_questions.split("\n"):
            q = q.strip()
            if not q:
                continue
            q = q.split(". ", 1)[-1].replace("**", "").replace("*", "")
            if q.lower().startswith(('here are', 'certainly')):
                continue
            questions.append(q)

        print(f"\n📋 PrepNexus has crafted the top 10 interview questions for {role}:")
        for i, q in enumerate(questions[:10], 1):
            print(f"{i}. {q}")
        print("\n✅ All the best! Let me know if you'd like more help.")

    except Exception as e:
        print(f"\n❌ PrepNexus ran into an issue: {str(e)}")
        print("🛠️ Troubleshooting Tips:")
        print("- Check https://status.groq.com/ for API status")
        print("- Verify your API key in the .env file")
        print("- Make sure your internet connection is active")


# --- CLI Interface ---
def main():
    print("\n PrepNexus")
    print("----------------------------")
    
    while True:
        try:
            cmd = input("\n🔧 Command (questions/exit): ").lower().strip()
            if cmd in ('exit', 'quit'):
                print("\n🎉 Good luck with your interviews! Thank You For Connecting with PrepNexus")
                break
            elif cmd in ('questions', 'q'):
                generate_interview_questions()
            else:
                print("❔ Unknown command. Try 'questions' or 'exit'")
        
        except KeyboardInterrupt:
            print("\n👋 Session ended gracefully. You've got this!")
            break

if __name__ == "__main__":
    main()
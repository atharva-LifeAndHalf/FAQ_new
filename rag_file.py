# rag_file.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# --- COMMUNITY IMPORTS ---
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# --- CORE/EXPRESSION LANGUAGE IMPORTS ---
from langchain_core.prompts import PromptTemplate # Fixed
from langchain.chains import RetrievalQA
# Load env
load_dotenv()
gemini_key = os.getenv("gemini_key")

# --------------- INITIALIZE LLM ----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key
)

# --------------- LOAD DATA ----------------
loader = UnstructuredExcelLoader("C://Users//ss//OneDrive//Desktop//LandH//FAQ Bot//FAQ_file.xlsx")
data = loader.load()
texts = [doc.page_content for doc in data]

# --------------- EMBEDDINGS ----------------
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# --------------- VECTOR DB ----------------
vector_path = "L&H-FAQ-POC"

# Create only once → avoids Streamlit re-running this each refresh
if not os.path.exists(vector_path):
    vector_db = FAISS.from_texts(texts, embedding_model)
    vector_db.save_local(vector_path)

db = FAISS.load_local(vector_path, embedding_model, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

# --------------- PROMPT TEMPLATE ----------------
prompt_template = PromptTemplate(
    template="""
You are an intelligent FAQ assistant.
Rules:
1. Use ONLY the information in context.
2. If context is irrelevant or empty, say:
   "I don't know. Please wait for the Human reply."
3. Never guess or hallucinate.

Context:
{context}

User Question:
{question}

Answer:
""",
    input_variables=['context', 'question']
)

# --------------- CHAIN ----------------
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    input_key='question',
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

# --------------- MAIN FUNCTION ----------------
def ask_bot(query):
    """Called by Streamlit"""
    response = chain({"question": query})

    answer = response["result"]
    sources = response["source_documents"]

    # Extract context text
    context_text = " ".join([s.page_content for s in sources]).strip()

    # IDK logic
    if context_text == "" or len(context_text) < 10:
        return "I don't know. Please wait for the Human reply."

    hallucination_phrases = ["i am not sure", "cannot answer", "as an ai", "no information"]
    if any(x in answer.lower() for x in hallucination_phrases):
        return "I don't know. Please wait for the Human reply."

    return answer






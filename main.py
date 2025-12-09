from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredExcelLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

load_dotenv()
gemini_key = os.getenv("gemini_key")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=gemini_key
)

loader = UnstructuredExcelLoader("FAQ_file.xlsx")
data = loader.load()
texts = [doc.page_content for doc in data]

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_path = "L&H-FAQ-POC"

vector_db = FAISS.from_texts(texts, embedding_model)
vector_db.save_local(vector_path)

db = FAISS.load_local(vector_path, embedding_model, allow_dangerous_deserialization=True)
retriever = db.as_retriever(search_kwargs={"k": 3})

prompt_template = PromptTemplate(
    template="""
You are an intelligent FAQ assistant.
Follow the rules strictly:

1. Use ONLY the information in the context.
2. If context does not contain the answer OR is irrelevant, say:
   "I don't know. Please wait for the Human reply."
3. Do NOT guess.  
4. Respond politely and clearly.

Context Retrieved:
{context}

User Question:
{question}

Final Answer:
""",
    input_variables=['context', 'question']
)

chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    input_key='question',
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template}
)

def ask_bot(query):
    response = chain({"question": query})

    answer = response["result"]
    sources = response["source_documents"]

    context_text = " ".join([s.page_content for s in sources]).strip()

    if context_text == "" or len(context_text) < 10:
        return "I don't know. Please wait for the Human reply."

    hallucination_phrases = ["I'm not sure", "cannot answer", "as an AI", "no information"]
    if any(x in answer.lower() for x in hallucination_phrases):
        return "I don't know. Please wait for the Human reply."

    return answer

print(ask_bot("Can I take the BootCamp?"))  # valid
print(ask_bot("What is the capital of Jupiter 5000?"))  # nonsense

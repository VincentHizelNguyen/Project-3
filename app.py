"""Korea Study RAG assistant with a modern Gradio UI."""
from pathlib import Path
import os
import numpy as np
import gradio as gr
from dotenv import load_dotenv
from google import genai
from sentence_transformers import SentenceTransformer

load_dotenv()
ROOT = Path(__file__).resolve().parent
KB = ROOT / "knowledge-base"
MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
TOP_K = int(os.getenv("TOP_K", "5"))

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("Missing GEMINI_API_KEY. Copy .env.example to .env and add your key.")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
embedder = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

def load_documents():
    docs = []
    if not KB.exists():
        return docs
    for path in KB.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            docs.append({"name": path.stem, "path": str(path.relative_to(ROOT)), "text": text})
    return docs

documents = load_documents()
embeddings = embedder.encode([d["text"] for d in documents], normalize_embeddings=True) if documents else np.empty((0, 384))

def retrieve(query):
    if not documents:
        return []
    q = embedder.encode([query], normalize_embeddings=True)[0]
    scores = embeddings @ q
    indexes = np.argsort(scores)[::-1][:TOP_K]
    return [(documents[i], float(scores[i])) for i in indexes]

def answer(message, history):
    hits = retrieve(message)
    context = "\n\n".join(f"[{d['name']}]\n{d['text']}" for d, _ in hits)
    prompt = f"""You are Korea Study's helpful education assistant. Answer in the user's language.\nUse only the supplied context when making factual claims. If the context is insufficient, say so clearly.\n\nCONTEXT:\n{context or '(No knowledge-base documents found.)'}\n\nUSER QUESTION:\n{message}"""
    response = client.models.generate_content(model=MODEL, contents=prompt)
    answer_text = response.text or "I could not generate an answer."
    if hits:
        sources = "\n\n**Nguồn tham khảo:** " + ", ".join(d["name"] for d, _ in hits)
        answer_text += sources
    return answer_text

css = """
.gradio-container {max-width: 1100px !important; margin: auto;}
#title {text-align:center; margin-bottom: 0.5rem;}
#subtitle {text-align:center; opacity:0.75;}
"""
with gr.Blocks(css=css, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎓 Korea Study AI Assistant", elem_id="title")
    gr.Markdown("Ask about schools, employees, services and Korean study visas.", elem_id="subtitle")
    gr.ChatInterface(fn=answer, title="Chat with your study assistant", examples=[
        "What services does Korea Study provide?",
        "Compare D-2 and D-4 visas.",
        "Tell me about KAIST."
    ])

if __name__ == "__main__":
    demo.launch()

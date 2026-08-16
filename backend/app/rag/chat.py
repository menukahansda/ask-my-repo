from google import genai

from app.config import GEMINI_API_KEY
from app.rag.retriever import retrieve

genai_client = genai.Client(api_key=GEMINI_API_KEY)


def generate_prompt(query, results):
    context_blocks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        context_blocks.append(f"File: {meta['file_origin']}\n{doc}")

    context = "\n\n---\n\n".join(context_blocks)

    prompt = f"""...
Answer the question using only the context above.
At the end, output a line starting with "CITED_FILES:" followed by a comma-separated list of exactly which files (from the context) you used to answer.

Context:
{context}

Question: {query}

Answer:"""
    return prompt


def chat(query, n_results=5):
    embed_results = retrieve(query, n_results=n_results)
    prompt = generate_prompt(query, embed_results)

    response = genai_client.models.generate_content(
        model="gemini-flash-lite-latest",
        contents=prompt,
    )

    sources = list({meta["file_origin"] for meta in embed_results["metadatas"][0]})
    answer_text = response.text
    answer = ""
    cited_files = []

    if "CITED_FILES:" in answer_text:
        answer, cited_line = answer_text.split("CITED_FILES:")
        cited_files = [f.strip() for f in cited_line.strip().split(",")]
    else:
        answer = answer_text
    
    if not cited_files: 
        cited_files = sources
        
    return {
        "answer": answer,
        "sources": cited_files,
    }


if __name__ == "__main__":
    user_query = "What is the purpose of the 'task_management_system' repository?"
    result = chat(user_query)
    print(result["answer"])
    print("\nSources:", result["sources"])

import argparse
from langchain.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from typing import List, Dict

from get_embedding_function import get_embedding_function

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Previous conversation:
{chat_history}

Current context:
{context}

---

Given the conversation history above and the current context, answer this question: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    query_rag(query_text)


def query_rag(query_text: str, chat_history: List[Dict[str, str]] = None):
    # Prepare the DB
    embedding_function = get_embedding_function()
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB
    results = db.similarity_search_with_score(query_text, k=5)
    
    # Format chat history
    formatted_history = ""
    if chat_history:
        for msg in chat_history[-3:]:  # Only use last 3 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            formatted_history += f"{role}: {msg['content']}\n"

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(
        context=context_text,
        question=query_text,
        chat_history=formatted_history
    )

    model = OllamaLLM(model="llama3.2:3b")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    return f"Response: {response_text}\n\nSources: {sources}"


if __name__ == "__main__":
    main()

# AI Agent 

**AI Agent** is a powerful conversational AI interface built using Streamlit, LangChain, and Chroma vector storage. It leverages retrieval augmented generation (RAG) to provide intelligent, context-aware responses to your queries.

---

## Features

- **Interactive Chat Interface:** A sleek and modern UI built with Streamlit.
- **RAG Pipeline:** Integrates vector similarity search to bring relevant context from your documents.
- **Document Ingestion:** Processes PDFs and TXT files, splitting them into manageable chunks.
- **Customizable Design:** Tailor the look and feel easily using custom CSS.
- **Database Management:** User-friendly controls for updating the document database and clearing the cache.

---

## Project Structure

- **app.py:** Main entry point for the web interface.
- **populate_database.py:** Loads, processes, and populates the database with documents.
- **query_data.py:** Handles query processing and response generation using an LLM.
- **get_embedding_function.py:** Configures and returns the embedding function for vector searches.
- **requirements.txt:** Lists the necessary Python dependencies.
- **.gitignore:** Specifies ignored files and folders for version control.

---

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your_username/ai-agent.git
   cd ai-agent
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     .\venv\Scripts\activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Running the Web Interface

Start the Streamlit app with:

```bash
streamlit run app.py
```

### Managing the Database

- **Update Database:** Click the "Update DB" button in the sidebar.
- **Clear Cache:** Click the "Clear Cache" button in the sidebar.
- **Reset Database:** Run the following command to clear and rebuild the database:
  
  ```bash
  python populate_database.py --reset
  ```

---

## Configuration

- **Data Directory:** The application loads documents from the `data` directory by default.
- **Custom CSS:** Modify the CSS in `app.py` to adjust the interface styling as needed.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements. For significant changes, open an issue first to discuss your ideas.

---

## License

Distributed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

- **LangChain:** Empowering advanced conversational AI.
- **Streamlit:** Simplifying the creation of interactive web applications.
- **Chroma:** Providing robust vector storage and similarity search.
- **Ollama:** Supplying high-quality language models and embeddings.

---

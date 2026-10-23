# Syllabus RAG Assistant

A chat assistant that answers questions about a B.Tech syllabus using only the course document, instead of the LLM's general knowledge.

## How it works

1. `index.ipynb` extracts text from `Syllabus.pdf`, cleans it, and splits it into 224 overlapping chunks (1,000 characters, 200 overlap).
2. Each chunk is embedded with `sentence-transformers/all-mpnet-base-v2` (768 dimensions) and stored in a Pinecone serverless index using cosine similarity.
3. `query.py` retrieves the top 4 chunks for a question and passes them to Llama 3.1 8B on Groq through a LangChain pipeline. The prompt tells the model to answer only from the retrieved context and to say it doesn't know otherwise.
4. `app.py` is a Streamlit chat interface with session history.

## Stack

Python · LangChain · Pinecone · Hugging Face sentence-transformers · Groq API · Streamlit

## Run it

Create a `.env` file with `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `HOST_KEY` and `GROQ_API_KEY`. Run `index.ipynb` once to build the index, then:

```bash
pip install langchain-core langchain-huggingface langchain-pinecone langchain-groq pinecone streamlit python-dotenv pdfminer.six
streamlit run app.py
```

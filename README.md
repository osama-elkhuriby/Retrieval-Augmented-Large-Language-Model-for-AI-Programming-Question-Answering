# Retrieval-Augmented-Large-Language-Model-for-AI-Programming-Question-Answering
A small-scale AI assistant for answering questions about AI programming (Python, PyTorch, TensorFlow, ML concepts) using Retrieval-Augmented Generation (RAG) over a curated set of technical documents.


## Installations

### Install the required packages
```bash
$ pip install -r requirements.txt
```

### Setup the environments variables
```bash
$ cp .env.example .env
```

### Run FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

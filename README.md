# Retrieval-Augmented-Large-Language-Model-for-AI-Programming-Question-Answering
A small-scale AI assistant for answering questions about AI programming (Python, PyTorch, TensorFlow, ML concepts) using Retrieval-Augmented Generation (RAG) over a curated set of technical documents.


## Recommended Setup

### Download Miniconda from https://www.anaconda.com/download

### Steps to install WSL:

1. Open PowerShell as Administrator.
2. Run:
   ```powershell
   wsl --install

### Setup the environment
```bash
$ conda create --name myenv python=3.11
$ conda activate myenv
```

### Install the required packages
```bash
$ pip install -r requirements.txt
```


### Ollama
```bash
$ irm https://ollama.com/install.ps1 | iex
```
### Download Studio 3T from https://robomongo.org/

### Setup the environment variables
```bash
$ cd Source
$ cp .env.example .env
$ cd ..
```
#### Put your own Values in .env 

### Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
$ sudo docker compose up -d
```
#### Put your own Values in .env 

### Run FastAPI server
```bash
$ cd Source
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```
### Run GUI
```bash
$ streamlit run rag_app.py
```
#### That's all

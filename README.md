# Retrieval-Augmented-Large-Language-Model-for-AI-Programming-Question-Answering
A small-scale AI assistant for answering questions about AI programming (Python, PyTorch, TensorFlow, ML concepts) using Retrieval-Augmented Generation (RAG) over a curated set of technical documents.


## Recommended Setup

### Download Miniconda form https://www.anaconda.com/download

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

### Setup the environments variables
```bash
$ cp .env.example .env
```
### Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
$ sudo docker compose up -d
```

### Run FastAPI server
```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

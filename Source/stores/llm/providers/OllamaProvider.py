from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum, OpenAIEnums
import ollama
import logging


class OllamaProvider(LLMInterface):

    def __init__(self,
                 embedding_model: str = "nomic-embed-text",
                 embedding_size: int = 768,
                 generation_model: str = None,
                 default_input_max_characters: int = 1000,
                 default_generation_max_output_tokens: int = 1024,
                 default_generation_temperature: float = 0.7):

        self.embedding_model = embedding_model
        self.embedding_size = embedding_size
        self.generation_model = generation_model
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature

        self.enums = OpenAIEnums
        self.logger = logging.getLogger(__name__)

    # -------------------------
    # Model setters
    # -------------------------

    def set_generation_model(self, model_id: str):
        self.generation_model = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model = model_id
        self.embedding_size = embedding_size

    # -------------------------
    # Utils
    # -------------------------

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    # -------------------------
    # Embeddings
    # -------------------------

    def embed_text(self, text: str, document_type: str = None):
        try:
            response = ollama.embeddings(
                model=self.embedding_model,
                prompt=self.process_text(text)
            )

            vector = response.get("embedding")

            if not vector:
                self.logger.error("Ollama returned empty embedding")
                return None

            return vector

        except Exception as e:
            self.logger.error(f"Ollama embedding failed: {e}")
            return None

    def embed_batch(self, texts: list, document_type: str = None):
        """Embed multiple texts in parallel using ollama."""
        import concurrent.futures
        
        def _embed(text):
            return self.embed_text(text, document_type)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            vectors = list(executor.map(_embed, texts))
        
        return vectors
    # -------------------------
    # Generation
    # -------------------------

    def generate_text(self, prompt: str, chat_history: list = [],
                      max_output_tokens: int = None,
                      temperature: float = None):
        if not self.generation_model:
            self.logger.error("Generation model not set")
            return None

        max_output_tokens = max_output_tokens or self.default_generation_max_output_tokens
        temperature = temperature or self.default_generation_temperature

        try:
            messages = chat_history + [{"role": "user", "content": prompt}]

            response = ollama.chat(
                model=self.generation_model,
                messages=messages,
                options={
                    "temperature": temperature,
                    "num_predict": max_output_tokens,
                }
            )

            return response["message"]["content"]

        except Exception as e:
            self.logger.error(f"Ollama generation failed: {e}")
            return None

    # -------------------------
    # Prompt construction
    # -------------------------

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "content": self.process_text(prompt)   # Ollama uses "content", not "text"
        }
from ..LLMInterface import LLMInterface
from ..LLMEnums import DocumentTypeEnum
import ollama
import logging


class OllamaProvider(LLMInterface):

    def __init__(self,
                 embedding_model: str = "nomic-embed-text",
                 default_input_max_characters: int = 1000):

        self.embedding_model = embedding_model
        self.default_input_max_characters = default_input_max_characters

        self.logger = logging.getLogger(__name__)

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

    # -------------------------
    # Optional generation stub
    # -------------------------

    def generate_text(self, *args, **kwargs):
        raise NotImplementedError("Use generation provider separately")

    def construct_prompt(self, prompt: str, role: str):
        return {
            "role": role,
            "text": self.process_text(prompt)
        }
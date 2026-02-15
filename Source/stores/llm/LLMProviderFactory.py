class LLMProviderFactory:
    def __init__(self,config:dict):
        self.config = config

    def create_provider(self, provider:str):
        pass
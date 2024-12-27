from ollama_llm import OllamaLLM
from openai_llm import OpenAILLM
from config import Config

class LLM:

    def __init__(self, config):
        # read config.json
        self.config = Config()
        self.model = config.llm_model_type.lower()  # 获取模型类型并转换为小写
        if self.model == "openai":
            self.llm = OpenAILLM()
        elif self.model == "ollama":
            self.llm = OllamaLLM(model=config.ollama_model_name, api_url=config.ollama_api_url)
        else:
            raise ValueError(f"Unsupported model type: {self.model}")  # 如果模型类型不支持，抛出错误

    def generate_daily_report(self, markdown_content):
        return self.llm.generate_daily_report(markdown_content)


if __name__ == "__main__":
    llm = LLM()
    print(llm.generate_daily_report("test"))
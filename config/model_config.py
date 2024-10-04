import os
from dotenv import load_dotenv

load_dotenv()

model_name = os.getenv("CHAT_MODEL")
provider = os.getenv("PROVIDER")
openai_api_key = os.getenv("OPENAI_API_KEY")
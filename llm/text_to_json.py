from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from utils.model_cost_calculator import calculate_cost
from config.prompt import get_prompt
from utils.record_usage import record_usage
from config.model_config import model_name, provider
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)


def completion(request, input):
    prompt = get_prompt(input)
    completion = client.chat.completions.create(
        response_format={"type": "json_object"},
        model=model_name,
        messages=[
            {"role": "system", "content": "You are an helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    api_key = request.headers.get('x-key')
    input_tokens = completion.usage.prompt_tokens
    output_tokens = completion.usage.completion_tokens
    cost = calculate_cost(provider, model_name, input_tokens, output_tokens)
    record_usage(api_key, input_tokens, output_tokens, cost)

    message = completion.choices[0].message.content
    if message:
        parsed_message = json.loads(message) 
        return parsed_message, cost, input_tokens, output_tokens
    else:
        return "No message returned from OpenAI."
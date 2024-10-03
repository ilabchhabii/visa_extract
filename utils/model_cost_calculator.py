def calculate_cost(provider, model_name, prompt_tokens, completion_tokens):
    try:
        if provider == "openai":
            if model_name == "gpt-4o-2024-08-06":
                input_cost = (prompt_tokens / 1000) * 0.00250
                output_cost = (completion_tokens / 1000) * 0.01000
                total_cost = input_cost + output_cost
                return round(total_cost, 5)

            elif model_name == "gpt-4o-mini-2024-07-18":
                input_cost = (prompt_tokens / 1000) * 0.000150
                output_cost = (completion_tokens / 1000) * 0.00060
                total_cost = input_cost + output_cost
                return round(total_cost, 5)

            elif model_name == "gpt-4o-2024-05-13":
                input_cost = (prompt_tokens / 1000) * 0.0050
                output_cost = (completion_tokens / 1000) * 0.0150
                total_cost = input_cost + output_cost
                return round(total_cost, 5)

        elif provider == "google":
            return 0.0

        elif provider == "groq":
            return 0.0
        
    except Exception as e:
        raise e
def get_prompt(text: str) -> str:
    return prompt.format(text=text)


prompt = """
You are tasked with converting the following text into a structured JSON format based on the given schema.

### Extracted Text
{text}

### JSON Schema
Your JSON output must strictly adhere to the following structure:

{{
  "form_name": "",
  "OMB_control_number": "",
  "form_number": "",
  "expires": "",
  "estimated_burden": "",
  "entry_information": {{
    "entrant_information": {{
      "name": {{
        "last_name": "",
        "first_name": "",
        "middle_name": ""
      }},
      "gender": "",
      "birth_date": "",
      "city_of_birth": "",
      "country_of_birth": "",
      "country_of_eligibility": "",
      "entrant_photograph": "",
      "mailing_address": {{
        "in_care_of": "",
        "address_line_1": "",
        "address_line_2": "",
        "city_town": "",
        "district_county_province_state": "",
        "postal_code_zip_code": "",
        "country": ""
      }},
      "country_where_live_today": "",
      "phone_number": "",
      "email_address": "",
      "highest_level_of_education": "",
      "marital_status": "",
      "number_of_children": 0
    }},
    "derivatives": {{
      "spouse_information": {{
        "name": {{
          "last_name": "",
          "first_name": "",
          "middle_name": ""
        }},
        "birth_date": "",
        "gender": "",
        "city_of_birth": "",
        "country_of_birth": "",
        "spouse_photograph": ""
      }},
      "children": [
        {{
          "name": {{
            "last_name": "",
            "first_name": "",
            "middle_name": ""
          }},
          "birth_date": "",
          "gender": "",
          "city_of_birth": "",
          "country_of_birth": "",
          "child_photograph": ""
        }}
      ]
    }}
  }}
}}

### Additional Information
Ensure that every field from the provided document is accurately represented in the final JSON output. Use the exact field names as they appear in the document, converting them to snake_case if necessary. If there additional fields in the input that are not in the schema provided, mention them with new keys(variables) in the JSON output.
If there are multiple entries for a field (e.g., multiple children), represent them as an array of objects.
Your task is to fill this JSON structure with the information provided in the extracted text, ensuring no information is lost in the conversion process.
"""

import openai
import utils
import os
import sys
import json


# TODO: create a script type mapping for the prompts
def build_prompt_from_product_data(product_details, script_type, duration):
    duration_word_mapping = {
        15: [30, 50],
        30: [50, 80]
    }
    
    script_type_mapping = {
        "how_to": "Emphasize how the product empowers users to feel confident, and express their personal style every day.",
        "product_highlights": "Clearly highlight the product’s standout features that adds value to the customer",
        "brand_value": "Emphasize the brand’s core values, mission, and what makes it trustworthy, innovative, or aspirational in the eyes of the customer"
    }
    
    script_type_value = script_type_mapping.get(script_type, "")
    min_word, max_word = duration_word_mapping.get(duration)[0], duration_word_mapping.get(duration)[1]
    
    prompt = f"""
    Write a first-person, emotionally engaging script for a video ad for {product_details['title']}. 
    Highlight key features such {product_details['about']}. 
    The description of the product is {product_details['description']}.
    {script_type_value}. The video ad should be {duration} seconds. 
    Do not bother with planning the actual shots for the video. 
    Just write it as a summary. Keep the word count within {min_word} - {max_word} words 
    Don't give any narration cues."""
    return prompt

# TODO: summarize the about and the description using another prompt
def get_openai_api_response(product_details, script_type, duration, openai_api_key):
    openai.api_key = openai_api_key
    
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": build_prompt_from_product_data(product_details, script_type, duration)}
        ],
        temperature=0.8
    )
    output = utils.post_process_output(response.choices[0].message["content"])
    return output

# # TODO: summarize the about and the description using another prompt
# def get_openai_api_response(product_details, script_type, duration, openai_api_key):

#     openai.api_key = DEFAULT_OPEN_API_KEY
#     # extracted_data = utils.load_json_file("data/amazon_product_data.json") # trimmer
#     extracted_data = utils.load_json_file("/Users/macbook/Desktop/Projects/video_ad_gen/backend/python/prompt/amazon_product_s25.json") # S25
#     title = extracted_data.get("title", "")
#     about = extracted_data.get("about", "")
#     description = extracted_data.get("description", "")

#     client = openai.OpenAI(api_key = DEFAULT_OPEN_API_KEY)
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "user", "content": build_prompt_from_gpt(title, about, description)}
#         ],
#         temperature=0.8
#     )
    
#     output = utils.post_process_output(response.choices[0].message.content)
#     return output

if __name__ == "__main__":
    product_details = sys.argv[1]
    product_details = json.loads(product_details)
    script_type = sys.argv[2]
    duration = int(sys.argv[3])
    openai_api_key = sys.argv[4]
    output = get_openai_api_response(product_details, script_type, duration, openai_api_key)
    print(output)
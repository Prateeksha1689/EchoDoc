# #setup groq api
# import os

# GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

# #convert image to required format
# import base64

# # image_path="skin_rash.jpg"

# def encode_image(image_path):
#     image_file=open(image_path,"rb")
#     return base64.b64encode(image_file.read()).decode('utf-8')

# #setup multimodal LLM
# from groq import Groq

# query="what is wrong with my hand?"
# model="meta-llama/llama-4-scout-17b-16e-instruct"


# def analyse_image_with_query(query,encoded_image,model):
#     client=Groq()
    
#     messages=[
#             {
#                 "role": "user",
#                 "content": [
#                     {
#                         "type": "text", 
#                         "text": query
#                     },
#                     {
#                         "type": "image_url",
#                         "image_url": {
#                             "url": f"data:image/jpeg;base64,{encoded_image}",
#                         },
#                     },
#                 ],
#             }]
#     chat_completion=client.chat.completions.create(
#         messages=messages,
#         model=model
#     )

#     return chat_completion.choices[0].message.content


import base64
import os
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyse_image_with_query(query, encoded_image, model="meta-llama/llama-4-scout-17b-16e-instruct"):
    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
            ]
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=1000
    )

    return response.choices
# %%
import json
import requests
import os


# %%
# Test the api for the genai_app
# @app.post("/info", response_model=List[QuestionAnswer])
# async def post_info(recipient_info: RecipientInfo):
#     ...
# %%
response = requests.post(
    "http://localhost:8000/info",
    json={"recipient_info": "John Doe"},
)
print(json.dumps(response.json(), indent=2))

# %%
recipient_info = """
I'm celebrating my best friend's birthday. We've been close since college, always sharing our love for hiking and 
outdoor adventures. One time, we got lost during a hike but ended up finding this beautiful, hidden waterfall, which is 
now our favorite spot. What I admire most about them is their relentless optimism, even in tough situations. 
They always find a way to smile and lift everyone's spirits.
"""
response = requests.post(
    "http://localhost:8000/info",
    json={"recipient_info": recipient_info},
)
print(json.dumps(response.json(), indent=2))
# """
# [{'question': 'What is your relationship with the recipient? (e.g., Family member, Colleague)',
#   'answer': 'best friend'},
#  {'question': 'What kind of activities or hobbies does the recipient enjoy? (e.g., Cooking, Hiking)',
#   'answer': 'hiking, outdoor adventures'},
#  {'question': "Share a memorable experience or moment you've had with the recipient. (e.g., A surprise party)",
#   'answer': 'Getting lost and discovering a hidden waterfall'}]
# """
# %%
# Test the api for the genai_app
# @app.post("/refine", response_model=EmailContent)
# async def post_refine(refined_input: List[RefineInput]):
refined_input =  [
{'question': 'What is your relationship with the recipient? (e.g., Family member, Colleague)',
  'answer': 'best friend'},
 {'question': 'What kind of activities or hobbies does the recipient enjoy? (e.g., Cooking, Hiking)',
  'answer': 'hiking, outdoor adventures'},
 {'question': "Share a memorable experience or moment you've had with the recipient. (e.g., A surprise party)",
  'answer': 'Getting lost and discovering a hidden waterfall'}]
response = requests.post(
    "http://localhost:8000/refine",
    json=refined_input)
print(json.dumps(response.json(), indent=2))

# """
# {'email_title': ' Title: "Reminiscing Our Adventure: A Letter of Friendship and Gratitude"',
#  'email_content': " Dear [Best Friend's Name],\n\nAs I sit down to pen this letter, I can't help but smile as I remember our adventure in the woods that led us to discovering a hidden waterfall. The thrill of getting lost together, the excitement in our voices as we heard the sound of rushing water growing louder, and the sense of accomplishment when we finally arrived at this breathtaking sight - it's memories like these that make our bond so strong.\n\nMay our friendship continue to lead us on many more adventures, both big and small. Here's to creating new memories and cherishing the old ones. I'm grateful for every moment we spend together, hiking through life's beautiful trails.\n\nWith love and appreciation,\n\n[Your Name]",
#  'email_image': 'base64_image_data'}
# """
# %%
import base64
# Use the base64_image_data to save the image
base64_image_data = response.json()['email_image']
image_data = base64.b64decode(base64_image_data)
with open('image.png', 'wb') as f:
    f.write(image_data)

# %%
# import json
# import requests
# url = "https://api.openai.com/v1/images/generations"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer {json.load(open('../secrets.json'))['openai_api_key']}"
# }
# data = {
#     "model": "dall-e-3",
#     "prompt": "a white Exotic Shorthair cat",
#     "response_format": "b64_json",
#     "n": 1,
#     "size": "1024x1024"
# }

# response_ = requests.post(url, headers=headers, json=data)

# # Print the response
# print(response_.json())

 # %%
 # save to json file
json.dump(response_.json(), open('response.json', 'w'))
# %%
# convert the images_base64 to image
import base64
import io
image_base64 = response_.json()['data']


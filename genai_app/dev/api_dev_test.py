# %%
import requests
# Test the api for the genai_app
# @app.post("/info", response_model=List[QuestionAnswer])
# async def post_info(recipient_info: RecipientInfo):
#     ...
# %%
response = requests.post(
    "http://localhost:8000/info",
    json={"recipient_info": "John Doe"},
)
print(response.json())


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
print(response.json())
"""
[{'question': 'What is your relationship with the recipient? (e.g., Family member, Colleague)',
  'answer': 'best friend',
  'placeholder': None},
 {'question': 'Describe a quality or trait you admire in the recipient. (e.g., Generosity, Humor)',
  'answer': 'Relentless optimism',
  'placeholder': 'Surprise me'},
 {'question': 'What kind of activities or hobbies does the recipient enjoy? (e.g., Cooking, Hiking)',
  'answer': 'hiking, outdoor adventures',
  'placeholder': 'Surprise me'},
 {'question': 'Is there a special message or sentiment you wish to convey? (e.g., Congratulations, Thank you)',
  'answer': "Celebrating friend's birthday, admire their optimism and love for outdoor adventures.",
  'placeholder': 'Surprise me'},
 {'question': "Share a memorable experience or moment you've had with the recipient. (e.g., A surprise party)",
  'answer': 'got lost during a hike, discovered hidden waterfall',
  'placeholder': 'Surprise me'}]
"""
# %%
# Test the api for the genai_app
# @app.post("/refine", response_model=EmailContent)
# async def post_refine(refined_input: List[RefineInput]):
refined_input =  [{'question': 'What is your relationship with the recipient? (e.g., Family member, Colleague)',
  'answer': 'best friend',
  'placeholder': None},
 {'question': 'Describe a quality or trait you admire in the recipient. (e.g., Generosity, Humor)',
  'answer': 'Relentless optimism',
  'placeholder': 'Surprise me'},
 {'question': 'What kind of activities or hobbies does the recipient enjoy? (e.g., Cooking, Hiking)',
  'answer': 'hiking, outdoor adventures',
  'placeholder': 'Surprise me'},
 {'question': 'Is there a special message or sentiment you wish to convey? (e.g., Congratulations, Thank you)',
  'answer': "Celebrating friend's birthday, admire their optimism and love for outdoor adventures.",
  'placeholder': 'Surprise me'},
 {'question': "Share a memorable experience or moment you've had with the recipient. (e.g., A surprise party)",
  'answer': 'got lost during a hike, discovered hidden waterfall',
  'placeholder': 'Surprise me'}]
for i, q in enumerate(refined_input):
    

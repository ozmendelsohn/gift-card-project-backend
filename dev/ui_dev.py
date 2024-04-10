# %%
import panel as pn
import requests

app = pn.template.MaterialTemplate(title='GenAI App')
# %%
recipient_info = pn.widgets.TextAreaInput(value="""I'm celebrating my best friend's birthday. We've been close since college, always sharing our love for hiking and 
outdoor adventures. One time, we got lost during a hike but ended up finding this beautiful, hidden waterfall, which is 
now our favorite spot. What I admire most about them is their relentless optimism, even in tough situations. 
They always find a way to smile and lift everyone's spirits.""", 
name='Recipient Info',
width=500, height=200)
post_info_button = pn.widgets.Button(name='Post Info', button_type='primary')
# %%
# @app.post("/info", response_model=List[QuestionAnswer])
# async def post_info(recipient_info: RecipientInfo):
#     ...
refined_input_template =  [
{'question': 'What is your relationship with the recipient? (e.g., Family member, Colleague)',
  'answer': 'best friend'},
 {'question': 'What kind of activities or hobbies does the recipient enjoy? (e.g., Cooking, Hiking)',
  'answer': 'hiking, outdoor adventures'},
 {'question': "Share a memorable experience or moment you've had with the recipient. (e.g., A surprise party)",
  'answer': 'Getting lost and discovering a hidden waterfall'}]
refined_input = pn.Column(*[pn.widgets.TextInput(value=ri['answer'], 
                                                 name=ri['question']) for ri in refined_input_template])
post_refine_button = pn.widgets.Button(name='Post Refine', button_type='primary')

def update_refined_input(event):
    print('Refined Input:', recipient_info.value)
    response = requests.post("http://localhost:8000/info",
                             json={"recipient_info": recipient_info.value})
    refined_input.objects = []
    for qa in response.json():
        refined_input.append(pn.widgets.TextInput(value=qa['answer'], name=qa['question']))
    print('Refined Input:', response.json())
post_info_button.on_click(update_refined_input)
# %%
# @app.post("/refine", response_model=EmailContent)
# async def post_refine(refined_input: List[RefineInput]):
#     ...

email_json =  {'email_title': ' Title: "Reminiscing Our Adventure: A Letter of Friendship and Gratitude"',
 'email_content': " Dear [Best Friend's Name],\n\nAs I sit down to pen this letter, I can't help but smile as I remember our adventure in the woods that led us to discovering a hidden waterfall. The thrill of getting lost together, the excitement in our voices as we heard the sound of rushing water growing louder, and the sense of accomplishment when we finally arrived at this breathtaking sight - it's memories like these that make our bond so strong.\n\nMay our friendship continue to lead us on many more adventures, both big and small. Here's to creating new memories and cherishing the old ones. I'm grateful for every moment we spend together, hiking through life's beautiful trails.\n\nWith love and appreciation,\n\n[Your Name]",
 'email_image': 'base64_image_data',
 "email_image_prompt": "I'm celebrating my best friend's birthday. We've been close since college, always sharing our love for hiking and outdoor adventures. One time, we got lost during a hike but ended up finding this beautiful, hidden waterfall, which is now our favorite spot. What I admire most about them is their relentless optimism, even in tough situations. They always find a way to smile and lift everyone's spirits."}
email_html_str = """
<h1>{email_title}</h1>
<p>{email_content}</p>
<img src="data:image/png;base64,{email_image}"/>
<p>{email_image_prompt}</p>
"""
email_html = pn.pane.HTML(email_html_str.format(**email_json))

def update_email_html(event):
    print('Refined Input:', refined_input.objects)
    refined_input_dict = [{"question": str(ri.name), "answer": str(ri.value)} for ri in refined_input.objects]
    response = requests.post("http://localhost:8000/refine",
                             json=refined_input_dict)
    email_html.object = ''
    email_html.object = email_html_str.format(**response.json())
    print('Email HTML:', response.json())
    
post_refine_button.on_click(update_email_html)
# %%

app.main.append(recipient_info)
app.main.append(post_info_button)
app.main.append(pn.Spacer(height=20))
app.main.append(refined_input)
app.main.append(post_refine_button)
app.main.append(pn.Spacer(height=20))
app.main.append(email_html)
app.servable()


# %%
# Create an example prompt:
"""
I am looking to send a gift card to my coworker who just give birth to her first born daughter. She is a very quiet 
and nice person. We just starting to share an office together and I enjoy her company. She work as data scientist like
me and we like to talk about theoretical staff together."""

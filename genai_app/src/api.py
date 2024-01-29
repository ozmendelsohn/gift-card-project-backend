from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import yaml
import os

from text_processing import CardTypeLabeler, QuestionRetriver, QuestionAnswerGenerator

CONFIG_PATH = '/home/oz/projects/gift-card-genai/genai_app/config' # TODO: define what it the correct way to access the config file

app = FastAPI()

# Define Pydantic models for request and response payloads
class RecipientInfo(BaseModel):
    recipient_info: str

class QuestionAnswer(BaseModel):
    question: str
    answer: str
    placeholder: Optional[str] = None

class RefineInput(BaseModel):
    question: str
    answer: str

class EmailContent(BaseModel):
    email_title: str
    email_content: str
    email_image: str  # Assuming base64_image_data is a string

# Screen 1 Endpoints
@app.post("/info", response_model=List[QuestionAnswer])
async def post_info(recipient_info: RecipientInfo):
    # Get what is the type of card to generate
    card_type = CardTypeLabeler().label_card_type(recipient_info.recipient_info)
    # Get the questions to ask # TODO: define what it the correct way to access the config file
    questions = QuestionRetriver().retrieve_questions(card_type)
    # Generate the answers
    llm_config = yaml.safe_load(open(os.path.join(CONFIG_PATH, 'llm.yaml')))
    questions_answers_generator = QuestionAnswerGenerator(llm_config['ollama_phi'])
    questions_answers = questions_answers_generator.generate_answers(questions, recipient_info.recipient_info)
    
    # This function would typically interact with a service or database
    # questions_answers = [  # Example response
    #     {"question": "What is your connection?", "answer": "Friend", "placeholder": "Friend"},
    #     {"question": "What is the recipient's hobbies?", "answer": "Hiking", "placeholder": "Not sure"},
    #     {"question": "Tell a funny and light-hearted story about the recipient.", "answer": "He is a funny guy.", "placeholder": "Suprise me"},
    # ]
    return questions_answers


# Screen 2 Endpoints

@app.post("/refine", response_model=EmailContent)
async def post_refine(refined_input: List[RefineInput]):
    # Process the refined input, generate email content and image
    # This function may involve calling other internal services or utilities
    email_title = "Generated Email Title"
    email_content = "Generated email content based on user's answers."
    email_image = "base64_encoded_image_data"
    return {"email_title": email_title, "email_content": email_content, "email_image": email_image}


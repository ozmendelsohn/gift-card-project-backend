from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
import json
import os
from utils import load_config

from text_processing import CardTypeLabeler, QuestionRetriver, QuestionAnswerGenerator, EmailComposer

chosen_model = 'groq_mixtral'
TRACKING = True
if TRACKING:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = json.load(open('../secrets.json'))['langsmith_api_key']
    os.environ["LANGCHAIN_PROJECT"] = "Gift-Card-Gen-AI"
app = FastAPI()

# Define Pydantic models for request and response payloads
class RecipientInfo(BaseModel):
    recipient_info: str

class QuestionAnswer(BaseModel):
    question: str
    answer: str

class RefineInput(BaseModel):
    question: str
    answer: str

class EmailContent(BaseModel):
    email_title: str
    email_content: str
    email_image: str  # Assuming base64_image_data is a string
    email_image_prompt: str

# Screen 1 Endpoints
@app.post("/info", response_model=List[QuestionAnswer])
async def post_info(recipient_info: RecipientInfo):
    # Get what is the type of card to generate
    card_type = CardTypeLabeler().label_card_type(recipient_info.recipient_info)
    # Get the questions to ask 
    questions = QuestionRetriver().retrieve_questions(card_type)
    # Generate the answers # TODO: define what it the correct way to access the config file
    llm_config = load_config('llm')
    questions_answers_generator = QuestionAnswerGenerator(llm_config[chosen_model])
    questions_answers = questions_answers_generator.generate_answers(questions=questions, 
                                                                     recipient_info = recipient_info.recipient_info)
    return questions_answers


# Screen 2 Endpoints

@app.post("/refine", response_model=EmailContent)
async def post_refine(refined_input: List[RefineInput]):
    # Process the refined input, generate email content and image
    # This function may involve calling other internal services or utilities
    llm_config = load_config('llm')
    email_composer = EmailComposer(llm_config[chosen_model])
    # convert the refined input to dict
    refined_input = [r.dict() for r in refined_input]
    email_content = email_composer.compose_email(refined_input)
    email_title = email_composer.compose_email_title(email_content)
    email_image_promnt = email_composer.compose_email_image_prompt(email_content)
    image_base64 = email_composer.generate_image(email_image_promnt)
    return {"email_title": email_title,
            "email_content": email_content, 
            "email_image": image_base64,
            "email_image_prompt": email_image_promnt}


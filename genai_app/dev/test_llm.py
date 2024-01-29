from pydantic import BaseModel
from typing import List, Optional
import yaml
import os
from text_processing import CardTypeLabeler, QuestionRetriver, QuestionAnswerGenerator

CONFIG_PATH = '/home/oz/projects/gift-card-genai/genai_app/config' # TODO: define what it the correct way to access the config file

recipient_info = """
I'm celebrating my best friend's birthday. We've been close since college, always sharing our love for hiking and outdoor adventures. One time, we got lost during a hike but ended up finding this beautiful, hidden waterfall, which is now our favorite spot. What I admire most about them is their relentless optimism, even in tough situations. They always find a way to smile and lift everyone's spirits.
"""
CardTypeLabeler().label_card_type('')
card_type = CardTypeLabeler().label_card_type('')
questions = QuestionRetriver().retrieve_questions(card_type)
llm_config = yaml.safe_load(open(os.path.join(CONFIG_PATH, 'llm.yaml')))
questions_answers_generator = QuestionAnswerGenerator(llm_config['ollama_phi'])
questions_answers_generator.generate_answers(questions=questions, recipient_info=recipient_info)
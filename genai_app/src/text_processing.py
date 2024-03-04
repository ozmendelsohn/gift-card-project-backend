import os
from utils import load_config
from llm import (get_llm, get_questions_template, get_email_content_template, 
                 get_email_title_template, get_email_image_prompt_template)
from langchain_core.output_parsers import JsonOutputParser
import json
import requests


# TODO: define what it the correct way to access the config file
QUESTION_CONFIG = 'questions'


class CardTypeLabeler:
    """
    This class is used to determine the type of card to generate based on the recipient's info and the available card
    types in the config file

    Attributes
    ----------
    recipient_info : str
        The recipient's info
    config : dict
        The config file containing the available card types and their corresponding keywords
    card_type : str

    """

    def load_questions(self) -> dict:
        """
        Load the questions from the config file.

        Returns
        -------
        dict
            The config file containing the available card types and their corresponding keywords
        """
   
        return load_config(QUESTION_CONFIG)

    def label_card_type(self, recipient_info: str) -> str:
        """
        Determine the type of card based on the recipient's info and the available card types in the config file.

        Parameters
        ----------
        recipient_info : str
            The recipient's info

        Returns
        -------
        str
            The type of card to generate
        """
        self.config = self.load_questions()
        card_typs = self.config.keys()
        # TODO: add logic to determine the card type based on the recipient's info and the available card types in the config file
        return 'generic_occasion'


class QuestionRetriver:
    """
    This class is used to retrieve the questions from the config file based on the card type.

    Attributes
    ----------
    card_type : str
        The type of card to generate
    config : dict
        The config file containing the available card types and their corresponding keywords
    questions : list
        The list of questions to ask

    """

    def load_questions(self) -> dict:
        """
        Load the questions from the config file.

        Returns
        -------
        dict
            The config file containing the available card types and their corresponding keywords
        """
        return load_config(QUESTION_CONFIG)

    def retrieve_questions(self, card_type: str) -> list:
        """
        Retrieve the questions from the config file based on the card type.

        Parameters
        ----------
        card_type : str
            The type of card to generate

        Returns
        -------
        list
            The list of questions to ask
        """
        self.config = self.load_questions()
        return self.config[card_type]['questions']

# Create QuestionAnswerGenerator class
# This class is used to generate the answers to the questions based on the recipient_info and the questions


class QuestionAnswerGenerator:
    """
    This class is used to generate the answers to the questions based on the recipient_info and the questions.

    Attributes
    ----------
    recipient_info : str
        The recipient's info
    questions : list
        The list of questions to ask
    answers : list
        The list of answers to the questions

    """
    answer_format = '{"answer": <answer>}'
    
    def __init__(self: str, llm_config: dict):
        """
        Initialize the QuestionAnswerGenerator class.
        """
        self.llm = get_llm(llm_config)

    def generate_answers(self, recipient_info, questions: list) -> list:
        """
        Generate the answers to the questions based on the recipient_info and the questions.

        Parameters
        ----------
        recipient_info : str
            The recipient's info
        
        questions : list
            The list of questions to ask

        Returns
        -------
        list
            The list of answers to the questions
        """
        chain = self.llm | JsonOutputParser()
        for i, question in enumerate(questions):
            messages = get_questions_template( recipient_info=recipient_info,
                                               question=question['question'],
                                               answer_format=self.answer_format)
            answer = chain.invoke(messages)['answer']
            answer = ', '.join(answer) if isinstance(answer, list) else answer
            if answer == '':
                answer = question.get('placeholder', None)
            questions[i]['answer'] = answer
        
        # drop the placeholder key
        questions = [ {k: v for k, v in q.items() if k != 'placeholder'} for q in questions]
        return questions
    
# Create EmailComposer class
# This class is used to compose the email content and image based on the refined input from the user
class EmailComposer:
    """
    This class is used to compose the email content and image based on the refined input from the user.

    Attributes
    ----------
    llm : str
        The LLM model
    email_title : str
        The title of the email
    email_content : str
        The content of the email
    email_image : str
        The image of the email

    """
    def __init__(self: str, llm_config: dict):
        """
        Initialize the EmailComposer class.
        """
        self.llm = get_llm(llm_config)

    def compose_email(self, refined_input: list) -> str:
        """
        Compose the email content based on the refined input from the user.

        Parameters
        ----------
        refined_input : list
            The refined input from the user

        Returns
        -------
        str
            The content of the email
        """
        chain = self.llm
        messages = get_email_content_template(refined_input)
        email_content = chain.invoke(messages).content
        return email_content
    
    def compose_email_title(self, email_content: str) -> str:
        """
        Compose the title of the email based on the content of the email.

        Parameters
        ----------
        email_content : str
            The content of the email

        Returns
        -------
        str
            The title of the email
        """
        chain = self.llm
        messages = get_email_title_template(email_content)
        email_title = chain.invoke(messages).content
        return email_title
    
    def compose_email_image_prompt(self, email_content: str) -> str:
        """
        Compose the image prompt of the email based on the content of the email.

        Parameters
        ----------
        email_content : str
            The content of the email

        Returns
        -------
        str
            The image prompt of the email
        """
        chain = self.llm
        messages = get_email_image_prompt_template(email_content)
        email_image_prompt = chain.invoke(messages).content
        return email_image_prompt
    
    def generate_image(self, email_image_prompt: str) -> str:
        """
        Generate the image of the email based on the image prompt.

        Parameters
        ----------
        email_image_prompt : str
            The image prompt of the email

        Returns
        -------
        str
            The image of the email
        """
        # %%
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {json.load(open('../secrets.json'))['openai_api_key']}"
        }
        data = {
            "model": "dall-e-3",
            "prompt": email_image_prompt,
            "response_format": "b64_json",
            "n": 1,
            "size": "1024x1024"
        }

        response = requests.post(url, headers=headers, json=data)
        base64_image_data = response.json()['data'][0]['b64_json']
        
        return base64_image_data
    
    

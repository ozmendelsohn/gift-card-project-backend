import os
import yaml
from llm import get_llm, get_questions_template
from langchain_core.output_parsers import StrOutputParser

# TODO: define what it the correct way to access the config file
CONFIG_PATH = '/home/oz/projects/gift-card-genai/genai_app/config'


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
        with open(os.path.join(CONFIG_PATH, 'questions.yaml')) as f:
            config = yaml.safe_load(f)
        return config

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
        with open(os.path.join(CONFIG_PATH, 'questions.yaml')) as f:
            config = yaml.safe_load(f)
        return config

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
        return self.config[card_type]

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
        questions : list
            The list of questions to ask

        Returns
        -------
        list
            The list of answers to the questions
        """
        prompt = get_questions_template()
        chain = prompt | self.llm | StrOutputParser()
        for i, question in enumerate(questions['questions']):
            answer = chain.invoke({'recipient_info': recipient_info, 'question': question})
            questions['questions'][i]['answer'] = answer
        return questions

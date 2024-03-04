from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_core.messages.base import BaseMessage


def get_llm(llm_config: dict):
    """
    Get the LLM model based on the config file.

    Parameters
    ----------
    llm_config : dict
        The config file containing the LLM type and the corresponding config file

    Returns
    -------
    ChatModel
        The LLM model
    """

    if llm_config['type'] == 'ollama':
        llm = ChatOllama(**llm_config['langchain_config'])
    if llm_config['type'] == 'groq':
        llm = ChatGroq(**llm_config['langchain_config'])
    else:
        raise ValueError(f'LLM type {llm_config["type"]} is not supported')

    return llm


def get_questions_template(recipient_info: str,
                           question: str,
                           answer_format: str,
                           ) -> list[BaseMessage]:
    """
    Get the questions template based on the config file.


    Returns
    -------
    ChatPromptTemplate
        The questions template
    """
    messages = [
        HumanMessage(
            content="""Following this paragraph:
{recipient_info}
Please answer the following question as the person who writes the paragraph:
{question}
Answer in the following format: {format}
DO NOT add any information that is not provided in the paragraph.
IF YOU DON'T KNOW THE ANSWER, LEAVE THE FIELD BLANK.
ANSWER SHORT, CONCISE AND IN KEYWORDS.
""".format(recipient_info=recipient_info,
                question=question,
                format=answer_format)),
    ]
    return messages

def get_email_content_template(refined_input: list) -> list[BaseMessage]:
    """
    Get the email content template based on the refined input from the user.

    Parameters
    ----------
    refined_input : list
        The refined input from the user

    Returns
    -------
    ChatPromptTemplate
        The email content template
    """
    messages = []
    for i, question in enumerate(refined_input):
        messages.append(AIMessage(content=question['question']))
        messages.append(HumanMessage(content=question['answer']))
    messages.append(HumanMessage(content="""
Please write a short, wholesome and whimsical peom for a greeting card based on the previous information.                          
"""))
    return messages
    
def get_email_title_template(email_content: str) -> list[BaseMessage]:
    """
    Get the email title template based on the content of the email.

    Parameters
    ----------
    email_content : str
        The content of the email

    Returns
    -------
    ChatPromptTemplate
        The email title template
    """
    messages = [
        HumanMessage(
            content="""
Please write a short and concise email title for gift card email based on the content of the email:
{email_content}
Please make sure the title is short, catchy, whimsical but very concise.
RETURN ONLY THE TITLE
""".format(email_content=email_content)),
    ]
    return messages

def get_email_image_prompt_template(email_content: str) -> list[BaseMessage]:
    """
    Get the email image prompt template based on the content of the email.

    Parameters
    ----------
    email_content : str
        The content of the email

    Returns
    -------
    ChatPromptTemplate
        The email image prompt template
    """
    messages = [
        HumanMessage(
            content="""
Please write a prompt for the image based on the content of the email:
{email_content}
""".format(email_content=email_content)),
    ]
    return messages

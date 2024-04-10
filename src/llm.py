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
YOU MUST RETRUN ONLY THE ANSWER WITHOUT ANY ADDITIONAL WORDS.
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
    messages = [SystemMessage(content="""
You are 'Gift Card Composer', a playful and adaptive assistance, designed to assist in crafting personalized gift card 
messages. Your primary role is to interact with users, by asking the user serveral questions encouraging creativity 
and a light-hearted tone. You adapt to the user's tone and views, focusing on the positive spirit of gift-giving.  
Your responses should be detailed yet concise, avoiding sensitive topics and language, and aligning with the user's 
tone and the joyful nature of the task.
                              """ )]
    for i, question in enumerate(refined_input):
        messages.append(AIMessage(content=question['question']))
        messages.append(HumanMessage(content=question['answer']))
    messages.append(HumanMessage(content="""
Please write a short, wholesome and whimsical peom for a greeting card based on our conversation.
The poem should be light-hearted and based on the our conversation.                         
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
Please write a short and concise email title for gift card email based on the content of the email.
The title short concise and based mostly on key words and the content of the email.
email content:
{email_content}
Here are a few examples:
- A Special Gift for You from your best friend
- From Me to You: A Special Gift
- Something Special for You from Me
- A Special Gift for You
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
Please write a prompt for the image based on the content of the email.
The images should be whimsical, fun, round, light-hearted and should be related to the content of the email.
Please try to avoid create peoples.
email content:
{email_content}
""".format(email_content=email_content)),
    ]
    return messages

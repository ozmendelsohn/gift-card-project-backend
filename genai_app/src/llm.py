from langchain_community.chat_models import ChatOllama
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
ANSWER SHORT, CONCISE AND IN KEYWORDS.
If you are not sure about the answer, please write \"Not sure\"
""".format(recipient_info=recipient_info,
                question=question,
                format=answer_format)),
    ]
    return messages

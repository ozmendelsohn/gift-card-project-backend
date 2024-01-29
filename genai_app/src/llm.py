from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage


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

def get_questions_template() -> ChatPromptTemplate:
    """
    Get the questions template based on the config file.

        
    Returns
    -------
    ChatPromptTemplate
        The questions template
    """
    messages = [
        SystemMessage(
            content="""
You are helpfull assistant. Please answer short and concise answers to the following questions. 
DO NOT add any information that is not provided in the paragraph.
If you are not sure about the answer, please write \"Not sure\"
"""),
        HumanMessage(
            content="""
Please answer the following questions using the following paragraph as a reference.
Paragraph:
{recipient_info}
question:
{question}
"""),
    ] 
    return  ChatPromptTemplate.from_messages(messages)
    
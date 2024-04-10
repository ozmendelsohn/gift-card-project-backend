from llm import get_llm
import yaml
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser


CONFIG_PATH = '/home/oz/projects/gift-card-genai/genai_app/config' # TODO: define what it the correct way to access the config file

recipient_info = """
I'm celebrating my best friend's birthday. We've been close since college, always sharing our love for hiking and outdoor adventures. One time, we got lost during a hike but ended up finding this beautiful, hidden waterfall, which is now our favorite spot. What I admire most about them is their relentless optimism, even in tough situations. They always find a way to smile and lift everyone's spirits.
"""
question = "What is your relationship with the recipient?"

answer_format = '{"answer": <answer>}'

llm_config = yaml.safe_load(open(os.path.join(CONFIG_PATH, 'llm.yaml')))
llm = get_llm(llm_config['ollama_mistral'])

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
""".format(recipient_info=recipient_info, question=question, format=answer_format)),
    ] 
print(messages[0].content)

chain = llm | JsonOutputParser()

answer = chain.invoke(messages,
                      config=dict(max_tokens=100))
print(answer)
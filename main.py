from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

from negocio_info import store_data

template = """"
Answer the question below in Spanish.

Here is the business information:
{negocio_info}

{context}

Question: {question}

Answer:

"""

model = OllamaLLM(model="llama3.2:1b")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model


def chat():
    print("Welcome to the chatbot")
    context = ""
    while True:
        question = input("You:")
        if question == "stop":
            break

        result = chain.invoke(
            {"negocio_info": store_data, "context": context, "question": question}
        )
        print("Bot:", result)
        context += f"Bot:{result}\nYou:{question}\n"


if __name__ == "__main__":
    chat()

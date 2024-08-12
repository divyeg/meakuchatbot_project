import panel as pn
import ollama
from uuid import uuid4
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.llms import Ollama
from langchain_ollama import ChatOllama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

pn.config.theme = "dark"
pn.extension(design="material")

CHROMA_PATH = "input_data/chroma"

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

TEMPLATE = """You are a helpful assistance for HackerEarth company. \
You first greet the customer in one line then collect their details such as name, email, contact number. \
You wait for the customer to respond then respond using the following context. \
{context_text} \
Answer the question using above context and donot repeat anything. \
You job is to engage customer asking about what are they looking for on the website so ask questions after responding. \
You respond in a short, very conversational friendly style. \
The company is about provide Human Resource services to their customers, the services include \
1. Repository of pre-built questions \
2. Assess a large pool of candidates in 38 different programming languages \
3. Versatile platform \
4. Advanced proctoring settings for assessments \
5. Detailed reports and analytics \
6. Dedicated account manager and product specialist available 24/7 \
7. Evaluates tests automatically to shortlist the best candidates \
If they are not looking for anything specific, you provide them details about what the company does and how its products can benefit the customer, \

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(TEMPLATE)


def get_chain(callbacks):
    retriever = db.as_retriever(callbacks=callbacks)
    model = ChatOllama(model="qwen:1.8b", temperature=0, callbacks=callbacks)

    def format_docs(docs):
        text = "\n\n".join([d.page_content for d in docs])
        return text

    def hack(docs):
        # https://github.com/langchain-ai/langchain/issues/7290
        for callback in callbacks:
            callback.on_retriever_end(docs, run_id=uuid4())
        return docs

    return (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | model
    )


async def callback(contents, user, instance):
    callback_handler = pn.chat.langchain.PanelCallbackHandler(instance)
    chain = get_chain(callbacks=[callback_handler])
    response = await chain.ainvoke(contents)
    return response.content


chat_interface = pn.chat.ChatInterface(callback=callback)

chat_interface.send(
    "Hi! How can i help you?", user="System", avatar="🤖", respond=False
)

chatbot = pn.Column(
    pn.pane.Markdown("# Qwen:1.8b Chatbot"),
    chat_interface,
    styles={
        "padding": "15px",
        "border": "1px solid white",
    },
)

chatbot.servable()

# llm = Ollama(model="qwen:1.8b")

# chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())


# def generate_response(contents: str, user: str, chat_interface: pn.chat.ChatInterface):
#     chat_history = chat_interface.serialize(
#         format="transformers",
#     )
#     response = ollama.chat(model=chain, stream=True, messages=chat_history)
#     message = ""
#     for partial_resp in response:
#         token = partial_resp["message"]["content"]
#         message += token
#         yield message


# chat_interface = pn.chat.ChatInterface(callback=generate_response)
# chat_interface.send(
#     "Hi! How can i help you?", user="System", avatar="🤖", respond=False
# )

# chatbot = pn.Column(
#     pn.pane.Markdown("# Qwen:1.8b Chatbot"),
#     chat_interface,
#     styles={
#         "padding": "15px",
#         "border": "1px solid white",
#     },
# )

# chatbot.servable()

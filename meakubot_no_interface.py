from langchain.chains import RetrievalQA
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# from langchain_text_splitters import CharacterTextSplitter

CHROMA_PATH = "input_data/chroma"

# loader = UnstructuredFileLoader("ai_adoption_framework_whitepaper.pdf")
# docs = loader.load()

# text_splitter = CharacterTextSplitter(
#     separator="\n", chunk_size=2000, chunk_overlap=200
# )
# texts = text_splitter.split_documents(docs)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)

llm = Ollama(model="qwen:1.8b")

chain = RetrievalQA.from_chain_type(llm, retriever=db.as_retriever())

question = "What are the advantages of using HackerEarth?"
result = chain.invoke({"query": question})

print(result["result"])

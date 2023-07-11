import os
from PyPDF2 import PdfReader 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticVectorSearch,Pinecone,Weaviate,FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_text_file_content(txt_files):
    text = ""
    for txt_file in txt_files:
        with open(txt_file, 'r') as file:
            text += file.read()
    return text

def get_text_chunks(raw_text):
    splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap = 100,
        length_function = len
    )
    chunks = splitter.split_text(raw_text)
    return chunks

def get_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts = chunks, embedding = embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(memory_key="ChatHistory",return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm,retriever=vectorstore.as_retriever(),memory=memory)
    return conversation_chain


def main():
    txt_files = ["testdoc.txt"]
    raw_text = get_text_file_content(txt_files)
    chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorstore(chunks)
    conversation_chain = get_conversation_chain(vectorstore)
    query = "What are some of Rehaan Raha's funniest escapades?"
    chat_history = [] # Add this line if there's no chat history yet.
    conversation_chain.run(chat_history=chat_history, question=query)
    
main()

# -*- coding: utf-8 -*-
"""ReverseEngineeringAssistantV2.0_RAG_PDF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18qjhyE5yfnfGaSdYTUyIlu7GmHCtgiFH

#Reverse Engineering Assistant V2.0
"""

!pip install langchain langchain_community langchain_chroma langchain-openai langchainhub unstructured[pdf]

import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass()

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

#Using the UnstructuredPDFLoader for loading the document
from langchain_community.document_loaders import UnstructuredPDFLoader

#Create the loader
loader = UnstructuredPDFLoader("/content/drive/MyDrive/Book PDFs/Hacking APIs - HackingAPIs.pdf")

#Get the loaded data
data = loader.load()

#Importing the needed libraries
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain import hub
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

#Splitting the data and creating a vectorestore
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

#Retrieving and generating using the relevant data from the pdf.
retriever = vectorstore.as_retriever()
prompt = hub.pull("byteberzerker/reverse_helper")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("Give me some SQL examples used in fuzzing APIs.")

#Addind Memory
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True, output_key='answer')




# Create the multipurpose chain
qachat = ConversationalRetrievalChain.from_llm(
    llm=ChatOpenAI(temperature=0),
    memory=memory,
    retriever=retriever,
    combine_docs_chain_kwargs={"prompt": prompt}

)

user_question = input("Please enter your question: ")

# Invoke the chain with the user question
response = qachat({"question": user_question})

# Extract and print the AI response content
ai_response_content = response['answer']
print(ai_response_content)

"""#With Nice Formatting"""

retriever = vectorstore.as_retriever()
prompt = hub.pull("byteberzerker/reverse_helper")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

result = rag_chain.invoke("Give me some SQL examples used in fuzzing APIs.")


# Function to print the result nicely
def print_nice_result(result):
    print("\n=== RAG Chain Result ===\n")
    sections = result.split("\n\n")
    for idx, section in enumerate(sections, start=1):
        print(f"Section {idx}:\n{section.strip()}\n")
        print("=" * 40)

# Print the nicely formatted result
print_nice_result(result)
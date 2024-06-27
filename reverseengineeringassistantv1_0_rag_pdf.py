# -*- coding: utf-8 -*-
"""ReverseEngineeringAssistantV1.0_RAG_PDF.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/18qjhyE5yfnfGaSdYTUyIlu7GmHCtgiFH

#Reverse Engineering Assistant V1.0
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
loader = UnstructuredPDFLoader("/content/Reverse Engineering PDF.pdf")

#Get the loaded data
data = loader.load()



#Importing the needed libraries
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain import hub

#Splitting the data and creating a vectorestore
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

#Retrieving and generating using the relevant data from the pdf.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

rag_chain.invoke("What are some common techniques to reverse engineer a windows executable?")


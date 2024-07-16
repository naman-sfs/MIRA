import os
from langchain_community.document_loaders import PyPDFLoader
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

MONGODB_ATLAS_CLUSTER_URI = os.getenv('MONGODB_ATLAS_CLUSTER_URI')
DB_NAME = os.getenv('DB_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')


def train_mira(file_location):    
    try:
        # initialize MongoDB python client
        client = MongoClient(MONGODB_ATLAS_CLUSTER_URI)
        MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]
        
        embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
        
        loader = PyPDFLoader(f'./{file_location}')
        documents = loader.load_and_split()
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200, add_start_index = True)
        chunks = text_splitter.split_documents(documents)

        vector_search = MongoDBAtlasVectorSearch.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection=MONGODB_COLLECTION
        )
        
        return True
    
    except:
        return False
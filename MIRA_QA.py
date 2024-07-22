import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from database import vector_search
from prompt import template, passage_template

load_dotenv()

os.environ['LANGCHAIN_TRACING_V2'] = 'true'
os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'

os.environ["LANGCHAIN_PROJECT"]= os.getenv('LANGCHAIN_PROJECT')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
os.environ["GOOGLE_API_KEY"] = os.getenv('GOOGLE_API_KEY')
os.environ["LANGCHAIN_API_KEY"] = os.getenv('LANGCHAIN_API_KEY')

class MIRA:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(model='text-embedding-ada-002'),
        self.llm = ChatOpenAI(model="gpt-3.5-turbo"),
        
    # retrieve the similar chunks using HyDE method
    def retrieve_documents_HYDE(self,query:str):
        # prompt for HyDE
        prompt_hyde = ChatPromptTemplate.from_template(passage_template)

        # chain for HyDE paper generation
        generate_docs_for_retrieval = (
            prompt_hyde | ChatOpenAI(model="gpt-3.5-turbo", temperature=0) | StrOutputParser() 
        )
        
        # combine the chain for HyDE and retrieval and return the retrieved chunks
        retrieval_chain = generate_docs_for_retrieval | vector_search.as_retriever(search_type='similarity',search_kwargs={"k":6})
        retireved_docs = retrieval_chain.invoke({"question":query})
        
        return retireved_docs
    

    # generate the answer using query
    def ask_query(self,query:str,retrieved_docs):
        # prompt for final answer generation
        prompt = ChatPromptTemplate.from_template(template)

        # Generative chain
        final_rag_chain = (
            prompt
            | ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
            | StrOutputParser()
        )

        # invoke the final chain
        answer = final_rag_chain.invoke({"context":retrieved_docs,"question":query})
        
        return answer
    
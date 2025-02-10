#Ths section declares the embediing model and LLM model to re-use it when we build the index and the agent

from dotenv import load_dotenv
import os
from llama_index.embeddings.openai import OpenAIEmbedding, OpenAIEmbeddingModelType
from llama_index.llms.openai import OpenAI


load_dotenv() # load the environment variables from the .env file

openai_api_key = os.getenv('OPENAI_API_KEY') # get the openai api key from the environment variables
embed_model = OpenAIEmbedding(
    api_key = openai_api_key, model = OpenAIEmbeddingModelType.TEXT_EMBED_3_LARGE) # create an instance of the embedding model(OpenAIEmbedding class)
llm_model = OpenAI(api_key = openai_api_key, model = 'gpt-4o-mini') # create an instance of the llm model(OpenAI class)
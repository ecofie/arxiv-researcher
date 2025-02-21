import streamlit as st

from agent import Agent
from index_manager import IndexManager
from constant import embed_model,llm_model
from index_manager_pinecone import IndexManagerPinecone

#use a decorator to cache the function output
@st.cache_resource   #decorator
def initialize_agent():
    #index_manager = IndexManager(embed_model) #used when the index in store locally 
    index_manager = IndexManagerPinecone(embed_model,index_name = "arxiv-research") #used when the index is stored in the pinecone cloud storage
    index = index_manager.retreive_index()
    return Agent(index,llm_model)

#initialise the agent and the session state
if "agent" not in st.session_state:
    st.session_state.agent = initialize_agent()

#initialize the message
if "message" not in st.session_state:
    st.session_state.message = []

st.title("Research Paper Chatbot")
    
#Display chat messages
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input("Ask me anything about research paper:"):
    st.session_state.message.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer= st.session_state.agent.chat(prompt).response
            st.markdown(answer)
            st.session_state.message.append({"role":"assistant","content":answer})
            
            
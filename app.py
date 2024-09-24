import streamlit as st
import openai
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Tracking the prompts using Langsmith
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A Chatbot With OpenAI"

# Prompt template 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user's queries."),
        ("user", "Question: {question}")
    ]
)

# Function to generate the response
def generate_response(llm_model, api_key, temperature, max_tokens, question):
    openai.api_key = api_key
    llm = ChatOpenAI(model=llm_model, temperature=temperature, max_tokens=max_tokens)
    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    answer = chain.invoke({'question': question})
    return answer

# Title of the APP
st.title("Enhanced Q&A Chatbot With OpenAI")

# Sidebar settings
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")

# Select the OpenAI model
llm_model = st.sidebar.selectbox("Select OpenAI model", ["gpt-4-turbo", "gpt-4"])

# Adjust response temperature and max tokens
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=300, value=150)

# Main interface for user inputs
st.write("Ask any question you have:")
user_input = st.text_input("Question:")

# Check if API key and user input are provided
if user_input and api_key:
    answer = generate_response(llm_model, api_key, temperature, max_tokens, user_input)
    st.write(answer)
elif not api_key:
    st.warning("Please enter the OpenAI API Key in the sidebar.")
else:
    st.write("Please provide a question to proceed.")

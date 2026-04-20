import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Env variables load karne ke liye
load_dotenv()

st.set_page_config(page_title="Logistics AI Agent", layout="wide")
st.title("🤖 Logistics Agentic AI Assistant")

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Opps! .env file mein GROQ_API_KEY nahi mili.")
else:
    # Model Setup
    llm = ChatGroq(
        temperature=0.3, 
        model_name="llama-3.1-8b-instant", 
        groq_api_key=groq_api_key
    )

    # Agent Definition
    researcher = Agent(
        role='Logistics Researcher',
        goal='Provide expert analysis on shipping and supply chain queries',
        backstory='You are a veteran logistics consultant with 20 years of experience.',
        llm=llm,
        verbose=True
    )

    query = st.text_input("Apna logistics sawal yahan likhein:", "Best shipping route from India to USA?")

    if st.button("Ask AI Team"):
        with st.spinner("Agents kaam kar rahe hain..."):
            task = Task(
                description=query,
                agent=researcher,
                expected_output="A detailed bullet-point report."
            )
            crew = Crew(agents=[researcher], tasks=[task])
            result = crew.kickoff()
            st.subheader("Results:")
            st.write(result.raw)
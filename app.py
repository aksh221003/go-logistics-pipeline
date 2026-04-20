import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
import os
from dotenv import load_dotenv

# Environment variables load karo
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Logistics AI Agent", layout="wide")
st.title("🤖 Logistics Agentic AI Assistant")

# API Key check
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Opps! .env file mein GROQ_API_KEY nahi mili. Please check karein.")
else:
    # 1. NEW WAY: CrewAI's Native LLM Setup (No Langchain needed)
    groq_llm = LLM(
        model="groq/llama-3.1-8b-instant",
        api_key=groq_api_key,
        temperature=0.2
    )

    # 2. Agent Definition
    researcher = Agent(
        role='Logistics Strategy Expert',
        goal='Provide accurate and detailed analysis for shipping, supply chain, and route optimization queries.',
        backstory='''You are a veteran logistics consultant with 20 years of experience. 
        You specialize in reducing costs and improving delivery timelines globally.''',
        llm=groq_llm, # <--- Direct CrewAI LLM
        verbose=True,
        allow_delegation=False
    )

    # UI Input
    user_query = st.text_input("Apna logistics sawal yahan likhein:", "Best shipping route from India to USA?")

    if st.button("Ask AI Team"):
        if user_query:
            with st.spinner("Agents brainstorming kar rahe hain... (isme 10-15 seconds lag sakte hain)"):
                try:
                    # 3. Task Definition
                    analysis_task = Task(
                        description=f"Analyze the following query and provide a professional recommendation: {user_query}",
                        agent=researcher,
                        expected_output="A comprehensive report with bullet points, covering costs, routes, and estimated time."
                    )

                    # 4. Crew Formation
                    logistics_crew = Crew(
                        agents=[researcher],
                        tasks=[analysis_task],
                        process=Process.sequential
                    )

                    # Execution
                    result = logistics_crew.kickoff()

                    # Result Display
                    st.success("Analysis Complete!")
                    st.subheader("Results:")
                    st.markdown(result.raw)

                except Exception as e:
                    st.error(f"Ek naya error aaya hai: {str(e)}")
        else:
            st.warning("Please kuch sawal toh likho!")

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Powered by CrewAI Native LLM & Groq")
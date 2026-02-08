import streamlit as st
import pandas as pd
from groq import Groq
from agents.manager import manager_agent
from agents.worker import worker_agent

st.set_page_config(page_title="Agentic Data Cleaner", page_icon="🧹", layout="wide")

if "cleaned_df" not in st.session_state:
    st.session_state.cleaned_df = None
if "cleaning_plan" not in st.session_state:
    st.session_state.cleaning_plan = None


st.sidebar.header("🔌 Configuration")
api_key = st.sidebar.text_input("Groq API Key", type="password")
model_select = st.sidebar.selectbox("Model", ["llama-3.3-70b-versatile"])


st.title("🤖 Autonomous Data Cleaning")

uploaded_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file and api_key:
    client = Groq(api_key=api_key)
    
    # Load Data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
        
    st.subheader("1. Raw Data Inspection")
    st.dataframe(df.head())

    # Planning out Data Cleaning Steps with Manager Agent
    if st.button("🧠 Analyze & Plan Strategy"):
        with st.spinner("Manager Agent is analyzing data patterns..."):
            plan_response = manager_agent(df, client, model_select)
            
            if "error" in plan_response:
                st.error(f"❌ Planning Failed: {plan_response['error']}")
                st.stop()
            
            if not plan_response.get('steps'):
                st.error("❌ Agent could not identify any cleaning steps.")
                st.stop()
                
            st.session_state.cleaning_plan = plan_response['steps']
            st.success("✅ Data Cleaning Plan Generated!")

    # Display Plan
    if st.session_state.cleaning_plan:
        st.subheader("2. Data Cleaning Plan")
        for i, step in enumerate(st.session_state.cleaning_plan):
            st.write(f"**Step {i+1}:** {step}")

        # Executing the data cleaning plan with Worker Agents
        if st.button("🚀 Execute Cleaning"):
            # Initialize Persistent environment - "Shared Memory"
            execution_env = {
                "df": df.copy(),
                "pd": pd,
                "__builtins__": __builtins__
            }
            
            progress_bar = st.progress(0)
            
            for index, step in enumerate(st.session_state.cleaning_plan):
                with st.expander(f"Processing Step {index+1}: {step}", expanded=True):
                    
                    max_retries = 3
                    success = False
                    error_msg = None
                    
                    for attempt in range(max_retries):
                        try:
                            # 1. Generate Code (pass error if retry)
                            code = worker_agent(execution_env['df'], step, client, model_select, error_msg)
                            if attempt == 0: st.code(code, language='python') 
                            
                            # 2. Execute in Persistent Env
                            exec(code, execution_env)
                            
                            st.success(f"✅ Applied successfully")
                            success = True

                            # Exit retry loop on success
                            break 
                        except Exception as e:
                            error_msg = str(e)
                            # st.warning(f"⚠️ Attempt {attempt+1} failed. Agent is self-correcting...")
                    
                    if not success:
                        st.error(f"❌ Step Failed after {max_retries} attempts: {error_msg}")
                        # We continue to next step instead of crashing whole app
                
                progress_bar.progress((index + 1) / len(st.session_state.cleaning_plan))

            st.session_state.cleaned_df = execution_env['df']
            st.success("🎉 All agents finished!")

    # Final Display and Download
    if st.session_state.cleaned_df is not None:
        st.subheader("3. Final Cleaned Dataset")
        st.dataframe(st.session_state.cleaned_df.head())
        
        csv_data = st.session_state.cleaned_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

elif not api_key:
    st.warning("Please enter your Groq API Key.")
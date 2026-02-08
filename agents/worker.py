

def worker_agent(df, task, client, model, error_history=None):
    """
    Generates Python code to execute a single data cleaning step.
    """
    data_sample = df.head(3).to_string()
    dtypes = df.dtypes.to_string()
    
    few_shot_examples = """
    Task: "Convert 'Price' to numeric"
    BAD CODE: df['Price'] = df['Price'].astype(float)  # Crashes on 'None'
    GOOD CODE: df['Price'] = pd.to_numeric(df['Price'], errors='coerce') # Safe

    Task: "Drop nulls in 'Email'"
    BAD CODE: df.dropna() # Drops everything!
    GOOD CODE: df = df.dropna(subset=['Email']) # Targeted
    """

    error_context = ""
    if error_history:
        error_context = f"\n⚠️ PREVIOUS ATTEMPT FAILED: {error_history}\nFIX THIS ERROR."

    prompt = f"""
    You are a Senior Python Data Engineer.
    
    CURRENT DATA TYPES:
    {dtypes}
    
    SAMPLE DATA:
    {data_sample}
    
    TASK: {task}
    
    {few_shot_examples}
    
    {error_context}
    
    RULES:
    1. Use variable `df`.
    2. Import ANY library you need (e.g., `import numpy as np`).
    3. Return ONLY valid Python code. No markdown.
    """
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1
    )
    
    code = response.choices[0].message.content
    code = code.replace("```python", "").replace("```", "").strip()

    return code
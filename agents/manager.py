import json
import io

def manager_agent(df, client, model):
    """
    Analyzes the dataframe and generates a cleaning plan.
    """
    buffer = io.StringIO()
    df.info(buf=buffer)
    schema_info = buffer.getvalue()
    
    few_shot_examples = """
    EXAMPLE 1:
    Input: Column 'Age' has values ['25', 'Unknown', '30']. Column 'Salary' is int64.
    Output: {"steps": ["Convert 'Age' to numeric, coercing errors", "Fill missing 'Age' values with median"]}

    EXAMPLE 2:
    Input: Column 'Date' is object type '2021-01-01'. Column 'ID' is valid.
    Output: {"steps": ["Convert 'Date' to datetime format"]}
    """

    prompt = f"""
    You are a Senior Data Strategy Manager.
    
    DATA PROFILE:
    {schema_info}
    
    SAMPLE DATA:
    {df.head(3).to_string()}
    
    TASK:
    Analyze the dataset and create a strategic cleaning plan.
    
    STRATEGY RULES:
    1. Look for mixed data types (numbers stored as strings).
    2. Identify missing values and decide whether to drop or fill.
    3. Detect potential categorical inconsistencies (e.g., "USA" vs "usa").
    
    {few_shot_examples}
    
    OUTPUT FORMAT:
    Return ONLY a valid JSON object with a key 'steps'.
    """
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}
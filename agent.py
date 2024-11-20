import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")



## Load Data from CSV
def load_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        return df, None  # Return None for the error if loading is successful
    except Exception as e:
        return None, str(e)  # Return an error message if an error occurs



# Define the file path variable
file_path = './Data/ecommerce_data.csv'

def pandas_Agent(username, query, file_path):
    print("entering pandas_Agent")
    # Load dataset and handle errors
    df, error = load_dataset(file_path)
    if error:  # Check if there is an error
        return f"Error loading data: {error}"

    # Filter the DataFrame by username
    try:
        filtered_df = df[df['username'] == username]
        if filtered_df.empty:
            return "No data found for the specified username."
    except Exception as e:
        return f"Error filtering data: {str(e)}"

    try:
        agent = create_pandas_dataframe_agent(
            ChatGoogleGenerativeAI(temperature=0, model="gemini-1.5-flash"),
            df,
            verbose=True,
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        )

        response = agent.invoke(query)
    except Exception as e:
        return f"Error processing query: {str(e)}"

    return response
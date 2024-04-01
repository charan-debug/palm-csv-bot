import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm import GooglePalm
import pandas as pd

# Define the Streamlit app
def main():
    st.title("Smart Dataframe Chat")
    
    # Create input field for Google API key
    google_api_key = st.text_input("Enter your Google API key:")
    
    # Check if Google API key is provided
    if google_api_key:
        # Load the Google Palm model with the provided API key
        llm = GooglePalm(api_key=google_api_key)
        
        # Define function to load SmartDataframe
        def load_smart_dataframe(data_file):
            # Load the SmartDataframe
            df = SmartDataframe(data_file, config={"llm": llm})
            return df
        
        # Create file uploader component
        uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
        
        # Check if file is uploaded
        if uploaded_file is not None:
            # Load data into a DataFrame
            df = pd.read_csv(uploaded_file)
            
            # Initialize SmartDataframe with the uploaded data
            smart_df = load_smart_dataframe(df)
            
            # Create an input text box for user query
            user_query = st.text_input("Enter your question:")
            
            # Check if the user has entered a query
            if user_query:
                # Use the SmartDataframe to get the response
                response = smart_df.chat(user_query)
                
                # Display the response
                st.write("Response:")
                st.write(response)

# Run the Streamlit app
if __name__ == "__main__":
    main()

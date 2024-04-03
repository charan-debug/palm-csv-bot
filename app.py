import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm import GooglePalm
import pandas as pd
import io

# Define the Streamlit app
def main():
    st.title("GOOGLE PALM AI Chatbot")
    
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
        uploaded_file = st.file_uploader("Upload file", type=['csv', 'xlsx'])
        
        # Check if file is uploaded
        if uploaded_file is not None:
            # Check file type
            if uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': # XLSX file
                # Read XLSX file as DataFrame
                xls = pd.ExcelFile(uploaded_file)
                df = pd.read_excel(xls)
                # Convert DataFrame to CSV format
                csv_file = io.StringIO()
                df.to_csv(csv_file, index=False)
                # Load CSV data into a DataFrame
                csv_file.seek(0)
                df = pd.read_csv(csv_file)
            else: # CSV file
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

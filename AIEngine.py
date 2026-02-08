import google.generativeai as gemini
import streamlit as st


def get_ai_review(data_summary):
    try:
        api_key = st.secrets["AI_API_KEY"]
        gemini.configure(api_key = api_key)
        model = gemini.GenerativeModel('gemini-2.5-flash')
    
    
        prompt = f"""
        You are an Teacher and mentor, and coach.
        You are brutally honest, no-sugarcoated analyst.
        Analyze the following habit tracking data for the user.
        If the Consistency is low, call out his laziness.
        if the efforts are low even when Done is checked, call it out.
        provide actionable, hard-hitting feedback.
        
        Data : {data_summary}
        """
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"There is something wrong : {e}"
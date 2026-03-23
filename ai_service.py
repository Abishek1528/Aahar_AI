import streamlit as st
from groq import Groq

def get_food_recommendation(daily_calories, goal, weight, height, age, gender, activity_level):
    """
    Generates a personalized food recommendation using Groq AI.
    """
    try:
        # Get the API key from Streamlit secrets
        api_key = st.secrets["GROK_API_KEY"]
        
        # Initialize the Groq client
        client = Groq(api_key=api_key)
        
        # Define the prompt for the AI
        prompt = f"""
        You are a professional nutritionist for Aahar AI. Based on the following user health data, 
        provide a detailed and personalized one-day meal plan.

        User Data:
        - Age: {age}
        - Gender: {gender}
        - Weight: {weight} kg
        - Height: {height} cm
        - Activity Level: {activity_level}
        - Primary Goal: {goal}
        - Target Daily Calorie Intake: {daily_calories} kcal

        Requirements for the output:
        1.  Provide specific food items and their approximate portions (e.g., 100g, 1 bowl).
        2.  Categorize the plan into: Breakfast, Mid-morning Snack, Lunch, Evening Snack, and Dinner.
        3.  The total calories of these meals must align with the target: {daily_calories} kcal.
        4.  Include a brief explanation of why these foods are chosen for the user's goal ({goal}).
        5.  Keep the format clean and professional using Markdown.
        6.  Use bold headings for each meal section.
        """

        # Call the Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", # Using a common Groq model
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly qualified clinical nutritionist who provides precise and medically-sound dietary advice."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        # Extract and return the AI's response
        return completion.choices[0].message.content

    except Exception as e:
        return f"Error: Could not generate a meal plan. (Details: {str(e)})"

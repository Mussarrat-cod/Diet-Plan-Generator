import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image

# Load and display header image
img = Image.open("healthy_banner.jpg")  # Ensure this image is in your working directory
st.image(img, use_column_width=True)

# Custom CSS for styling
st.markdown("""
<style>
body {
    background-color: #f4fdf4;
}

h1, h3, h4 {
    color: #2E7D32;
}

.bmi-card, .category-card, .deficiency-card {
    background-color: #ffffff;
    border-left: 5px solid #81C784;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

.bullet-point {
    margin-left: 20px;
    color: #388E3C;
    font-weight: 500;
}

.header-text {
    color: #1B5E20;
    font-size: 22px;
    font-weight: 700;
}

p {
    font-size: 17px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

# BMI calculation
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_diet_recommendations(bmi_category, deficiencies):
    recommendations = []
    if bmi_category == "Underweight":
        recommendations += ["Increase caloric intake with nutrient-dense foods",
                            "Focus on healthy fats and proteins"]
    elif bmi_category == "Overweight":
        recommendations += ["Reduce caloric intake while maintaining nutrient density",
                            "Increase fiber-rich foods"]
    elif bmi_category == "Obese":
        recommendations += ["Significantly reduce caloric intake",
                            "Focus on high-fiber, low-calorie foods"]

    deficiency_map = {
        "Iron": "Include iron-rich foods like lean meats, leafy greens, and legumes",
        "Vitamin D": "Add fatty fish, fortified dairy, and egg yolks to your diet",
        "Calcium": "Incorporate dairy products, fortified plant milk, and leafy greens",
        "Vitamin B12": "Include animal products or fortified foods",
        "Protein": "Add lean meats, fish, eggs, or plant-based protein sources"
    }
    for d in deficiencies:
        if d in deficiency_map:
            recommendations.append(deficiency_map[d])

    return recommendations

def main():
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1>🍏 Personalized Diet Planner</h1>
        <p style='color: #666; font-size: 18px;'>Your guide to healthy eating based on your BMI and nutrient needs</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="bmi-card">
        <h3 class="header-text">🧮 1. Calculate Your BMI</h3>
        <p>Enter your weight and height to calculate your Body Mass Index (BMI).</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        weight = st.number_input("Weight (kg)", 20.0, 300.0, 70.0)
    with col2:
        height = st.number_input("Height (m)", 0.5, 2.5, 1.7)

    if st.button("Calculate BMI"):
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)
        st.session_state['bmi'] = bmi
        st.session_state['category'] = category

        st.markdown(f"""
        <div class="category-card">
            <h4>Your Results:</h4>
            <p>Your BMI: <b>{bmi:.2f}</b></p>
            <p>Category: <b>{category}</b></p>
        </div>
        """, unsafe_allow_html=True)

        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=bmi,
            title={'text': "BMI Score"},
            gauge={
                'axis': {'range': [10, 40]},
                'bar': {'color': "#4CAF50"},
                'steps': [
                    {'range': [10, 18.5], 'color': "#FFCDD2"},
                    {'range': [18.5, 24.9], 'color': "#C8E6C9"},
                    {'range': [25, 29.9], 'color': "#FFF9C4"},
                    {'range': [30, 40], 'color': "#FFAB91"},
                ]
            }
        ))
        st.plotly_chart(fig)

    st.markdown("""
    <div class="deficiency-card">
        <h3 class="header-text">🍎 2. Nutrient Deficiency Assessment</h3>
        <p>Select any nutrient deficiencies you have been diagnosed with:</p>
    </div>
    """, unsafe_allow_html=True)

    deficiencies = st.multiselect("Select deficiencies:",
                                  ["Iron", "Vitamin D", "Calcium", "Vitamin B12", "Protein"])

    if st.button("Generate Diet Plan"):
        if 'category' not in st.session_state:
            st.warning("Please calculate your BMI first.")
        else:
            category = st.session_state['category']
            plan = get_diet_recommendations(category, deficiencies)

            st.markdown("""
            <div class="deficiency-card">
                <h3 class="header-text">📋 Your Personalized Diet Plan</h3>
                <p>Based on your BMI and deficiencies:</p>
            </div>
            """, unsafe_allow_html=True)

            for rec in plan:
                st.markdown(f"<div class='bullet-point'>• {rec}</div>", unsafe_allow_html=True)

            st.markdown("""
            <div class="deficiency-card">
                <h3 class="header-text">💡 Additional Tips</h3>
            </div>
            """, unsafe_allow_html=True)

            tips = [
                "Stay hydrated by drinking plenty of water",
                "Eat a variety of colorful fruits and vegetables",
                "Consult with a dietitian for personalized advice",
                "Monitor your progress and adjust the plan as needed"
            ]
            for tip in tips:
                st.markdown(f"<div class='bullet-point'>• {tip}</div>", unsafe_allow_html=True)

    st.markdown("""
    <hr>
    <div style='text-align: center; color: grey; font-size: 14px;'>
        Made with ❤️ using Streamlit · Powered by OpenAI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

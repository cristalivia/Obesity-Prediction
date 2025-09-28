import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Obesity Prediction Application")

st.title("Obesity Prediction")
st.markdown("Insert the form below to predict your obesity level.")

with st.form("prediction_form"):
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.number_input("Age", min_value=15, max_value=100, step=1)
    height = st.number_input("Height (m)", format="%.2f",min_value=1.00)
    weight = st.number_input("Weight (kg)", format="%.1f",min_value=20.0)
    family_history = st.selectbox("Do you have a family history of overweight or obesity?", ["yes", "no"])
    favc = st.selectbox("Do you eat high calorie food frequently?", ["yes", "no"])
    fcvc = st.slider("On a scale of 1 to 3, how frequently do you consume vegetables?", 1.0, 3.0, step=0.1)
    ncp = st.number_input("How many main meals do you typically consume per day?", min_value=1, max_value=4, step=1)
    caec = st.selectbox("How often do you eat food between main meals?", ["no", "Sometimes", "Frequently", "Always"])
    smoke = st.selectbox("Do you smoke?", ["yes", "no"])
    ch2o = st.slider("On a scale of 1 to 3, how would you describe your average daily water intake?", 1.0, 3.0, step=0.1)
    scc = st.selectbox("Do you monitor your calorie intake?", ["yes", "no"])
    faf = st.slider("On a scale of 1 to 3, how often do you engage in physical activity?", 0.0, 3.0, step=0.1)
    tue = st.slider( "On a scale of 0 to 2, how much time do you spend daily using technology devices?", 0.0, 2.0, step=0.1)
    calc = st.selectbox("How often do you consume alcohol?", ["no", "Sometimes", "Frequently"])
    mtrans = st.selectbox("What is your primary mode of transportation?", ["Walking", "Bike", "Motorbike", "Public_Transportation", "Automobile"])

    submitted = st.form_submit_button("Predict")

if submitted:
    api_url = "http://127.0.0.1:8000/predict"
    label_mapping = {
        "0": "Insufficient Weight",
        "1": "Normal Weight",
        "2": "Obesity Type I",
        "3": "Obesity Type II",
        "4": "Obesity Type III",
        "5": "Overweight Level I",
        "6": "Overweight Level II"
    }
    payload = {
        "Gender": gender,
        "Age": int(age),
        "Height": float(height),
        "Weight": float(weight),
        "family_history_with_overweight": family_history,
        "FAVC": favc,
        "FCVC": fcvc,
        "NCP": ncp,
        "CAEC": caec,
        "SMOKE": smoke,
        "CH2O": ch2o,
        "SCC": scc,
        "FAF": faf,
        "TUE": tue,
        "CALC": calc,
        "MTRANS": mtrans
    }

    try:
        response = requests.post(api_url, json=payload)
        result = response.json()
        label = str(result["prediction"])
        category = label_mapping.get(label, "Unknown")
        st.success(f"Your predicted obesity category is **{category}**")

    except Exception as e:
        st.error(f"Error connecting to API: {e}")

if st.checkbox("Run Test Cases"):
    st.markdown("## Test Case Results")
    label_mapping = {
        "0": "Insufficient Weight",
        "1": "Normal Weight",
        "2": "Obesity Type I",
        "3": "Obesity Type II",
        "4": "Obesity Type III",
        "5": "Overweight Level I",
        "6": "Overweight Level II"
    }
    test_cases = [
        {
            "title": "Test Case 1",
            "data": {
                "Gender": "Male",
                "Age": 31,
                "Height": 1.87,
                "Weight": 128.87,
                "family_history_with_overweight": "yes",
                "FAVC": "yes",
                "FCVC": 2.96,
                "NCP": 3.00,
                "CAEC": "Sometimes",
                "SMOKE": "yes",
                "CH2O": 1.28,
                "SCC": "no",
                "FAF": 0.90,
                "TUE": 1.875,
                "CALC": "Sometimes",
                "MTRANS": "Automobile"
            }
        },
        {
            "title": "Test Case 2",
            "data": {
                "Gender": "Female",
                "Age": 18,
                "Height": 1.59,
                "Weight": 40.00,
                "family_history_with_overweight": "yes",
                "FAVC": "yes",
                "FCVC": 2.00,
                "NCP": 1.00,
                "CAEC": "Frequently",
                "SMOKE": "no",
                "CH2O": 1.00,
                "SCC": "no",
                "FAF": 0.00,
                "TUE": 2.000,
                "CALC": "no",
                "MTRANS": "Public_Transportation"
            }
        }
    ]

    for case in test_cases:
        st.markdown(f"### {case['title']}")
        df_input = pd.DataFrame([case["data"]])
        st.dataframe(df_input.style.set_properties(**{'text-align': 'left'}), use_container_width=True)

        try:
            response = requests.post("http://127.0.0.1:8000/predict", json=case["data"])
            if response.status_code == 200:
                result = response.json()
                label = str(result["prediction"])
                category = label_mapping.get(label, "Unknown")
                st.success(f"Prediction: **{category}**")
            else:
                err = response.json().get("detail", response.text)
                st.error(f"Error {response.status_code}: {err}")
        except Exception as e:
                st.error(f"Error in {case['title']}: {e}")
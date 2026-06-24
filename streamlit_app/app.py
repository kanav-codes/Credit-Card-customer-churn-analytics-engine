import os
import streamlit as st
import pandas as pd
import joblib

# Page Config
st.set_page_config(page_title="Churn Prediction App", layout="wide")

# FIX: Model ka path current file ke folder ke hisaab se set karo
current_dir = os.path.dirname(__file__)
model_path = os.path.join(current_dir, 'churn_model.pkl')
model = joblib.load(model_path)

st.title("📊 Customer Churn Prediction Dashboard")

tab1, tab2, tab3 = st.tabs(["📊 Performance", "📉 Drivers", "🧪 Live Test"])

with tab1:
    st.subheader("Model Performance")
    # Images ke liye bhi path fix karo
    st.image(os.path.join(current_dir, "images1/aoc.png"), use_container_width=True)
    st.write("**Model Accuracy:** 85% | **AUC Score:** 0.98")

with tab2:
    st.subheader("Key Drivers")
    st.image(os.path.join(current_dir, "images1/driversc.png"), use_container_width=True)

# ... baaki ka code waisa hi rehne de ...

with tab3:
    st.subheader("🧪 Live Test")
    
    # User Inputs
    trans_amt = st.number_input("Total Transaction Amount", 509, 19000, 4400)
    trans_ct = st.number_input("Total Transaction Count", 9, 140, 64)
    credit_limit = st.number_input("Credit Limit", 1443, 34517, 8600)
    edu = st.selectbox("Education Level", ["Graduate", "High School", "Doctorate", "Post-Graduate", "Uneducated", "Unknown"])
    marital = st.selectbox("Marital Status", ["Married", "Single", "Unknown"])

    if st.button("Predict"):
        # Base dictionary (Average Values)
        data = {
            'Dependent_count': 2, 'Months_on_book': 36, 'Total_Relationship_Count': 4, 
            'Months_Inactive_12_mon': 2, 'Contacts_Count_12_mon': 2, 'Credit_Limit': credit_limit, 
            'Total_Revolving_Bal': 1160, 'Avg_Open_To_Buy': 7400, 'Total_Amt_Chng_Q4_Q1': 0.76, 
            'Total_Trans_Amt': trans_amt, 'Total_Trans_Ct': trans_ct, 'Total_Ct_Chng_Q4_Q1': 0.71, 
            'Avg_Utilization_Ratio': 0.27, 'Education_Level_Doctorate': 0, 'Education_Level_Graduate': 0, 
            'Education_Level_High School': 0, 'Education_Level_Post-Graduate': 0, 'Education_Level_Uneducated': 0, 
            'Education_Level_Unknown': 0, 'Marital_Status_Married': 0, 'Marital_Status_Single': 0, 
            'Marital_Status_Unknown': 0, 'Income_Category_$40K - $60K': 1, 'Income_Category_$60K - $80K': 0, 
            'Income_Category_$80K - $120K': 0, 'Income_Category_Less than $40K': 0, 
            'Income_Category_Unknown': 0, 'Card_Category_Gold': 0, 'Card_Category_Platinum': 0, 'Card_Category_Silver': 1
        }
        
        # Update Categorical Inputs
        data[f'Education_Level_{edu}'] = 1
        data[f'Marital_Status_{marital}'] = 1
        
        # Convert and Predict
        input_df = pd.DataFrame([data])
        prediction = model.predict(input_df)
        
        if prediction[0] == 1:
            st.error("Prediction: Customer likely to CHURN! ⚠️")
        else:
            st.success("Prediction: Customer likely to STAY. ✅")

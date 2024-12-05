import pandas as pd
import streamlit as st
import pickle

# Load the trained credit score classification model
with open(r"C:\Users\Sahan\Documents\phase_5_Project\CSV\credit_score_pipeline.pkl", "rb") as f:
    model_pipeline = pickle.load(f)

# Function to predict credit category (Bad, Fair, or Good)
def predict_credit_category(outstanding_debt, num_credit_cards, payment_of_min_amount, num_bank_accounts, monthly_inhand_salary, annual_income, age, num_of_loan):
    # Correct the encoding: 0 = Yes (good), 1 = No (bad)
    input_data = pd.DataFrame({
        "Outstanding_Debt_Cleaned": [outstanding_debt],
        "Num_Credit_Card": [num_credit_cards],
        "Payment_of_Min_Amount_Yes": [1 if payment_of_min_amount == "No" else 0],  # Now, 1 means 'No' (bad), 0 means 'Yes' (good)
        "Num_Bank_Accounts": [num_bank_accounts],
        "Monthly_Inhand_Salary": [monthly_inhand_salary],
        "Annual_Income_Cleaned": [annual_income],
        "Age_Cleaned": [age],
        "Num_of_Loan_Cleaned": [num_of_loan]
    })
    
    # Predict the credit category (0 = Bad, 1 = Fair, 2 = Good)
    credit_category = model_pipeline.predict(input_data)[0]
    return credit_category

# Map credit category to house eligibility
def map_credit_category_to_houses(credit_category):
    """ Map the predicted credit category to eligible house price limit """
    if credit_category == 0:
        return "Bad Credit: Limited options, lower price range houses."
    elif credit_category == 1:
        return "Fair Credit: Moderate price range houses."
    elif credit_category == 2:
        return "Good Credit: Higher price range houses."

# Filter house listings based on credit category and income
def get_house_listings_based_on_credit(df, credit_category, annual_income):
    """ 
    Filter houses based on the predicted credit category and annual income range.
    """
    # Calculate house price range based on user's annual income
    min_price = annual_income * 0.7  # 70% of annual income (adjust as necessary)
    max_price = annual_income * 1.4  # 140% of annual income (adjust as necessary)
    
    # Filter houses based on the price range and exclude houses under 70,000
    filtered_houses = df[(df['price'] >= 70000) & (df['price'] >= min_price) & (df['price'] <= max_price)]
    
    # Eliminate listings where 'living_space' is 0 or bedroom_number or bathroom_number is 0
    filtered_houses = filtered_houses[(filtered_houses['living_space'] > 0) & (filtered_houses['bedroom_number'] > 0) & (filtered_houses['bathroom_number'] > 0)]
    
    # Clean up the zip_code format (remove commas)
    filtered_houses['zip_code'] = filtered_houses['zip_code'].astype(str).str.replace(",", "")
    
    # Handle sorting differently based on credit category
    if credit_category == 2:  # Good Credit
        # Sort by most bedrooms, living space, and bathrooms (descending order)
        sorted_houses = filtered_houses.sort_values(
            by=['bedroom_number', 'living_space', 'bathroom_number'],
            ascending=[False, False, False]
        )
        # Sort by price (ascending) to show least expensive ones in the best category
        sorted_houses = sorted_houses.sort_values(by='price', ascending=True)

    elif credit_category == 1:  # Fair Credit
        # Find the median for bedrooms, living space, and bathrooms within the filtered houses
        median_bedroom = filtered_houses['bedroom_number'].median()
        median_living_space = filtered_houses['living_space'].median()
        median_bathroom = filtered_houses['bathroom_number'].median()
        
        # Sort by median values first
        filtered_houses['bedroom_distance'] = (filtered_houses['bedroom_number'] - median_bedroom).abs()
        filtered_houses['living_space_distance'] = (filtered_houses['living_space'] - median_living_space).abs()
        filtered_houses['bathroom_distance'] = (filtered_houses['bathroom_number'] - median_bathroom).abs()
        
        # Sort by closeness to the median, then by bedrooms, living space, and bathrooms in descending order
        sorted_houses = filtered_houses.sort_values(
            by=['bedroom_distance', 'living_space_distance', 'bathroom_distance'],
            ascending=[True, True, True]
        )
        sorted_houses = sorted_houses.sort_values(
            by=['bedroom_number', 'living_space', 'bathroom_number'],
            ascending=[False, False, False]
        )
        
        # Get the 5 most expensive houses in the price range
        expensive_houses = filtered_houses.sort_values(by='price', ascending=False).head(5)
        
        # Combine the two lists and remove duplicates
        sorted_houses = pd.concat([sorted_houses, expensive_houses]).drop_duplicates()

    else:  # Bad Credit
        # Sort by least bedrooms, living space, and bathrooms (ascending order)
        sorted_houses = filtered_houses.sort_values(
            by=['bedroom_number', 'living_space', 'bathroom_number'],
            ascending=[True, True, True]
        )
    
    # Show only top 10 listings
    top_houses = sorted_houses.head(10)

    return top_houses[['address', 'price', 'bedroom_number', 'bathroom_number', 'living_space', 'zip_code']]

# Streamlit App UI
def app():
    st.title(" Houses based on your fiancial information")

    # User input for classification model features
    outstanding_debt = st.number_input("How much money do you owe across all of your bank accounts?", min_value=0.0)
    num_credit_cards = st.number_input("Number of Credit Cards:", min_value=1)
    payment_of_min_amount = st.selectbox("Do you pay your balances on time?", options=["Yes", "No"])
    num_bank_accounts = st.number_input("Number of Bank Accounts:", min_value=0)
    annual_income = st.number_input("Annual Income:", min_value=0.0)
    monthly_inhand_salary = st.number_input("How much money do you spend on fees every month (rent,insurance...etc.)?", min_value=0.0)
    age = st.number_input("Age:", min_value=18)
    num_of_loan = st.number_input("Number of Loans:", min_value=0)

    # If the user inputs all necessary information
    if (outstanding_debt > 0 and num_credit_cards > 0 and num_bank_accounts >= 0 and
        monthly_inhand_salary > 0 and annual_income > 0 and age >= 18 and num_of_loan >= 0):
        # Get the predicted credit category
        credit_category = predict_credit_category(outstanding_debt, num_credit_cards, payment_of_min_amount, num_bank_accounts, monthly_inhand_salary, annual_income, age, num_of_loan)
        
        # Map credit category to house eligibility
        eligibility = map_credit_category_to_houses(credit_category)
        st.write(f"Credit Category: {['Bad Credit', 'Fair Credit', 'Good Credit'][credit_category]}")
        st.write(eligibility)

        # Load the dataset (replace with your actual dataset path)
        df = pd.read_csv(r"C:\Users\Sahan\Documents\Phase_5_Project\CSV\NYCH.csv")  # Update to correct path

        # Filter and sort the houses based on credit category and annual income
        house_listings = get_house_listings_based_on_credit(df, credit_category, annual_income)

        # Display the results
        if not house_listings.empty:
            st.write("Here are the available listings (sorted by the adjusted criteria):")
            st.dataframe(house_listings)
        else:
            st.write("No listings found based on your credit category and income range.")
    else:
        st.write("Please enter valid inputs to get recommendations.")

# Run the Streamlit app
if __name__ == "__main__":
    app()

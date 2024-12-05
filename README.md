# <font color="blue"><u>Introduction:</u></font>
The classification pipeline is designed to predict the credit category of individuals based on their financial information. By leveraging machine learning techniques, this pipeline assists in predicting whether a person is classified as having Bad, Fair, or Good credit based on input features such as debt, salary, number of credit cards, and loans. The pipeline uses XGBClassifier, a powerful gradient boosting model, to handle class imbalance and optimize the classification task.

# <font color="blue"><u>Overview:</u></font>
The pipeline consists of multiple stages:

Data Preprocessing: Handling missing data and splitting the dataset.
Class Imbalance Handling: Using oversampling methods like RandomOverSampler.
Model Training and Tuning: Applying XGBClassifier with hyperparameter tuning using RandomizedSearchCV.
Model Evaluation: Using performance metrics such as accuracy, precision, recall, and AUC-ROC score.
Feature Importance: Visualizing which features are most influential in predicting the credit score

# <font color="blue"><u>Business Understanding:</u></font>
The goal of the classification pipeline is to predict an individual's credit score category, which has direct applications in financial services. Financial institutions can use this prediction to assess an individual's eligibility for loans, credit cards, or even mortgages. By predicting credit scores based on financial data, businesses can improve decision-making and reduce financial risk.

# <font color="blue"><u>Data Understanding and Analysis:</u></font>

The dataset consists of various financial features such as:

Debt and income-related attributes: These include annual income, outstanding debt, and the number of credit cards.
Credit-related behaviors: Features like the number of loans and whether the individual pays the minimum amount due on time.
Preprocessing steps include:

Data Cleaning: Removing missing values from the target variable (Credit_Score).
Handling Class Imbalance: Since the credit categories are imbalanced, techniques like oversampling were applied to ensure the model doesn't become biased toward the majority class.

# <font color="blue"><u>Results:</u></font>
The app provides interactive results by showing house listings that match the user's predicted credit score category. The listings are:

Good Credit: More premium houses are shown, with desirable features like more bedrooms, larger space, etc.
Fair Credit: Moderate-priced houses are shown, with a balance of desirable attributes.
Bad Credit: Houses that are more affordable or have fewer amenities are shown to match the user's financial capabilities.

# <font color="blue"><u>Conclusions:</u></font>
The Streamlit app effectively combines the prediction of credit scores with a personalized housing recommendation system. It offers an engaging and user-friendly way for individuals to understand their credit status and make informed decisions regarding housing. Further improvements could include enhancing the user interface with more advanced visualizations or integrating real-time data for more up-to-date house listings.






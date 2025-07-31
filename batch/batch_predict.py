import pandas as pd
import joblib

model = joblib.load("xgboost_random_search.pkl")

# Load new data 
new_loans = pd.read_csv('batch/input/new_loans.csv')

# Apply preprocessing
X = pd.get_dummies(new_loans, drop_first=True)

for col in model.feature_names_in_:
    if col not in X.columns:
        X[col] = 0
X = X[model.feature_names_in_]


# Run predictions
new_loans['default_probability'] = model.predict_proba(X)[:,1]
new_loans['prediction'] = (new_loans['default_probability'] >= 0.5).astype(int)

# Save results
new_loans.to_csv("predictions.csv", index=False)
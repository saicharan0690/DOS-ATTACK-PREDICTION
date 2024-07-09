import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
df = pd.read_csv('DrDos_NTP.csv', header=0, low_memory=False)

# Identify and handle columns with mixed types
# For example, if 'Column_Name' is the column causing the issue, you can convert it to numeric or drop it
# df['Column_Name'] = pd.to_numeric(df['Column_Name'], errors='coerce')
# df = df.dropna(subset=['Column_Name'])

# Preprocess the dataset
df.columns = df.columns.str.strip()  # Remove leading/trailing whitespaces from column names
target_column = 'Label'  # Use 'Label' without any whitespaces
X = df.drop(target_column, axis=1)
y = df[target_column]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy}")

# Save the model
joblib.dump(model, 'random_forest_model.pkl')

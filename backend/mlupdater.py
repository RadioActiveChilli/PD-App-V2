import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

# Load the data from the Excel file
df = pd.read_excel('predictiontable.xlsx')

# Prepare the data
X = df[['Length of line drawing', 'Percentage Difference from Reference Length',
        'Percentage Similarity to Reference Drawing', 'Number of Times Pen was Lifted',
        'Average angle between consecutive groups of 3 points']]
y = df['Prediction of Parkinson\'s Disease']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Naive Bayes classifier
clf = GaussianNB()
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

# Example of predicting a new data row
new_data_row = [[1140.67, -0.02, 40.22, 0, 25.595862227]]
prediction = clf.predict(new_data_row)
print("Predicted Parkinson's Disease:", prediction)

from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the Iris dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target
print("Dataset Size:", X.shape)


# Split dataset into {60% train, 20% test}
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)
# Splitting temp dataset into {50% test, 50% cross validation}
X_test, X_cv, y_test, y_cv = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# model training
random_forest = RandomForestClassifier()
random_forest.fit(X_train, y_train)

# model testing on {50% test dataset}
y_pred_test = random_forest.predict(X_test)
accuracy_test = accuracy_score(y_test, y_pred_test)
print("Test Set Accuracy:", accuracy_test)

# model testing on {50% cross validation dataset}
y_pred_cv = random_forest.predict(X_cv)
accuracy_cv = accuracy_score(y_cv, y_pred_cv)
print("Cross-Validation Set Accuracy:", accuracy_cv)
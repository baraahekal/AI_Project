from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()
X = iris.data
y = iris.target

# split dataset to {20% test, 80% train}
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

random_forest = RandomForestClassifier()
random_forest.fit(X_train, y_train)
y_pred_random_forest = random_forest.predict(X_test)
accuracy_random_forest = accuracy_score(y_test, y_pred_random_forest)
print("Random Forest Accuracy:", accuracy_random_forest)


from sklearn.model_selection import cross_val_score
# used k-fold cross validation which k = 5, to ensure the model overall performance
cross_val_scores = cross_val_score(random_forest, X, y, cv=5)
print("Average Cross-Validation Accuracy:", cross_val_scores.mean())
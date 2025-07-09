import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Load dataset
file_path = "collected_alpha_power_results.csv"
data = pd.read_csv(file_path)
data["Dataset No."] = data["Dataset No."].astype(str)

# Handle missing values
imputer = SimpleImputer(strategy="mean")
X = data.iloc[:, :-2]
X = imputer.fit_transform(X)

# Extract labels and groups
y = data["Stress"].values
groups = data["Dataset No."].values

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Define Keras model
def create_model(input_dim):
    model = Sequential()
    model.add(Dense(64, activation='relu', input_dim=input_dim))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))  # For binary classification
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# GroupKFold cross-validation
group_kfold = GroupKFold(n_splits=5)
accuracies = []

for fold, (train_idx, test_idx) in enumerate(group_kfold.split(X_scaled, y, groups)):
    print(f"Fold {fold+1}")
    X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]

    model = create_model(X_train.shape[1])
    model.fit(X_train, y_train, epochs=20, batch_size=32, verbose=0)

    y_pred = (model.predict(X_test) > 0.5).astype("int32").flatten()
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.2f}")
    accuracies.append(acc)

print(f"Cross-Validation Accuracy: {np.mean(accuracies):.2f} ± {np.std(accuracies):.2f}")

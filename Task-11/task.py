# Import necessary libraries
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Step 1: Load a random dataset (Iris dataset)
iris = load_iris()
X = iris.data  # Features
y = iris.target  # Labels

# Convert to DataFrame for better visualization
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = y
df['species_name'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})

print("="*50)
print("DATASET OVERVIEW")
print("="*50)
print(f"Dataset shape: {df.shape}")
print(f"Features: {iris.feature_names}")
print(f"Target classes: {iris.target_names}")
print("\nFirst 5 rows:")
print(df.head())
print("\nDataset info:")
print(df.info())

# Step 2: Train-Test Splitting
print("\n" + "="*50)
print("TRAIN-TEST SPLITTING")
print("="*50)

# Split the data (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2,      # 20% for testing
    random_state=42,    # For reproducibility
    stratify=y          # Maintain class distribution
)

print(f"Training set size: {X_train.shape[0]} samples")
print(f"Testing set size: {X_test.shape[0]} samples")
print(f"Training labels distribution: {np.bincount(y_train)}")
print(f"Testing labels distribution: {np.bincount(y_test)}")

# Step 3: Choose and apply the right model
print("\n" + "="*50)
print("MODEL SELECTION & TRAINING")
print("="*50)

# Trying multiple models to choose the best one
models = {
    'Logistic Regression': LogisticRegression(max_iter=200, random_state=42),
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'Support Vector Machine': SVC(kernel='rbf', random_state=42)
}

best_model = None
best_accuracy = 0

for name, model in models.items():
    # Train the model
    model.fit(X_train, y_train)
    
    # Make predictions on test set
    y_pred = model.predict(X_test)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n{name}:")
    print(f"  Training Accuracy: {model.score(X_train, y_train):.4f}")
    print(f"  Testing Accuracy: {accuracy:.4f}")
    
    # Track best model
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_model = model
        best_model_name = name

print(f"\n✓ Best Model Selected: {best_model_name} (Accuracy: {best_accuracy:.4f})")

# Step 4: Testing/Predicting with the best model
print("\n" + "="*50)
print("TESTING/PREDICTING WITH BEST MODEL")
print("="*50)

# Make predictions on test set
y_pred_final = best_model.predict(X_test)

# Display predictions vs actual values
print("\nSample Predictions (first 10 test samples):")
print("-" * 50)
comparison_df = pd.DataFrame({
    'Actual': y_test[:10],
    'Actual Species': [iris.target_names[i] for i in y_test[:10]],
    'Predicted': y_pred_final[:10],
    'Predicted Species': [iris.target_names[i] for i in y_pred_final[:10]],
    'Correct?': y_test[:10] == y_pred_final[:10]
})
print(comparison_df)

# Step 5: Display Accuracy Score and detailed metrics
print("\n" + "="*50)
print("ACCURACY SCORE & PERFORMANCE METRICS")
print("="*50)

# Overall accuracy
accuracy = accuracy_score(y_test, y_pred_final)
print(f"\n✓ Overall Accuracy Score: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Detailed classification report
print("\n📊 Classification Report:")
print("-" * 50)
print(classification_report(y_test, y_pred_final, 
                          target_names=iris.target_names))

# Confusion Matrix
print("\n📈 Confusion Matrix:")
print("-" * 50)
cm = confusion_matrix(y_test, y_pred_final)
print(cm)

# Visualize confusion matrix (optional - if matplotlib is available)
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=iris.target_names,
                yticklabels=iris.target_names)
    plt.title('Confusion Matrix - Iris Dataset')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.tight_layout()
    plt.show()
except:
    print("\n(Visualization skipped - matplotlib/seaborn not available)")

# Additional metrics
print("\n" + "="*50)
print("ADDITIONAL INSIGHTS")
print("="*50)

# Per-class accuracy
print("\nPer-class Accuracy:")
for i, class_name in enumerate(iris.target_names):
    class_mask = y_test == i
    class_correct = (y_pred_final[class_mask] == y_test[class_mask]).sum()
    class_total = class_mask.sum()
    if class_total > 0:
        print(f"  {class_name:12s}: {class_correct}/{class_total} ({class_correct/class_total*100:.1f}%)")

# Number of misclassifications
misclassifications = (y_pred_final != y_test).sum()
print(f"\n❌ Total Misclassifications: {misclassifications}/{len(y_test)}")

return best_model, accuracy, y_pred_final
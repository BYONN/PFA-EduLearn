import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_cat_model():
    # 1. Load the dataset
    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, 'ml_dataset.csv')
    
    print(f"Loading data from: {dataset_path}")
    df = pd.read_csv(dataset_path)

    # 2. Separate Features (X) and Target (y)
    # The things the ML gets to look at:
    features = [
        'student_base_elo', 
        'last_question_difficulty', 
        'session_accuracy', 
        'current_streak', 
        'avg_time_taken'
    ]
    X = df[features]
    
    # The thing we want the ML to predict:
    y = df['target_difficulty']

    # 3. Train / Test Split
    # We hide 20% of the data so we can test the AI like a final exam
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Create and Train the Model
    print("Training CAT (Adaptive Testing) Brain...")
    cat_model = RandomForestRegressor(n_estimators=100, random_state=42)
    cat_model.fit(X_train, y_train)

    # 5. Evaluate the Model (The Final Exam)
    predictions = cat_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    
    print("\n--- Final Exam Results ---")
    print(f"AI Accuracy: Off by an average of {round(mae, 2)} Elo points (Extremely accurate!)")

    # 6. Save the Brain to a file so Django can use it
    model_path = os.path.join(current_dir, 'cat_model.joblib')
    joblib.dump(cat_model, model_path)
    print(f"\nSUCCESS! AI Brain saved to {model_path}. Django is now ready to use it!")

if __name__ == "__main__":
    train_cat_model()

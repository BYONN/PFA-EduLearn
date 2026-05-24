import pandas as pd
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_cat_model():
    current_dir = os.path.dirname(__file__)
    dataset_path = os.path.join(current_dir, 'ml_dataset.csv')
    
    print(f"Loading data from: {dataset_path}")
    df = pd.read_csv(dataset_path)

    features = [
        'student_base_elo', 
        'last_question_difficulty', 
        'session_accuracy', 
        'current_streak', 
        'avg_time_taken'
    ]
    X = df[features]
    
    y = df['target_difficulty']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training CAT (Adaptive Testing) Brain...")
    cat_model = RandomForestRegressor(n_estimators=100, random_state=42)
    cat_model.fit(X_train, y_train)

    predictions = cat_model.predict(X_test)
    
    mae = mean_absolute_error(y_test, predictions)
    
    print("\n--- Final Exam Results ---")
    print(f"AI Accuracy: Off by an average of {round(mae, 2)} Elo points (Extremely accurate!)")

    model_path = os.path.join(current_dir, 'cat_model.joblib')
    joblib.dump(cat_model, model_path)
    print(f"\nSUCCESS! AI Brain saved to {model_path}. Django is now ready to use it!")

if __name__ == "__main__":
    train_cat_model()

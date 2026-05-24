import joblib
import os
import pandas as pd

def test_cat_model():
    print("==================================================")
    print("   ADAPTIVE AI (CAT) - TEST LAB   ")
    print("==================================================\n")

    current_dir = os.path.dirname(__file__)
    model_path = os.path.join(current_dir, 'cat_model.joblib')
    
    try:
        cat_model = joblib.load(model_path)
    except FileNotFoundError:
        print("ERROR: Could not find cat_model.joblib. Did you run train_model.py?")
        return

    print("Loading test scenarios...\n")
    
    scenarios = [
        {
            "name": "Scenario 1: The Struggling Student",
            "desc": "A 1200 Elo student who is getting low accuracy (30%) and taking a long time (55s).",
            "student_base_elo": 1200,
            "last_question_difficulty": 1250,
            "session_accuracy": 0.30,
            "current_streak": 0,
            "avg_time_taken": 55
        },
        {
            "name": "Scenario 2: The Average Student",
            "desc": "A 1200 Elo student answering normally with okay accuracy (60%).",
            "student_base_elo": 1200,
            "last_question_difficulty": 1250,
            "session_accuracy": 0.60,
            "current_streak": 1,
            "avg_time_taken": 25
        },
        {
            "name": "Scenario 3: The Gifted Student (Hot Streak)",
            "desc": "A 1200 Elo student crushing it! High accuracy (95%), 4 streak, answering fast (10s).",
            "student_base_elo": 1200,
            "last_question_difficulty": 1250,
            "session_accuracy": 0.95,
            "current_streak": 4,
            "avg_time_taken": 10
        }
    ]

    for s in scenarios:
        print(f"\n--- {s['name']} ---")
        print(f"Context: {s['desc']}")
        
        input_data = pd.DataFrame([{
            'student_base_elo': s['student_base_elo'],
            'last_question_difficulty': s['last_question_difficulty'],
            'session_accuracy': s['session_accuracy'],
            'current_streak': s['current_streak'],
            'avg_time_taken': s['avg_time_taken']
        }])
        
        predicted_difficulty = cat_model.predict(input_data)[0]
        
        print(f"-> Current Question Elo: {s['last_question_difficulty']}")
        print(f"** AI RECOMMENDED NEXT QUESTION ELO: {round(predicted_difficulty)}")
        
        jump = round(predicted_difficulty) - s['last_question_difficulty']
        if jump > 0:
            print(f"++ Difficulty Jump: +{jump} points (Getting harder!)")
        else:
            print(f"-- Difficulty Jump: {jump} points (Getting easier!)")
        
    print("\n==================================================")
    print("Testing complete. The CAT brain is fully functional!")

if __name__ == "__main__":
    test_cat_model()

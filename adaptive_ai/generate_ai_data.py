import pandas as pd
import random
import os

def generate_cat_dataset(num_samples=10000):
    """
    Generates a dataset for a Computerized Adaptive Testing (CAT) ML Model.
    The goal is to recommend the ideal difficulty for the NEXT question.
    """
    data = []
    
    for _ in range(num_samples):
        student_base_elo = random.randint(800, 2000)
        
        last_question_difficulty = student_base_elo + random.randint(-150, 150)
        
        session_accuracy = round(random.uniform(0.2, 1.0), 2)
        
        if session_accuracy > 0.8:
            current_streak = random.randint(2, 8)
        elif session_accuracy > 0.5:
            current_streak = random.randint(0, 3)
        else:
            current_streak = 0
            
        avg_time_taken = random.randint(5, 60)
        
        difficulty_shift = 0
        
        difficulty_shift += (current_streak * 30) 
        
        difficulty_shift += ((session_accuracy - 0.5) * 150)
        
        if avg_time_taken < 15:
            difficulty_shift += 20
        elif avg_time_taken > 45:
            difficulty_shift -= 20
            
        target_difficulty = round(last_question_difficulty + difficulty_shift)
        
        target_difficulty = max(500, min(target_difficulty, 2500))
        
        data.append([
            student_base_elo, 
            last_question_difficulty, 
            session_accuracy, 
            current_streak, 
            avg_time_taken, 
            target_difficulty
        ])
        
    columns = [
        'student_base_elo', 
        'last_question_difficulty', 
        'session_accuracy', 
        'current_streak', 
        'avg_time_taken', 
        'target_difficulty'
    ]
    df = pd.DataFrame(data, columns=columns)
    
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'ml_dataset.csv')
    df.to_csv(file_path, index=False)
    
    print(f"SUCCESS: Generated {num_samples} samples and saved to {file_path}")
    print(df.head(10))

if __name__ == "__main__":
    generate_cat_dataset()

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
        # 1. Randomly generate the student's starting baseline
        student_base_elo = random.randint(800, 2000)
        
        # 2. Simulate what happened in the previous question
        # Usually it's around their base elo
        last_question_difficulty = student_base_elo + random.randint(-150, 150)
        
        # 3. Simulate their performance in the current quiz session
        session_accuracy = round(random.uniform(0.2, 1.0), 2)
        
        # Streak depends heavily on accuracy. High accuracy = chance of high streak.
        if session_accuracy > 0.8:
            current_streak = random.randint(2, 8)
        elif session_accuracy > 0.5:
            current_streak = random.randint(0, 3)
        else:
            current_streak = 0
            
        avg_time_taken = random.randint(5, 60) # seconds
        
        # -------------------------------------------------------------
        # THE LOGIC WE WANT THE ML TO LEARN
        # -------------------------------------------------------------
        difficulty_shift = 0
        
        # A) Streak Bonus: The higher the streak, the harder the next question
        difficulty_shift += (current_streak * 30) 
        
        # B) Accuracy Bonus: High accuracy pushes difficulty up, low pushes it down
        # If accuracy is 100%, (1.0 - 0.5)*150 = +75
        # If accuracy is 20%, (0.2 - 0.5)*150 = -45
        difficulty_shift += ((session_accuracy - 0.5) * 150)
        
        # C) Time Bonus: Fast answers mean they find it easy. Slow means they struggle.
        if avg_time_taken < 15:
            difficulty_shift += 20  # Fast! Give a slightly harder question
        elif avg_time_taken > 45:
            difficulty_shift -= 20  # Slow! Ease up a bit
            
        # 4. Calculate the Target
        target_difficulty = round(last_question_difficulty + difficulty_shift)
        
        # Keep it within realistic bounds
        target_difficulty = max(500, min(target_difficulty, 2500))
        
        data.append([
            student_base_elo, 
            last_question_difficulty, 
            session_accuracy, 
            current_streak, 
            avg_time_taken, 
            target_difficulty
        ])
        
    # 5. Save to CSV
    columns = [
        'student_base_elo', 
        'last_question_difficulty', 
        'session_accuracy', 
        'current_streak', 
        'avg_time_taken', 
        'target_difficulty'
    ]
    df = pd.DataFrame(data, columns=columns)
    
    # Save in the same directory as this script
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'ml_dataset.csv')
    df.to_csv(file_path, index=False)
    
    print(f"SUCCESS: Generated {num_samples} samples and saved to {file_path}")
    print(df.head(10)) # Print a preview

if __name__ == "__main__":
    generate_cat_dataset()

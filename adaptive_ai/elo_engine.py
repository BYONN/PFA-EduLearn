import math

# user rating : 1500
# question difficulty : 1400
# 1 / (1 + math.pow(10, (1400-1500)/400)) = 0.64
# expected score = 0.64
# user answered correctly, actual score = 1
# new rating = 1500 + 32 * (1 -0.64) = 1511.52
def calculate_expected_score(user_rating, question_difficulty):
    """
    Calculates the probability (0.0 to 1.0) of a user answering a question correctly.
    Based on the standard chess Elo formula.
    """
    return 1 / (1 + math.pow(10, (question_difficulty - user_rating) / 400.0))

def update_user_elo(user_rating, question_difficulty, is_correct, k_factor=32):
    """
    Returns the new Elo rating for the user after attempting a question.
    
    :param user_rating: The current Elo rating of the student (e.g., 1200)
    :param question_difficulty: The Elo rating of the question (e.g., 1400)
    :param is_correct: Boolean, True if they got it right, False if wrong
    :param k_factor: How aggressively the rating changes. Default is 32.
    """
    # 1. Calculate what the system expects them to do
    expected_score = calculate_expected_score(user_rating, question_difficulty)
    
    # 2. What they actually did (1 for correct, 0 for incorrect)
    actual_score = 1 if is_correct else 0
    
    # 3. Calculate new rating
    new_rating = user_rating + k_factor * (actual_score - expected_score)
    
    return round(new_rating, 2)

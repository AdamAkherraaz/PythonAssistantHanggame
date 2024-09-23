import pandas as pd
import sys
from datetime import datetime
from collections import Counter

def main():
    if len(sys.argv) != 2:
        print("Error: missing argument")
        sys.exit(1)
    
    filename = sys.argv[1]
    df = pd.read_csv(filename, index_col=False, header=None, names=['Mot'])
    
    alphabet = list('abcdefghijklmnopqrstuvwxyz')
    random_word = df.sample().iloc[0, 0]
    random_word = random_word.lower()
    word_len = len(random_word)
    empty_case = "_"
    hash_answer = []
    split_word = [i for i in random_word]
    letter_already_used = []
    number_of_try = 0
    df_filter = df[df['Mot'].str.len() == word_len]
    
    for i in range(word_len):
        hash_answer.append(empty_case)
    
    previous_best_score = float('inf')
    
    while split_word != hash_answer and number_of_try < 20:
        for i, char in enumerate(hash_answer):
            if char != "_":
                df_filter = df_filter[df_filter['Mot'].str[i] == char]
        
        def assistant(hash_answer):
            total_letter_frequency = Counter()
            for word in df_filter['Mot'].str.lower():
                word_letter_frequency = Counter(word)
                total_letter_frequency.update(word_letter_frequency)

            found_letters = set(char for char in hash_answer if char != "_")
            letter_number = {letter: total_letter_frequency[letter] for letter in alphabet if letter not in found_letters}

            total_characters = sum(letter_number.values())
    
            if total_characters == 0:
                print("Toutes les lettres ont été trouvées ou il n'y a plus de mots correspondants.")
                return {}

            letter_frequencies_percentage = {letter: (count / total_characters) * 100 for letter, count in letter_number.items()}

            top_3_letters = sorted(letter_frequencies_percentage.items(), key=lambda x: x[1], reverse=True)[:3]

            print("Prédiction de l'assistant :")
            for letter, probability in top_3_letters:
                print(f"- Avec une probabilité de {probability:.2f}%, la lettre '{letter}' est suggérée")

            return letter_number

        assistant(hash_answer)
        
       
     
        
        print(hash_answer, " ", number_of_try, "/20")
        
        user_answer = str(input("Pick a letter ! "))
        
        if user_answer in split_word:
            for idx, letter in enumerate(split_word):
                if letter == user_answer:
                    hash_answer[idx] = user_answer
            print("Congrats ! Keep going !! Here the letters you already used :", "\n", letter_already_used)
        else:
            letter_already_used.append(user_answer)
            number_of_try += 1
            print("Nope, try again !! Here the letters you already used :", "\n", letter_already_used)
            print("number of try : ", number_of_try)
    
    if split_word == hash_answer:
        score_clean = pd.DataFrame({
            'date': [datetime.now()],
            'score': [number_of_try]
        })
        
        try:
            existing_data = pd.read_csv("score.csv")
            previous_best_score = existing_data['score'].min()
            updated_data = pd.concat([existing_data, score_clean], ignore_index=True)
        except FileNotFoundError:
            updated_data = score_clean
        
        updated_data = updated_data.sort_values(by=["score"], ascending=True)
        updated_data.to_csv("score.csv", index=False)
        
        if previous_best_score > number_of_try:
            print("Congrats ! You made a new record !!!")
        else:
            print("Good job, but not a new record.")
    else:
        print("Sorry, you've run out of tries.")

if __name__ == "__main__":
    main()
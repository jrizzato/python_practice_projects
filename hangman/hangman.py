from hangman_words import word_list
from hangman_art import stages, win, lose, welcome
from replit import clear
import random

# setup
chosen_word = random.choice(word_list)
# print(chosen_word)
placeholder = ""
game_over = False
correct_letters = []
lives = 6
primera = True

for _ in range(len(chosen_word)):
    placeholder += "_"

print(welcome)
print("\n Para ganar, adivina la palabra antes de que te cuelguen")
print("================================================================")

while not game_over:
    
    if primera:
        print(placeholder)
        print(stages[6])
        primera = False

    guess = input("Ingresa una letra: ").lower()

    clear()

    display = ""

    for letter in chosen_word:
        if letter == guess:
            display += letter
            correct_letters.append(guess)
        elif letter in correct_letters:
            display += letter
        else:
            display += "_"

    print(display)         

    if guess not in chosen_word:
        lives -= 1
    print(stages[lives])  

    if lives == 0:
        game_over = True
        print(lose)
        print(f"La palabra era {chosen_word}")

    if "_" not in display:
        game_over = True
        print(win)

    print("=============================================================================")
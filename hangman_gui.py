import tkinter as tk
from tkinter import messagebox
import random

# Category -> list of (word, clue) tuples
word_categories = {
    "Fruits": [
        ("apple", "Keeps the doctor away"),
        ("grape", "Small and used for wine"),
        ("mango", "King of fruits"),
        ("peach", "Soft fruit with fuzzy skin"),
        ("lemon", "Yellow and sour"),
        ("guava", "Rich in Vitamin C"),
        ("melon", "Large and juicy summer fruit")
    ],
    "Animals": [
        ("tiger", "Striped big cat"),
        ("zebra", "Horse with stripes"),
        ("panda", "Eats bamboo"),
        ("koala", "Australian tree-hugger"),
        ("moose", "Large antlered animal"),
        ("sheep", "Gives wool"),
        ("horse", "Used for riding")
    ],
    "Countries": [
        ("spain", "Famous for flamenco"),
        ("egypt", "Land of pyramids"),
        ("india", "Home to the Taj Mahal"),
        ("japan", "Land of the rising sun"),
        ("ghana", "West African nation"),
        ("nepal", "Home of Mount Everest"),
        ("italy", "Famous for pasta and pizza")
    ]
}

# Global state
word_list = []
current_index = 0
word = ""
clue = ""
guessed_letters = []
wrong_guesses = 0
max_guesses = 6
display_word = []

# Draw hangman
def draw_hangman(stage):
    canvas.delete("all")
    canvas.create_line(20, 180, 180, 180, width=2)
    canvas.create_line(50, 180, 50, 20, width=2)
    canvas.create_line(50, 20, 120, 20, width=2)
    canvas.create_line(120, 20, 120, 40, width=2)

    if stage > 0:
        canvas.create_oval(100, 40, 140, 80, width=2)
    if stage > 1:
        canvas.create_line(120, 80, 120, 130, width=2)
    if stage > 2:
        canvas.create_line(120, 90, 90, 110, width=2)
    if stage > 3:
        canvas.create_line(120, 90, 150, 110, width=2)
    if stage > 4:
        canvas.create_line(120, 130, 90, 160, width=2)
    if stage > 5:
        canvas.create_line(120, 130, 150, 160, width=2)

# Start or continue game
def start_next_word():
    global current_index, word, clue, display_word, guessed_letters, wrong_guesses

    if current_index >= len(word_list):
        ask_to_continue()
        return

    word, clue = word_list[current_index]
    current_index += 1
    display_word = ["_" for _ in word]
    guessed_letters = []
    wrong_guesses = 0

    clue_label.config(text="💡 Clue: " + clue)
    entry.config(state='normal')
    guess_button.config(state='normal')
    draw_hangman(wrong_guesses)
    update_display()
    result_label.config(text="")
    entry.focus()

# Ask if user wants to play again
def ask_to_continue():
    response = messagebox.askyesno("Play Again?", "🎉 You've completed this category!\nDo you want to play again?")
    if response:
        game_frame.pack_forget()
        category_frame.pack()
    else:
        root.destroy()

# Process guess
def make_guess():
    global wrong_guesses
    guess = entry.get().lower()
    entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        result_label.config(text="⚠️ Enter one letter.")
        return

    if guess in guessed_letters:
        result_label.config(text="⚠️ Already guessed.")
        return

    guessed_letters.append(guess)

    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                display_word[i] = guess
        result_label.config(text="✅ Correct!")
    else:
        wrong_guesses += 1
        draw_hangman(wrong_guesses)
        result_label.config(text=f"❌ Wrong! {max_guesses - wrong_guesses} left.")

    update_display()

    if "_" not in display_word:
        result_label.config(text=f"🎉 Correct! The word was '{word}'.")
        root.after(1500, start_next_word)
    elif wrong_guesses >= max_guesses:
        result_label.config(text=f"💀 Game Over! The word was '{word}'.")
        root.after(1500, start_next_word)

# Update display
def update_display():
    word_label.config(text="Word: " + " ".join(display_word))
    letters_label.config(text="Guessed: " + ", ".join(guessed_letters))

# Handle category selection
def select_category(cat):
    global word_list, current_index
    category_frame.pack_forget()
    game_frame.pack()
    word_list = random.sample(word_categories[cat], len(word_categories[cat]))  # Shuffle words
    current_index = 0
    start_next_word()

# GUI setup
root = tk.Tk()
root.title("🎯 Hangman Game with Categories & Clues")
root.geometry("430x550")
root.resizable(False, False)

# Category screen
category_frame = tk.Frame(root)
category_frame.pack(pady=30)

tk.Label(category_frame, text="Select a Category", font=("Helvetica", 16)).pack(pady=10)

for cat in word_categories:
    tk.Button(category_frame, text=cat, width=20, command=lambda c=cat: select_category(c)).pack(pady=5)

# Game screen
game_frame = tk.Frame(root)

canvas = tk.Canvas(game_frame, width=200, height=200)
canvas.pack(pady=10)

clue_label = tk.Label(game_frame, text="", font=("Helvetica", 12), fg="blue")
clue_label.pack(pady=5)

word_label = tk.Label(game_frame, text="", font=("Courier", 18))
word_label.pack()

letters_label = tk.Label(game_frame, text="", font=("Helvetica", 12))
letters_label.pack()

entry = tk.Entry(game_frame, font=("Helvetica", 14), width=5, justify='center')
entry.pack(pady=10)
entry.bind("<Return>", lambda event: make_guess())  # 🔥 Enter key triggers guess

guess_button = tk.Button(game_frame, text="Guess", command=make_guess)
guess_button.pack()

result_label = tk.Label(game_frame, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

root.mainloop()

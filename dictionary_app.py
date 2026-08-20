import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
import pyttsx3



DICTIONARY_API = "https://api.dictionaryapi.dev/api/v2/entries/en/"
SUGGESTION_API = "https://api.datamuse.com/words"

HISTORY_FILE = "search_history.json"




engine = pyttsx3.init()
engine.setProperty("rate", 150)




def save_history(word):

    history = []

    if os.path.exists(HISTORY_FILE):

        try:
            with open(HISTORY_FILE, "r") as file:
                history = json.load(file)

        except:
            history = []

    if word not in history:
        history.append(word)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)




def pronounce_word():

    word = word_entry.get().strip()

    if word == "":
        messagebox.showwarning(
            "Warning",
            "Please enter a word first."
        )
        return

    try:

        engine.say(word)
        engine.runAndWait()

    except:

        messagebox.showerror(
            "Error",
            "Unable to pronounce the word."
        )



def generate_example(word):

    examples = {

        "happy":
        "She felt happy after receiving the good news.",

        "sad":
        "He felt sad when his friend left.",

        "beautiful":
        "The garden looks beautiful in the morning.",

        "computer":
        "I use a computer to complete my work.",

        "education":
        "Education plays an important role in our lives.",

        "technology":
        "Technology has changed the way we live.",

        "school":
        "The students go to school every morning.",

        "student":
        "The student is studying for the examination.",

        "book":
        "I read a book before going to bed.",

        "friend":
        "My friend helped me with my homework.",

        "water":
        "We should drink enough water every day.",

        "food":
        "The food smells delicious.",

        "important":
        "Time is very important in our life.",

        "success":
        "Hard work is the key to success.",

        "knowledge":
        "Reading books increases our knowledge.",

        "programming":
        "I enjoy learning programming.",

        "python":
        "Python is a popular programming language.",

        "car":
        "My father drives a car to work.",

        "house":
        "They live in a beautiful house.",

        "book":
        "She is reading a book.",

        "love":
        "I love spending time with my family.",

        "learn":
        "I want to learn something new every day.",

        "run":
        "He likes to run in the morning.",

        "beautiful":
        "The flowers in the garden are beautiful.",

        "strong":
        "The athlete is strong and energetic.",

        "fast":
        "The car is moving very fast.",

        "good":
        "She is a good student.",

        "bad":
        "It was a bad experience.",

        "easy":
        "This question is easy to solve.",

        "difficult":
        "This problem is difficult to understand."
    }

    word_lower = word.lower()

    if word_lower in examples:
        return examples[word_lower]

    return (
        f"The word '{word}' is used in this example sentence."
    )




def search_word():

    word = word_entry.get().strip().lower()

    if word == "":

        messagebox.showwarning(
            "Warning",
            "Please enter an English word."
        )

        return

    result_text.delete(
        "1.0",
        tk.END
    )

    try:

       
        response = requests.get(
            DICTIONARY_API + word,
            timeout=8
        )

        

        if response.status_code != 200:

            show_suggestions(word)

            return

        data = response.json()[0]

       
        result_text.insert(
            tk.END,
            "WORD\n",
            "heading"
        )

        result_text.insert(
            tk.END,
            data.get(
                "word",
                word
            ).capitalize()
            + "\n\n"
        )

        # =================================================
        # MEANING
        # =================================================

        result_text.insert(
            tk.END,
            "MEANING\n",
            "heading"
        )

        meanings = data.get(
            "meanings",
            []
        )

        all_examples = []

        for meaning in meanings:

            definitions = meaning.get(
                "definitions",
                []
            )

            for i, definition in enumerate(
                definitions[:3],
                start=1
            ):

                definition_text = definition.get(
                    "definition",
                    "Definition not available."
                )

                result_text.insert(
                    tk.END,
                    f"{i}. {definition_text}\n"
                )

                # -----------------------------------------
                # API EXAMPLE
                # -----------------------------------------

                api_example = definition.get(
                    "example"
                )

                if api_example:

                    all_examples.append(
                        api_example
                    )

        result_text.insert(
            tk.END,
            "\n"
        )

        # =================================================
        # EXAMPLE SENTENCE
        # =================================================

        result_text.insert(
            tk.END,
            "EXAMPLE SENTENCE\n",
            "heading"
        )

        if all_examples:

            for example in all_examples[:2]:

                result_text.insert(
                    tk.END,
                    "• " + example + "\n",
                    "example"
                )

        else:

            generated_example = generate_example(
                word
            )

            result_text.insert(
                tk.END,
                "• " + generated_example + "\n",
                "example"
            )

        result_text.insert(
            tk.END,
            "\n"
        )

        # =================================================
        # SYNONYMS
        # =================================================

        synonyms = set()

        for meaning in meanings:

            for synonym in meaning.get(
                "synonyms",
                []
            ):

                synonyms.add(
                    synonym
                )

            for definition in meaning.get(
                "definitions",
                []
            ):

                for synonym in definition.get(
                    "synonyms",
                    []
                ):

                    synonyms.add(
                        synonym
                    )

        result_text.insert(
            tk.END,
            "SYNONYMS\n",
            "heading"
        )

        if synonyms:

            result_text.insert(
                tk.END,
                ", ".join(
                    sorted(synonyms)[:15]
                )
                + "\n\n"
            )

        else:

            result_text.insert(
                tk.END,
                "Not available\n\n"
            )

        # =================================================
        # ANTONYMS
        # =================================================

        antonyms = set()

        for meaning in meanings:

            for antonym in meaning.get(
                "antonyms",
                []
            ):

                antonyms.add(
                    antonym
                )

            for definition in meaning.get(
                "definitions",
                []
            ):

                for antonym in definition.get(
                    "antonyms",
                    []
                ):

                    antonyms.add(
                        antonym
                    )

        result_text.insert(
            tk.END,
            "ANTONYMS\n",
            "heading"
        )

        if antonyms:

            result_text.insert(
                tk.END,
                ", ".join(
                    sorted(antonyms)[:15]
                )
                + "\n\n"
            )

        else:

            result_text.insert(
                tk.END,
                "Not available\n\n"
            )

        # =================================================
        # SAVE HISTORY
        # =================================================

        save_history(word)

        status_label.config(
            text=f"Results found for: {word}"
        )

    except requests.exceptions.RequestException:

        messagebox.showerror(
            "Network Error",
            "Please check your internet connection."
        )

        status_label.config(
            text="Network error!"
        )


# =========================================================
# WORD SUGGESTIONS
# =========================================================

def show_suggestions(word):

    result_text.delete(
        "1.0",
        tk.END
    )

    result_text.insert(
        tk.END,
        "❌ WORD NOT FOUND\n\n",
        "error"
    )

    result_text.insert(
        tk.END,
        f"We could not find: {word}\n\n"
    )

    result_text.insert(
        tk.END,
        "💡 DID YOU MEAN?\n\n",
        "heading"
    )

    try:

        response = requests.get(
            SUGGESTION_API,
            params={
                "sp": word,
                "max": 8
            },
            timeout=5
        )

        suggestions = response.json()

        if suggestions:

            for item in suggestions:

                suggestion = item.get(
                    "word",
                    ""
                )

                result_text.insert(
                    tk.END,
                    "• " + suggestion + "\n"
                )

        else:

            result_text.insert(
                tk.END,
                "No suggestions found."
            )

        status_label.config(
            text="Word not found. Suggestions displayed."
        )

    except:

        result_text.insert(
            tk.END,
            "Unable to load suggestions."
        )


# =========================================================
# CLEAR SEARCH
# =========================================================

def clear_search():

    word_entry.delete(
        0,
        tk.END
    )

    result_text.delete(
        "1.0",
        tk.END
    )

    status_label.config(
        text="Ready to search..."
    )

    word_entry.focus()


# =========================================================
# SHOW HISTORY
# =========================================================

def show_history():

    result_text.delete(
        "1.0",
        tk.END
    )

    result_text.insert(
        tk.END,
        "📚 SEARCH HISTORY\n\n",
        "heading"
    )

    if not os.path.exists(
        HISTORY_FILE
    ):

        result_text.insert(
            tk.END,
            "No search history available."
        )

        return

    try:

        with open(
            HISTORY_FILE,
            "r"
        ) as file:

            history = json.load(file)

        if history:

            for i, word in enumerate(
                history,
                start=1
            ):

                result_text.insert(
                    tk.END,
                    f"{i}. {word}\n"
                )

        else:

            result_text.insert(
                tk.END,
                "No searches yet."
            )

    except:

        result_text.insert(
            tk.END,
            "Unable to read history."
        )


# =========================================================
# CLEAR HISTORY
# =========================================================

def clear_history():

    if os.path.exists(
        HISTORY_FILE
    ):

        try:

            os.remove(
                HISTORY_FILE
            )

            result_text.delete(
                "1.0",
                tk.END
            )

            result_text.insert(
                tk.END,
                "Search history cleared successfully.",
                "success"
            )

        except:

            messagebox.showerror(
                "Error",
                "Unable to clear history."
            )

    else:

        messagebox.showinfo(
            "History",
            "No history found."
        )


# =========================================================
# ENTER KEY
# =========================================================

def enter_search(event):

    search_word()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "English Dictionary Application"
)

root.geometry(
    "900x700"
)

root.minsize(
    750,
    600
)

root.configure(
    bg="#eef2ff"
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg="#4f46e5",
    height=105
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


title = tk.Label(
    header,
    text="📖 English Dictionary",
    font=("Arial", 28, "bold"),
    bg="#4f46e5",
    fg="white"
)

title.pack(
    pady=(15, 2)
)


subtitle = tk.Label(
    header,
    text="Search • Learn • Listen • Improve",
    font=("Arial", 11),
    bg="#4f46e5",
    fg="#e0e7ff"
)

subtitle.pack()


# =========================================================
# SEARCH FRAME
# =========================================================

search_frame = tk.Frame(
    root,
    bg="#eef2ff"
)

search_frame.pack(
    pady=20
)


word_entry = tk.Entry(
    search_frame,
    font=("Arial", 16),
    width=34,
    bd=2,
    relief="solid"
)

word_entry.grid(
    row=0,
    column=0,
    padx=6
)


search_button = tk.Button(
    search_frame,
    text="🔍 Search",
    font=("Arial", 12, "bold"),
    bg="#4f46e5",
    fg="white",
    padx=16,
    pady=9,
    bd=0,
    command=search_word
)

search_button.grid(
    row=0,
    column=1,
    padx=4
)


speak_button = tk.Button(
    search_frame,
    text="🔊 Pronounce",
    font=("Arial", 12, "bold"),
    bg="#059669",
    fg="white",
    padx=16,
    pady=9,
    bd=0,
    command=pronounce_word
)

speak_button.grid(
    row=0,
    column=2,
    padx=4
)


# =========================================================
# BUTTON FRAME
# =========================================================

button_frame = tk.Frame(
    root,
    bg="#eef2ff"
)

button_frame.pack(
    pady=3
)


clear_button = tk.Button(
    button_frame,
    text="🗑 Clear",
    font=("Arial", 11, "bold"),
    bg="#ef4444",
    fg="white",
    padx=20,
    pady=7,
    bd=0,
    command=clear_search
)

clear_button.grid(
    row=0,
    column=0,
    padx=5
)


history_button = tk.Button(
    button_frame,
    text="📚 History",
    font=("Arial", 11, "bold"),
    bg="#f59e0b",
    fg="white",
    padx=20,
    pady=7,
    bd=0,
    command=show_history
)

history_button.grid(
    row=0,
    column=1,
    padx=5
)


clear_history_button = tk.Button(
    button_frame,
    text="❌ Clear History",
    font=("Arial", 11, "bold"),
    bg="#7c3aed",
    fg="white",
    padx=20,
    pady=7,
    bd=0,
    command=clear_history
)

clear_history_button.grid(
    row=0,
    column=2,
    padx=5
)


# =========================================================
# RESULT FRAME
# =========================================================

result_frame = tk.Frame(
    root,
    bg="white",
    bd=2,
    relief="solid"
)

result_frame.pack(
    padx=30,
    pady=15,
    fill="both",
    expand=True
)


result_text = tk.Text(
    result_frame,
    font=("Arial", 12),
    wrap="word",
    padx=20,
    pady=15,
    bg="white",
    fg="#1f2937",
    bd=0
)

result_text.pack(
    side="left",
    fill="both",
    expand=True
)


# =========================================================
# SCROLLBAR
# =========================================================

scrollbar = tk.Scrollbar(
    result_frame,
    command=result_text.yview
)

scrollbar.pack(
    side="right",
    fill="y"
)

result_text.config(
    yscrollcommand=scrollbar.set
)


# =========================================================
# TEXT STYLES
# =========================================================

result_text.tag_config(
    "heading",
    font=("Arial", 14, "bold"),
    foreground="#4f46e5"
)

result_text.tag_config(
    "example",
    font=("Arial", 12, "italic"),
    foreground="#7c3aed"
)

result_text.tag_config(
    "error",
    font=("Arial", 17, "bold"),
    foreground="#dc2626"
)

result_text.tag_config(
    "success",
    font=("Arial", 14, "bold"),
    foreground="#059669"
)


# =========================================================
# STATUS LABEL
# =========================================================

status_label = tk.Label(
    root,
    text="Ready to search...",
    font=("Arial", 10),
    bg="#eef2ff",
    fg="#6b7280"
)

status_label.pack(
    pady=(0, 8)
)


# =========================================================
# ENTER KEY
# =========================================================

word_entry.bind(
    "<Return>",
    enter_search
)


# =========================================================
# START
# =========================================================

word_entry.focus()

root.mainloop()
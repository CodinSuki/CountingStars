import re 
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import ImageTk
import tkinter.messagebox as messagebox
import nltk
from nltk.corpus import words
from nltk.corpus import wordnet

nltk.download("words")
nltk.download("wordnet")

class SpellingChecker:
    def __init__(self):
        #Code for window
        self.root = tk.Tk()
        self.root.iconbitmap("IMAGES/shabugods.ico")
        self.root.geometry("800x600")
        self.root.configure(bg="lightgrey") 
        self.root.title("Counting Stars: Spelling Checker")
        
        photo_image = tk.PhotoImage(file="IMAGES/wooden.png")
        bg_label = tk.Label(self.root, image=photo_image)
        bg_label.place(relwidth=1, relheight=1)
        
        #Code for Scroll text
        self.text = ScrolledText(self.root, font=("Arial", 14))
        self.text.bind("<KeyRelease>", self.check)
        self.text.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)      
        
        #Code for text view add custom word bar
        self.custom_words_entry = tk.Entry(self.root, font=("Arial", 12))
        self.custom_words_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")  

        #Code for text add custom word button
        self.add_word_button = tk.Button(self.root, text="Add Custom Word", command=self.add_custom_word)
        self.add_word_button.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew") 

        #Code for text view delete custom word bar
        self.delete_custom_words_entry = tk.Entry(self.root, font=("Arial", 12))
        self.delete_custom_words_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")  

        #Code for text delete custom word button
        self.delete_word_button = tk.Button(self.root, text="Delete Custom Word", command=self.delete_custom_word)
        self.delete_word_button.grid(row=2, column=1, padx=10, pady=(0, 10), sticky="ew") 
        
        #Code for text view custom words button
        self.show_custom_words_button = tk.Button(self.root, text="Show Custom Words", command=self.show_custom_words)
        self.show_custom_words_button.grid(row=2, column=2, padx=10, pady=(0, 10), sticky="ew")

        self.old_spaces = 0 
        self.custom_words = set() # Set to store custom words 
        
        # Load custom words from file
        self.load_custom_words()
        
        # Counters 
        self.word_count_label = tk.Label(self.root, text="Word Count: 0")
        self.word_count_label.grid(row=5, column=5, columnspan=2, sticky="nw")  
        
        self.char_count_label = tk.Label(self.root, text="Character Count: 0")
        self.char_count_label.grid(row=6, column=5, columnspan=2, sticky="nw") 
        
        self.root.grid_rowconfigure(0, weight=1)  
        self.root.grid_columnconfigure(0, weight=1)  
        
        self.root.mainloop()
        
    def update_counts(self): # Code to count the number of words and characters 
        content = self.text.get("1.0", tk.END)
        word_count = len(re.findall(r'\w+', content))
        char_count = len(content) - content.count('\n')  # Subtracting newline characters
        
        self.word_count_label.config(text=f"Word Count: {word_count}")
        self.char_count_label.config(text=f"Character Count: {char_count}")
        
    def check(self, event): # Code to check the spelling
        self.update_counts()

        content = self.text.get("1.0", tk.END)
        space_count = content.count(" ")

        if space_count != self.old_spaces:
            self.old_spaces = space_count
            
            for tag in self.text.tag_names():
                self.text.tag_delete(tag)
            
            for word in content.split():
                cleaned_word = re.sub(r"[^\w]", "", word.lower())
                if cleaned_word not in words.words() and cleaned_word not in self.custom_words:
                    position = content.find(word)
                    self.text.tag_add(cleaned_word, f"1.{position}", f"1.{position + len(word)}")
                    self.text.tag_config(cleaned_word, foreground="red")


    def add_custom_word(self): # Code to add a custom word
        custom_word = self.custom_words_entry.get().strip().lower()
        if custom_word:
            self.custom_words.add(custom_word)
            self.save_custom_words()
            self.custom_words_entry.delete(0, tk.END)

    def delete_custom_word(self): # Code to delete a custom word
        custom_word = self.delete_custom_words_entry.get().strip().lower()
        if custom_word in self.custom_words:
            self.custom_words.remove(custom_word)
            self.save_custom_words()
            self.delete_custom_words_entry.delete(0, tk.END)

    def show_custom_words(self): 
        if self.custom_words: 
            custom_words_str = "\n".join(sorted(self.custom_words)) 
            messagebox.showinfo("Custom Words", f"Custom Words:\n{custom_words_str}") 
        else: 
            messagebox.showinfo("Custom Words", "No custom words added yet.") 
    def save_custom_words(self): 
        with open("custom_words.txt", "w") as file: 
            for word in self.custom_words: 
                file.write(word + "\n") 
                
    def load_custom_words(self): 
        try: 
            with open("custom_words.txt", "r") as file: 
                self.custom_words = set(word.strip().lower() for word in file.readlines()) 
        except FileNotFoundError: 
            # If the file does not exist, create it 
            open("custom_words.txt", "w").close()  # Create an empty file 



SpellingChecker() 


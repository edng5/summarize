# Summarize by Edward Ng
# Summarizes text and extracts the key information. Supports PDF, websites and audio file inputs.
# 1/22/2023

from newspaper import Article
import spacy, speech_recognition
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader


def summarize(text: str, per: float) -> str:
    '''
    Takes in text and a percentge and summarizes the text to highlight key information.
    text: The text to summarize.
    per: percentage of sentence.
    :returns: string of summarized text.
    '''
    # load English pipeline
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]

    # normalize word frequencies and rank sentences to find importance
    word_freq={}
    for word in doc:
        # filter out STOP_WORDS
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
    max_freq=max(word_freq.values())
    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq
    sentence_tokens= [sentence for sentence in doc.sents]
    sentence_scores = {}
    for sentence in sentence_tokens:
        for word in sentence:
            if word.text.lower() in word_freq.keys():
                if sentence not in sentence_scores.keys():                            
                    sentence_scores[sentence]=word_freq[word.text.lower()]
                else:
                    sentence_scores[sentence]+=word_freq[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary='\n'.join(final_summary)
    return summary 


def extract_text(path: str) -> str:
    '''
    Takes in a path or url to a source and maps document format to extract text properly.
    :path - a url or path to a source to extract text from.
    :return: string of text to process on.
    '''
    # TODO: add pdf, video and audio mapping
    if path[:3] in 'http':
        article = Article(path)
        article.download()
        article.parse()
        return article.text
    elif path[-3:] in 'txt':
        with open(path, 'r') as f:
            text = f.read()
        return text
    elif path[-3:] in 'pdf':
        reader = PdfReader(path)
        page = reader.pages[0]
        text = page.extract_text()
        # text = ''
        # for page in reader.pages:
            # text = text + page.extract_text()
        return text


def browseFiles() -> None:
    '''
    Opens a file browser.0
    :returns: None
    '''
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.txt*"),
                                                       ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

    path = filename
    text = extract_text(path)
    text = (summarize(text,  0.20))
    summary.configure(text=text)


if __name__ == "__main__":
    # url = 'https://www.sciencedirect.com/science/article/pii/S2590005622000595'
    url = 'https://www.sciencedaily.com/releases/2021/08/210811162816.htm'

    # GUI Components
    window = tk.Tk()

    label_file_explorer = tk.Label(window,
                            text = "Summarize",
                            width = 100, height = 4,
                            fg = "blue")
    label_file_explorer.pack()

    button_explore = tk.Button(window,
                        text = "Browse Files",
                        command = browseFiles)
  
    button_exit = tk.Button(window,
                     text = "Exit",
                     command = exit)

    label_file_explorer.grid(column = 1, row = 1)
  
    button_explore.grid(column = 1, row = 2)
    
    button_exit.grid(column = 1,row = 3)

    summary = tk.Label(window, text='')
    summary.grid(column = 1, row = 4)

    window.mainloop()

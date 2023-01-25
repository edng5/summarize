# Summarize by Edward Ng
# Summarizes text and extracts the key information. Supports PDF, websites and audio file inputs.
# 1/22/2023

from newspaper import Article
import spacy, PyPDF2, speech_recognition
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import tkinter as tk


def summarize(text: str, per: float) -> str:
    '''
    Takes in text and a percentge and summarizes the text to highlight key information.
    text: The text to summarize.
    per: percentage of sentence.
    Returns string.
    '''
    # load English pipeline
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]

    # Find word frequencies and rank sentences to find importance
    word_frequencies={}
    for word in doc:
        # filter out STOP_WORDS
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sentence for sentence in doc.sents]
    sentence_scores = {}
    for sentence in sentence_tokens:
        for word in sentence:
            if word.text.lower() in word_frequencies.keys():
                if sentence not in sentence_scores.keys():                            
                    sentence_scores[sentence]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sentence]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary='\n'.join(final_summary)
    return summary 

if __name__ == "__main__":
    url = 'https://www.sciencedaily.com/releases/2021/08/210811162816.htm'
    article = Article(url)
    article.download()
    article.parse()

    print(article.text)
    print(summarize(article.text, 0.1))

    # GUI Components
    window = tk.Tk()

    frame_a = tk.Frame()
    frame_b = tk.Frame()
    frame_c = tk.Frame()

    label_a = tk.Label(master=frame_a, text="Summarize")
    label_a.pack()

    label_b = tk.Label(master=frame_b, text=article.text)
    label_b.pack()

    label_c = tk.Label(master=frame_c, text=summarize(article.text, 0.05))
    label_c.pack()

    frame_a.pack()
    frame_b.pack()
    frame_c.pack()

    window.mainloop()

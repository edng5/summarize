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
from tkPDFViewer import tkPDFViewer as pdf

from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline


def text_rank_summarize(text: str, per: float) -> str:
    '''
    Uses the text rank algorithm to produce an extractive text summarization.
    text: The text to summarize.
    per: percentage of sentence.
    :returns: string of summarized text.
    '''
    # load English pipeline
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    # tokens=[token.text for token in doc]

    # normalize word frequencies and rank sentences to find importance
    word_freq={}
    for word in doc:
        # filter out STOP_WORDS
        if word.text.lower() not in list(STOP_WORDS) and word.text.lower() not in punctuation:
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


def pegasus_summarize(text: str) -> str:
    '''
    Uses Pegasus pretrained model to produce abstractive text summarization.
    :text - the text to summarize
    :returns: string of summarized text.
    '''
    model = "google/pegasus-xsum"
    pegasus_tokenizer = PegasusTokenizer.from_pretrained(model)

    # Define PEGASUS model
    pegasus_model = PegasusForConditionalGeneration.from_pretrained(model)

    # Create tokens
    tokens = pegasus_tokenizer(text, truncation=True, padding="longest", return_tensors="pt")

    # Summarize text
    encoded_summary = pegasus_model.generate(**tokens)

    # Decode summarized text
    decoded_summary = pegasus_tokenizer.decode(
        encoded_summary[0],
        skip_special_tokens=True
    )

    # Define summarization pipeline 
    summarizer = pipeline(
        "summarization", 
        model=model, 
        tokenizer=pegasus_tokenizer, 
        framework="pt"
    )

    summary = summarizer(text, min_length=30, max_length=150)

    return summary[0]["summary_text"]


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
    Opens a file browser.
    :returns: None
    '''
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files",
                                                        "*.*"), ("all files",
                                                        "*.*")))
      
    # Change label contents
    label_file_explorer.configure(text="File Opened: "+filename)

    path = filename
    text = extract_text(path)
    text = (text_rank_summarize(text,  0.20))
    # can only pass a max length in pegasus?
    # text = pegasus_summarize(text)
    summary.configure(text=text)
    # v1.pdf_view(page_frame,
    #              pdf_location = filename, 
    #              width = 75, height = 100)


if __name__ == "__main__":
    # url = 'https://www.sciencedirect.com/science/article/pii/S2590005622000595'
    url = 'https://www.sciencedaily.com/releases/2021/08/210811162816.htm'

    # GUI Components
    root = tk.Tk()

    root.geometry("1080x1080")

    page_frame = tk.Frame(root,  width=75,  height=100,  bg='grey')
    page_frame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)
    work_frame = tk.Frame(root,  width=50,  height=100)
    work_frame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)


    label_file_explorer = tk.Label(work_frame,
                            text = "Summarize",
                            width = 100, height = 4,
                            fg = "blue")
    label_file_explorer.pack(side="top")

    button_explore = tk.Button(work_frame,
                        text = "Browse Files",
                        command = browseFiles)
  
    button_exit = tk.Button(work_frame,
                     text = "Exit",
                     command = exit)

    label_file_explorer.pack(side="top")
  
    button_explore.pack(side="right")
    
    button_exit.pack(side="left")

    summary = tk.Label(work_frame, text='')
    summary.pack(side="bottom")

    v1 = pdf.ShowPdf()

    filename = r"E:\Downloads\1-s2.0-S2590005622000595-main.pdf"
    pdf_viewer = v1.pdf_view(page_frame,
                 pdf_location = filename, 
                 width = 75, height = 100)

    #destroy and recreate to refresh the pdf viewer
    # if FLAG == 1:
    #     pdf_viewer.destroy()
    #     pdf_viewer = v1.pdf_view(page_frame,
    #              pdf_location = filename, 
    #              width = 75, height = 100)

    pdf_viewer.pack(side="left")

    root.mainloop()

from transformers import PegasusForConditionalGeneration
from transformers import PegasusTokenizer
from transformers import pipeline

from PyPDF2 import PdfReader

from newspaper import Article
import spacy, speech_recognition
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest



def text_rank_summarize(text: str, per: float) -> str:
    '''
    Uses the text rank algorithm to produce an extractive text summarization.
    :param text: The text to summarize.
    :param per: percentage of sentence.
    :return: string of summarized text.
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
    :param text: the text to summarize
    :return: string of summarized text.
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
    :param path: a url or path to a source to extract text from.
    :return: string of text to process on.
    '''
    # TODO: add pdf, video and audio mapping
    if not path:
        return ''
    elif path[:3] in 'http':
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

def get_file_type(path: str) -> str:
    '''
    Takes in a path or url to a source and maps identifies the file type.
    :param path: a url or path to a source.
    :return: string of file type.
    '''
    if not path:
        return ''
    elif path[:3] in 'http':
        return "Website"
    elif path[-3:] in 'txt':
        return "Text File"
    elif path[-3:] in 'pdf':
        return "PDF File"

# Summarize by Edward Ng
# Summarizes text and extracts the key information. Supports PDF, websites and audio file inputs.
# 1/22/2023

import tkinter as tk
from tkinter import filedialog
# from utils import run
from tkPDFViewer import tkPDFViewer as pdf

from utils import *

def browseFiles() -> None:
    '''
    Opens a file browser.
    :return: None
    '''
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("all files",
                                                        "*.*"), ("all files",
                                                        "*.*")))
      
    # Change label contents
    text_file.insert("1.0", filename)
    file_type = get_file_type(filename)
    label_file_type.configure(text="File Type: "+ file_type)
    # text = extract_text(filename)
    # text = (text_rank_summarize(text,  0.20))
    # can only pass a max length 512 in pegasus?
    # text = pegasus_summarize(text)
    # summary.configure(text=text)
    open_pdf(filename)

def open_pdf(file: str) -> None:
    '''
    Refreshes PDF Viewer to display the current PDF.
    :param file: string of file path.
    :return: None 
    '''
    global v2

    if file:
        # if old instance exists, destroy it first
        if v2:
            v2.destroy()
        v1 = pdf.ShowPdf()
        # clear the stored image list
        v1.img_object_li.clear()
        # shows the new images extracted from PDF file
        v2 = v1.pdf_view(page_frame, pdf_location=file, width=75, height=100) # smaller height
        v2.pack()


#===================================================MAIN============================================================#

if __name__ == "__main__":
    # url = 'https://www.sciencedirect.com/science/article/pii/S2590005622000595'
    # url = 'https://www.sciencedaily.com/releases/2021/08/210811162816.htm'

    # GUI Components
    root = tk.Tk()
    root.title("Summarize")
    root.geometry("1080x1080")

    # Frame containers
    page_frame = tk.Frame(root,  width=75,  height=100,  bg='grey')
    page_frame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)
    work_frame = tk.Frame(root,  width=50,  height=100)
    work_frame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)

    top_frame = tk.Frame(work_frame,  width=50,  height=90)
    work_frame.pack(side='top',  fill='both',  expand=True)
    bottom_frame = tk.Frame(work_frame,  width=50,  height=10)
    work_frame.pack(side='bottom',  fill='both',  expand=True)

    # Label components
    label_file_type = tk.Label(work_frame,
                            text = "",
                            width = 100, height = 4,
                            fg = "blue")

    # Text Field
    text_file = tk.Text(work_frame)
    
    text_first_page = tk.Text(work_frame)
    text_last_page = tk.Text(work_frame)

    # Button Components
    button_explore = tk.Button(work_frame,
                        text = "Browse Files",
                        command = browseFiles)
  
    button_summarize = tk.Button(work_frame,
                     text = "Summarize",
                     command = exit)

    button_settings = tk.Button(work_frame,
                     text = "Settings",
                     command = exit)

    button_speech = tk.Button(work_frame,
                     text = "Speech",
                     command = exit)

    button_save = tk.Button(work_frame,
                     text = "Save",
                     command = exit)

    # PDF Viewer Component
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(page_frame, pdf_location='', width=75, height=100) # smaller height

    # Pack components
    label_file_type.pack(side="top")
  
    button_explore.pack(side="right")

    text_file.pack()
    
    text_first_page.pack()

    text_last_page.pack()

    button_summarize.pack()

    button_settings.pack()

    button_speech.pack()

    button_save.pack()

    v2.pack()
    
    root.mainloop()

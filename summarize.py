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
    if button_explore.cget('text') == "Browse Files":
        filename = filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("all files",
                                                            "*.*"), ("all files",
                                                            "*.*")))
        
        # Change label contents
        text_file.delete("1.0","end")
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
    global pdf_viewer

    if file:
        # if old instance exists, destroy it first
        if pdf_viewer:
            pdf_viewer.destroy()
        view = pdf.ShowPdf()
        # clear the stored image list
        view.img_object_li.clear()
        # shows the new images extracted from PDF file
        pdf_viewer = view.pdf_view(page_frame, pdf_location=file, width=75, height=100) # smaller height
        pdf_viewer.pack()


def detect_file_path() -> None:
    '''
    Keep Browse Button updated to searching or browsing.
    :return: None
    '''
    path = text_file.get("1.0", "end")
    print(path)
    if get_file_type(path) == "Website":
        button_explore["text"]="Search"
    else:
        button_explore["text"]="Browse Files"


#===================================================MAIN============================================================#

if __name__ == "__main__":
    # url = 'https://www.sciencedirect.com/science/article/pii/S2590005622000595'
    # url = 'https://www.sciencedaily.com/releases/2021/08/210811162816.htm'

    # GUI Components
    root = tk.Tk()
    root.title("Summarize")
    root.geometry("1920x1080")

    # Frame containers
    page_frame = tk.Frame(root,  width=80,  height=100,  bg='grey')
    page_frame.pack(side='left',  fill='both',  padx=10,  pady=5,  expand=True)
    work_frame = tk.Frame(root,  width=50,  height=100)
    work_frame.pack(side='right',  fill='both',  padx=10,  pady=5,  expand=True)

    # Label components
    label_file_type = tk.Label(work_frame,
                            text = "File Type:",
                            width = 50, height = 4,
                            fg = "blue")
    label_file_type.pack()

    top_frame = tk.Frame(work_frame,  width=40,  height=2)
    top_frame.pack()

    center_frame = tk.Frame(work_frame,  width=40,  height=2)
    center_frame.pack()

    center2_frame = tk.Frame(work_frame,  width=40,  height=2)
    center2_frame.pack()

    bottom_frame = tk.Frame(work_frame,  width=40,  height=2)
    bottom_frame.pack()

    top_left_frame = tk.Frame(top_frame,  width=40,  height=2)
    top_left_frame.pack(side="left", fill='both',  expand=True)
    top_right_frame = tk.Frame(top_frame,  width=10,  height=2)
    top_right_frame.pack(side="right", fill='both',  expand=True)

    center_left_frame = tk.Frame(center_frame,  width=25,  height=5)
    center_left_frame.pack(side="left", fill='both',  expand=True)
    center_right_frame = tk.Frame(center_frame,  width=25,  height=5)
    center_right_frame.pack(side="right", fill='both',  expand=True)

    center2_left_frame = tk.Frame(center2_frame,  width=25,  height=5)
    center2_left_frame.pack(side="left", fill='both',  expand=True)
    center2_right_frame = tk.Frame(center2_frame,  width=25,  height=5)
    center2_right_frame.pack(side="right", fill='both',  expand=True)
    
    bottom_left_frame = tk.Frame(bottom_frame,  width=40,  height=2)
    bottom_left_frame.pack(side="left", fill='both',  expand=True)
    bottom_right_frame = tk.Frame(bottom_frame,  width=40,  height=2)
    bottom_right_frame.pack(side="right", fill='both',  expand=True)

    label_page_num = tk.Label(center_left_frame,
                            text = "Summarize pages:",
                            width = 20, height = 1,
                            fg = "blue")
    label_page_num.pack(side="left")

    # Text Field
    text_file = tk.Text(top_left_frame, width=50, height=2)
    
    text_first_page = tk.Text(center_left_frame, width=2, height=1)
    text_last_page = tk.Text(center_right_frame, width=2, height=1)

    # Button Components
    button_explore = tk.Button(top_right_frame,
                        text = "Browse Files",
                        command = browseFiles)
  
    button_summarize = tk.Button(center2_right_frame,
                     text = "Summarize",
                     command = exit)

    button_settings = tk.Button(center2_left_frame,
                     text = "Settings",
                     command = exit)

    button_speech = tk.Button(bottom_left_frame,
                     text = "Speech",
                     command = exit)

    button_save = tk.Button(bottom_right_frame,
                     text = "Save",
                     command = exit)

    # PDF Viewer Component
    view = pdf.ShowPdf()
    pdf_viewer = view.pdf_view(page_frame, pdf_location='', width=80, height=100)

    # Pack components
    text_file.pack()

    button_explore.pack()
    
    text_first_page.pack()

    text_last_page.pack()

    button_settings.pack()

    button_summarize.pack()

    button_speech.pack()

    button_save.pack()

    pdf_viewer.pack()

    detect_file_path()
    
    root.mainloop()

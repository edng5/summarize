# Summarize by Edward Ng
# Summarizes text and extracts the key information. Supports PDF, websites and audio file inputs.
# 1/22/2023

import tkinter as tk
from tkinter import filedialog
from utils import ShowPdf

from summary_controller import *
from summary_model import *

PDF_LOCATION = ""

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
    # can only pass a max length 512 in pegasus?
    # text = pegasus_summarize(text)
    summary.configure(text=text)
    # v1.pdf_view(page_frame,
    #              pdf_location = filename, 
    #              width = 75, height = 100)
    PDF_LOCATION = filename


#==============MAIN=================#

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

    v1 = ShowPdf()

    filename = r"E:\Downloads\1-s2.0-S2590005622000595-main.pdf"
    pdf_viewer = v1.pdf_view(page_frame,
                 pdf_location = PDF_LOCATION, 
                 width = 75, height = 100)

    #destroy and recreate to refresh the pdf viewer
    # if FLAG == 1:
    #     pdf_viewer.destroy()
    #     pdf_viewer = v1.pdf_view(page_frame,
    #              pdf_location = filename, 
    #              width = 75, height = 100)

    pdf_viewer.pack(side="left")
    
    # pdf_viewer.update_idletasks()
    # root.after(0, v1.pdf_view(page_frame, pdf_location = PDF_LOCATION, width = 75, height = 100))
    root.mainloop()

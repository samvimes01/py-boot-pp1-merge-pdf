import os
import shutil

import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

from datetime import datetime
from pypdf import PdfWriter


class DocSelector:
    def __init__(self, win):
        self.__win = win
        self.__docs = []
        self.__init_ui()

    def __init_ui(self):
        root = self.__win.get_root()
        bold_font = ("Helvetica", 18, "bold")
        # Files to merge list
        frame_head = tk.Frame(root)
        selected_label = tk.Label(frame_head, text="Files to merge", font=bold_font)
        selected_label.pack(side=tk.LEFT, anchor="w")
        # Create button to select docx file
        self.select_button = tk.Button(frame_head, text="Select PDF files", command=self.select_docx)
        self.select_button.pack(side=tk.RIGHT)
        frame_head.pack(padx=10, pady=10, fill=tk.X)

        # Create listbox to show available docx files
        self.listbox = tk.Listbox(root)
        self.listbox.pack(padx=10, fill=tk.BOTH, expand=True)

        # Selected file block
        frame = tk.Frame(root)
        # Button to move selected item up
        self.move_up_button = tk.Button(frame, text="Move Up", command=self.move_up)
        self.move_up_button.pack(side=tk.LEFT)
        # Button to move selected item down
        self.move_down_button = tk.Button(frame, text="Move Down", command=self.move_down)
        self.move_down_button.pack(side=tk.LEFT)
        # Button to remove selected file
        self.remove_button = tk.Button(
            frame, text="Remove selected file", command=self.delete_item
        )
        self.remove_button.pack(side=tk.RIGHT)
        frame.pack(pady=10)
        
        # Merged files block
        selected_label = tk.Label(root, text="Merged files", font=bold_font)
        selected_label.pack(padx=10, pady=10, anchor="w")
        self.merged_list = tk.Listbox(root)
        self.merged_list.pack(padx=10, fill=tk.BOTH, expand=True)

        # Create button to select docx file
        self.select_button = tk.Button(
            root, text="Merge files to a single PDF", command=self.merge_pdfs
        )
        self.select_button.pack(pady=10)

    def get_self_tmp_dir(self):
        # temp_dir = tempfile.gettempdir()
        temp_dir = os.path.join("tmp", "merged")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
        return os.path.join("tmp")

    def get_doc_dir(self):
        path = os.path.expanduser("~/Documents")
        if os.path.isdir(path):
            return path
        else:
            return os.path.expanduser("~")

    # Function to handle button click and select docx file
    def select_docx(self):
        doc_dir = self.get_doc_dir()
        # Open file dialog with specific options
        files = filedialog.askopenfilenames(
            initialdir=doc_dir,
            title="Select Docx File",
            filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*")),
        )
        if len(files) == 0:
            return

        for file in files:
            filename = os.path.basename(file)
            self.__docs.append(file)
            self.listbox.insert(tk.END, filename)


    # Function to update list of available docx files in temp directory
    def update_mergedlist(self):
        temp_dir = os.path.join(self.get_self_tmp_dir(), "merged")
        # Clear listbox
        self.merged_list.delete(0, tk.END)
        # Get list of docx files in temp directory
        for filename in os.listdir(temp_dir):
            if filename.endswith(".pdf"):
                self.merged_list.insert(tk.END, filename)

    def merge_pdfs(self):
        temp_dir = self.get_self_tmp_dir()
        merger = PdfWriter()

        for pdf in self.__docs:
            # shutil.copy(doc, os.path.join(temp_dir))
            merger.append(pdf)
        dtstr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        merger.write(os.path.join(temp_dir, "merged", f"merged-{dtstr}.pdf"))
        merger.close()
        messagebox.showinfo(title="Success", message=f"merged {len(self.__docs)} files successfully")
        self.update_mergedlist()

    # move items
    def move_up(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return  # No item selected

        index = selected_index[0]
        if index > 0:
            item = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index - 1, item)
            self.listbox.select_set(index - 1)

    def move_down(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            return  # No item selected

        index = selected_index[0]
        if index < len(self.__docs) - 1:
            item = self.listbox.get(index)
            self.listbox.delete(index)
            self.listbox.insert(index + 1, item)
            self.listbox.select_set(index + 1)

    # Function to delete an item from the listbox
    def delete_item(self):
        sel = self.listbox.curselection()
        if not sel or len(sel) == 0:
            messagebox.showwarning(title="Fail Deleting", message="Please, select a file")
            return
        print(self.listbox.get(sel[0]))
        self.listbox.delete(sel[0])
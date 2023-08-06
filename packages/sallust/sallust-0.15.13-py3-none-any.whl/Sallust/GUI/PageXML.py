import tkinter as tk
from tkinter.font import Font
from natsort import natsorted
from tkinter import filedialog
from sallust import Constants


class PageXML(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg=Constants.dark_color)
        self.search_indexes = []

        text_font = Font(family="Verdana",
                         size=12)

        self.save_button = tk.Button(self,
                                     text="Save",
                                     image=Constants.image_save,
                                     command=self.save_xml,
                                     bg=Constants.dark_color)

        self.save_button.pack(anchor="w")

        self.text = tk.Text(self,
                            cursor="arrow",
                            bd=0,
                            fg="white",
                            font=text_font,
                            highlightbackground=Constants.dark_color,
                            highlightcolor=Constants.dark_color,
                            highlightthickness=10,
                            bg=Constants.medium_color)

        self.text.pack(expand=1, fill="both")

        self.text.tag_configure("hover_line",
                                background=Constants.light_color)
        self.text.tag_configure("code_character",
                                foreground=Constants.code_character_color)
        self.text.tag_configure("string_character",
                                foreground=Constants.string_character_color)

        self.text.bind("<Motion>", self.hover_line)
        self.text.bind("<KeyRelease>", self.hover_line)
        self.text.bind("<Key>", self.search)
        self.text.bind("<KeyRelease>", self.search)
        self.text.bind("<Leave>", self.remove_hover)
        self.imported_xml = False
        self.filename = None

    def create_xml(self):
        if self.imported_xml is False:
            self.text.delete("1.0", "end")
            with open(self.controller.current_xml, "r") as f:
                string_xml = f.read()
                self.text.insert("end", string_xml)
        self.search()

    def set_xml(self, string_xml):
        self.imported_xml = True
        self.text.delete("1.0", "end")
        self.text.insert("end", string_xml)
        self.search()

    def save_xml(self):
        self.filename = filedialog.asksaveasfile("w",
                                                 filename=self.controller.current_xml,
                                                 filetypes=[("XML file", ".xml")],
                                                 defaultextension=".xml")
        if self.filename:
            file_to_save = self.text.get("1.0", "end")
            self.filename.write(file_to_save)
            self.filename.close()

    def remove_hover(self, event=None):
        self.text.tag_remove("hover_line", "1.0", "end")

    def hover_line(self, event=None):
        self.remove_hover()
        index = self.text.index("current")
        self.text.tag_add("hover_line", str(index)+" linestart", str(index) + " lineend + 1 char")

    def search(self, event=None):
        self.text.tag_remove("code_character", "1.0", "end")
        self.text.tag_remove("string_character", "1.0", "end")
        self.search_indexes = []
        search_index = "1.0"

        while search_index != "+ 1 char":
            try:
                # search the value starting at 'search index' and returns the index if there is a coincidence
                search_index = self.text.search("<", search_index, "end", nocase=1)
                search_index_end_one = self.text.search("=", search_index, "end", nocase=1)
                search_index_end_two = self.text.search(" ", search_index, "end", nocase=1)
                search_index_end_three = self.text.search(">", search_index, "end", nocase=1)
                end_index = [search_index_end_one, search_index_end_two, search_index_end_three]
                end_index = natsorted(end_index, key=lambda y: y.lower())
                end = end_index[0]
                if end_index[0] == "":
                    end = end_index[1]
                if end_index[1] == "":
                    end = end_index[2]
                self.text.tag_add("code_character", search_index, end + "+ 1 char ")
                search_index = end
                if search_index != "":
                    # if the index is not empty store it
                    self.search_indexes.append(search_index)

            except Exception:
                self.error_message()
            search_index = search_index + "+ 1 char"

        search_index = "1.0"
        while search_index != "+ 1 char":
            # search the value starting at 'search index' and returns the index if there is a coincidence
            search_index = self.text.search(">", search_index, "end", nocase=1)
            if search_index is not "":
                search_end = self.text.search("<", search_index, "end", nocase=1)
                self.text.tag_add("code_character", search_index)
                if search_end is not "":
                    self.text.tag_add("string_character", search_index+"+ 1 char", search_end)

            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"
        # tag the coincidences of the search as selected
        search_index = "1.0"

    def error_message(self):
        pass
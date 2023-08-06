from sallust import Constants


class ColorizePythonFunctions:

    def __init__(self, steps):
        # Assign the arguments
        self.steps = steps
        # Initialize variables
        self.tag = "function"
        self.error_line_tag = "failed_line"
        self.text = self.steps.text
        self.color_tags = []
        self.code_characters = [" if ", " else:", " finally ", " while ", " try:", " in ", " for ",
                                "raise ", "None" "True", "False", "while", "continue", "class ", "finally:", " is ",
                                "lambda:", "not", "elif", "import", "pass", "assert", "break", "from", " and ", "del",
                                "with ", "yield", "return", "==", "<=", ">=", "!=", " def ", ","]

        self.special_methods = ["__new__", "__init__", "__del__", "__repr__", "__str__", "__bytes__", "__format__",
                                "__lt__", "__le__", "__eq__", "__ne__", "__gt__", "__ge__", "__hash__", "__bool__",
                                "__getattr__", "__getattribute__", "__setattr__", "__delattr__", "__dir__",
                                "__class__ ", "__get__", "__set__", "__delete__", "__set_name__", "__slots__",
                                "__init_subclass__", "__instancecheck__", "__subclasscheck__", "__class_getitem__",
                                "__call__", "__len__", "__length_hint__", "__getitem__", "__getitem__", "__getitem__",
                                ]

    def update_color(self):

        """Update all the colors of the text widget"""
        for element in self.color_tags:
            self.text.tag_remove(element, "1.0", "end")

        # Colorize the strings
        self.colorize_from_to('"""', '"""', Constants.string_character_color, to_code_included=True)
        self.colorize_from_to('"', '"', Constants.string_character_color, to_code_included=True, search_gap="+ 2 char")
        self.colorize_from_to("'", "'", Constants.string_character_color, to_code_included=True, search_gap="+ 2 char")
        # Colorize the step method name
        self.colorize_from_to("def test", '(', "#e7c51e")
        # Colorize all the key python words
        for code in self.code_characters:
            self.colorize(code, Constants.code_character_color, nocase=0)
        for code in self.special_methods:
            self.colorize(code, Constants.purple, nocase=0)
        # colorize the word 'self'
        self.colorize("self", Constants.purple)
        # raise the tag of the word 'def' in order to be shown with the color of key words
        self.text.tag_raise("color_ def ", "color_def test")

    def colorize(self, code, color, nocase=1):

        """this function searches for all strings 'code' inside the given 'Text' widget and changes it's color
        to 'color' if they are tagged with 'function'

        :type code: (str) the string to be changed
        :type color: (str) the color to be assigned
        :type nocase: (int) if the search match has to ignore case sensitive (0 if search has to be case sensitive)
        """

        # create the tag for the code
        tag_name = "color_" + code

        # if it's not already created append the tag to all color tags
        if tag_name not in self.color_tags:
            self.color_tags.append(tag_name)

        # configure the tag letter color
        self.text.tag_configure(tag_name, foreground=color)

        # initialize the search index
        search_index = "1.0"

        # do a loop while search index has not reach the end
        while search_index != "+ 1 char":
            # search the value starting at 'search index' and returns the index if there is a coincidence
            search_index = self.text.search(code, search_index, "end", nocase=nocase)
            # get all tags that index have
            if search_index is not "":
                tag_names = self.text.tag_names(search_index)
                # assign the color tag if the coincidence have the 'function' tag
                if "function" in tag_names:
                    # calculate the code length
                    code_length = "+" + str(len(code)) + " char"
                    # assign the color tag to the code
                    self.text.tag_add(tag_name, search_index, search_index + code_length)


            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"
        # Raise the tag over the tag 'function' in order to be shown
        self.text.tag_raise(tag_name, self.tag)

    def colorize_from_to(self, from_code, to_code, color, to_code_included=False, search_gap= "+ 1 char"):
        """this function searches for all strings  that starts as 'from_code' and ends as 'to_code'
         inside the given 'Text' widget and changes it's color to 'color' if they are tagged with 'function'

        :type from_code: (str) the starting point of the string
        :type to_code: (str) the end point of the string
        :type color: (str) the color to be assigned
        :type to_code_included: (bool) if the end point should be colorized too
        """

        # Create the tag for the code
        tag_name = "color_" + from_code

        # if the tag it's not already created append the tag to all color tags
        if tag_name not in self.color_tags:
            self.color_tags.append(tag_name)
        # Configure the tag letter color
        self.text.tag_configure(tag_name, foreground=color)

        # Get the length of the 'from_code' string
        from_code_length = "+" + str(len(from_code)) + " char"

        # If to_code_included then calculate the length of 'to_code' in order to be colorized
        if to_code_included:
            to_code_length = "+" + str(len(to_code)) + " char"
        else:
            to_code_length = ""

        # Initialize the search_index
        search_index = "1.0"
        search_index_end = None

        # do a loop while search index has not reach the end
        while search_index != "+ 1 char":
            # search the 'from_code' string starting at 'search index', returns the index if there is a coincidence
            search_index = self.text.search(from_code, search_index, "end", nocase=1)
            if search_index is not "":
                # search the 'to_code' string starting at 'search index' and returns the index if there is a coincidence
                search_index_end = self.text.search(to_code, search_index + from_code_length, "end", nocase=1)

                # Get the tags that are assigned to the start index and end index
                tag_names = self.text.tag_names(search_index)
                tag_names_end = self.text.tag_names(search_index_end)

                # if 'function' tag is in both index then colorize all text from 'from_code' to 'to_code'
                if "function" in tag_names_end:
                    if "function" in tag_names:
                        self.text.tag_add(tag_name, search_index, search_index_end + to_code_length)

                # set the search_index to the current coincidence
                search_index = search_index_end

            # set the search_index to the current coincidence plus 1 character
            search_index = search_index + "+ 1 char"

        # Raise the tag over the tag 'function' in order to be shown
        self.text.tag_raise(tag_name, self.tag)


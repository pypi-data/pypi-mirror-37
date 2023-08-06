import tkinter as tk
import numpy as np
from sallust import Constants as Constants


class StepsTable(tk.Frame):

    """This class creates a table that represents the passed and failed steps"""

    def __init__(self, parent, controller, graphics,  **kw):
        """
            This class creates a table that represents the passed and failed steps

        :type parent: (tk.Frame)
        :type controller: (Window)
        :type graphics: (Graphics)

        """
        super().__init__(parent, **kw)

        # Assign arguments
        self.controller = controller
        self.steps_frame = parent
        self.graphics = graphics

        # set the row and column initial values
        self.index_row = 2
        self.index_column = 2

        # configure frame
        self.configure(bg=Constants.light_color)

        # Create table elements
        self.steps_table_column_steps = tk.Label(self,
                                                 text="Nº Steps",
                                                 font=Constants.text_font(),
                                                 fg=Constants.text_color,
                                                 bg=Constants.medium_color,
                                                 bd=10)

        self.steps_table_column_percentage = tk.Label(self,
                                                      text="% Steps",
                                                      font=Constants.text_font(),
                                                      fg=Constants.text_color,
                                                      bg=Constants.medium_color,
                                                      bd=10)

        self.steps_table_passed_header = tk.Label(self,
                                                  text="Passed",
                                                  font=Constants.text_font(),
                                                  fg=Constants.text_color,
                                                  bg=Constants.green_color,
                                                  bd=10)

        self.steps_table_failed_header = tk.Label(self,
                                                  text="Failed ",
                                                  font=Constants.text_font(),
                                                  fg=Constants.text_color,
                                                  bg=Constants.red_color,
                                                  bd=10)

        self.steps_table_passed_result = tk.Label(self,
                                                  text="0",
                                                  font=Constants.text_font(),
                                                  fg=Constants.text_color,
                                                  bg=Constants.ultra_light_color,
                                                  bd=10)

        self.steps_table_failed_result = tk.Label(self,
                                                  text="0",
                                                  font=Constants.text_font(),
                                                  fg=Constants.text_color,
                                                  bg=Constants.ultra_light_color,
                                                  bd=10)

        self.steps_table_passed_percentage_result = tk.Label(self,
                                                             text="0",
                                                             font=Constants.text_font(),
                                                             fg=Constants.text_color,
                                                             bg=Constants.ultra_light_color,
                                                             bd=10)

        self.steps_table_failed_percentage_result = tk.Label(self,
                                                             text="0",
                                                             font=Constants.text_font(),
                                                             fg=Constants.text_color,
                                                             bg=Constants.ultra_light_color,
                                                             bd=10)
        # Grid elements
        self.steps_table_column_steps.grid(row=self.index_row,
                                           column=self.index_column + 1,
                                           sticky="nwes",
                                           pady=1,
                                           padx=1)

        self.steps_table_column_percentage.grid(row=self.index_row,
                                                column=self.index_column + 2,
                                                sticky="nwes",
                                                pady=1,
                                                padx=1)

        self.steps_table_passed_header.grid(row=self.index_row + 1,
                                            column=self.index_column,
                                            sticky="nwes",
                                            pady=1,
                                            padx=1)

        self.steps_table_failed_header.grid(row=self.index_row + 2,
                                            column=self.index_column,
                                            sticky="nwes",
                                            pady=1,
                                            padx=1)

        self.steps_table_passed_result.grid(row=self.index_row + 1,
                                            column=self.index_column + 1,
                                            sticky="nwes",
                                            pady=1,
                                            padx=1)

        self.steps_table_failed_result.grid(row=self.index_row + 2,
                                            column=self.index_column + 1,
                                            sticky="nwes",
                                            pady=1,
                                            padx=1)

        self.steps_table_passed_percentage_result.grid(row=self.index_row + 1,
                                                       column=self.index_column + 2,
                                                       sticky="nwes",
                                                       pady=1,
                                                       padx=1)

        self.steps_table_failed_percentage_result.grid(row=self.index_row + 2,
                                                       column=self.index_column + 2,
                                                       sticky="nwes",
                                                       pady=1,
                                                       padx=1)

        self.configure_cells()

    def configure_cells(self):
        # Configure rows and columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(5, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(0, minsize=40)
        self.rowconfigure(5, minsize=40)

    def update_table(self):

        # set the variables to zero
        passed = 0
        failed = 0

        # get the passed steps
        for i in range(len(self.graphics.passed)):
            passed += self.graphics.passed[i]

        # get the failed steps
        for i in range(len(self.graphics.failed)):
            failed += self.graphics.failed[i]

        # get the total number of steps
        total = passed + failed

        # calculate the percentages
        passed_per = np.round((passed / total) * 100, 1)
        failed_per = np.round((failed / total) * 100, 1)

        # Update the table representation values
        self.steps_table_passed_result.configure(text=passed)
        self.steps_table_failed_result.configure(text=failed)
        self.steps_table_passed_percentage_result.configure(text=passed_per)
        self.steps_table_failed_percentage_result.configure(text=failed_per)

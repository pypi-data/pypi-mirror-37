from fpdf import FPDF


class ResultsPDF(FPDF):

    def set_data(self, data):
        self.data = data

    def header(self):
        title = "Results of Test Run"
        # Arial bold 15
        self.set_font('Arial', size=15)
        # Calculate width of title and position
        w = 170
        self.set_x((210 - w) / 2)
        # Colors of frame, background and text
        self.set_draw_color(48, 62, 88)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        # Thickness of frame (1 mm)
        self.set_line_width(0.7)
        # Title
        self.cell(w, 16, title, 1, 1, 'C', 1)
        self.image('sallust/GUI/img/Apyno_logo_big.png', 25, 12, 13, 13)
        # Line break
        self.ln(10)
        self.draw_border_lines()

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Text color in gray
        self.set_text_color(128)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def draw_border_lines(self):
        self.line(20, 25, 20, self.h - 30)
        self.line(190, 25, 190, self.h - 30)
        self.line(20, self.h - 30, 190, self.h-30)

    def draw_resume_data_row(self, tag, value):
        self.set_draw_color(0, 0, 0)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        spacing = 3
        col_width = self.w / 7
        row_height = self.font_size - 1
        self.cell(col_width, (row_height * spacing), str(tag), border=1, fill=1, align="C")
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        self.cell(col_width, (row_height * spacing), str(value), border=1, fill=1, align="C")
        self.ln(7)

    def draw_resume_data(self, data):
        self.set_draw_color(212, 212, 212)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        self.set_left_margin(30)

        self.ln(5)
        self.set_font("Arial", size=9)
        self.image("temp/pie.png", 98, 30, 90, 80)
        self.draw_resume_data_row("Total test case", data.get_number_of_test_case())
        self.draw_resume_data_row("Passed test case", data.get_passed_test_case())
        self.draw_resume_data_row("Failed test case", data.get_failed_test_case())
        self.draw_resume_data_row("Total steps", data.get_total_steps())
        self.draw_resume_data_row("Passed steps", data.get_total_passed_steps())
        self.draw_resume_data_row("Failed steps", data.get_total_failed_steps())
        self.ln(30)

    def data_table(self, data):
        self.set_font("Arial", size=13)
        self.set_left_margin(80)
        self.cell(0, 0, "TABLE OF TEST CASE")
        self.set_left_margin(30)
        self.ln(8)
        self.set_font("Arial", size=6)
        self.set_draw_color(212, 212, 212)
        self.set_fill_color(92, 116, 144)
        self.set_text_color(255, 255, 255)
        self.set_left_margin(30)
        spacing = 3
        col_width = self.w / 7
        row_height = self.font_size

        self.cell(col_width, (row_height * spacing),
                  txt="Test Case", border=1, fill=1, align='C')
        self.cell(col_width, (row_height * spacing),
                  txt="Passed Steps", border=1, fill=1, align='C')
        self.cell(col_width, (row_height * spacing),
                  txt="Failed Steps", border=1, fill=1, align='C')
        self.cell(col_width, (row_height * spacing),
                  txt="Total Steps", border=1, fill=1, align='C')
        self.cell(col_width, (row_height * spacing),
                  txt="% Steps", border=1, fill=1, align='C')
        self.ln(6)
        self.set_left_margin(30)
        for i in range(data.get_number_of_test_case()):
            test_d = data.get_test_case_by_order(i)
            data_list = [test_d.get_name(),
                         test_d.get_passed_steps(),
                         test_d.get_failed_steps(),
                         test_d.get_total_steps(),
                         str(test_d.get_passed_percentage(1)) + "%"]
            for element in data_list:
                if test_d.get_status() == "pass":
                    self.set_fill_color(34, 134, 58)
                else:
                    self.set_fill_color(146, 46, 46)
                self.cell(col_width, (row_height * spacing),
                          txt=str(element), border=1, fill=1, align='C')

            self.ln(6)
        self.ln(10)

    def check_end(self, distance=250):
        y = self.get_y()
        if y > distance:
            self.add_page()

    def case_by_case(self, data):
        self.set_text_color(0, 0, 0)
        self.set_draw_color(48, 62, 88)
        self.set_font("Arial", size=13)
        self.set_left_margin(87)
        self.check_end(190)
        self.cell(0, 0, "FAILED STEPS")
        self.set_left_margin(00)
        self.ln(10)
        self.set_font("Arial", size=11)
        for i in range(data.get_number_of_test_case()):

            self.set_left_margin(0)
            test_d = data.get_test_case_by_order(i)
            if test_d.get_status() == "pass":
                continue
            self.set_font("Arial", size=11)

            self.set_text_color(255, 255, 255)
            self.set_draw_color(212, 212, 212)
            if test_d.get_status() == "pass":
                self.set_fill_color(34, 134, 58)
            else:
                self.set_fill_color(146, 46, 46)

            self.check_end(200)
            self.set_left_margin(30)
            self.cell(150, self.font_size + 2, txt=test_d.get_name(), border=1, fill=1, align="C")
            self.set_left_margin(0)
            self.ln(11)
            self.set_font("Arial", size=8)
            for j in range(test_d.get_number_of_steps()):
                self.set_left_margin(0)
                self.set_font("Arial", size=8)

                step = test_d.get_step_by_order(j+1)
                if step.get_status() == "fail":
                    x = self.get_x()
                    y = self.get_y()
                    title_string = "(Step " + str(step.get_order()) + "). " + step.get_description()
                    self.line(x+50, y + 2,  150, y + 2)
                    self.check_end()
                    self.set_text_color(0, 0, 0)
                    self.cell(0, 0, txt=title_string, align="C")
                    self.ln(5)
                    self.set_font("Arial", size=6)
                    self.check_end()
                    self.cell(0, 3, txt="status: " + str(step.get_status()), align="C")
                    self.ln(3)
                    self.check_end()
                    self.cell(0, 3, txt="execution time: " + str(step.get_time()), align="C")
                    self.ln(3)
                    self.set_fill_color(170, 211, 231)
                    self.set_left_margin(50)
                    self.multi_cell(100, 3, txt=str(step.get_method()), border=1, fill=1)
                    self.set_left_margin(0)
                    self.ln(3)
                    self.set_fill_color(212, 109, 109)
                    self.set_left_margin(50)
                    self.check_end()
                    if step.get_error_message() is not None:
                        self.multi_cell(100, 3, txt=step.get_error_message(), border=1, fill=1)
                    self.set_left_margin(0)
                    self.ln(5)
                self.set_left_margin(0)
            self.ln(10)

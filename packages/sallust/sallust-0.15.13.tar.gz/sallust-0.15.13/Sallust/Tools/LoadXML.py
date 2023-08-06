from defusedxml.lxml import _etree as et
from sallust.Tools import TestData


class LoadXML:

    def __init__(self, controller, steps):
        self.controller = controller
        self.steps = steps

    def load_file(self, path):
        self.controller.data = TestData.TestRunData()
        try:
            tree = et.parse(path)
        except Exception:
            raise FileNotFoundError
        root = tree.getroot()
        self.controller.get_frame("PageXML").set_xml(et.tostring(root))
        for i in range(len(root)-1):
            test_case = root[i]
            self.steps.add_test_case(test_case.get("name"))
            test_case_data = self.controller.data.add_test_case(test_case.get("name"), i)
            for index, value in enumerate(test_case):
                elem = value
                status = elem[0]
                time = elem[1]
                description = elem[2]
                if status.text == "passed":
                    self.steps.step_pass(description.text, time.text)
                    test_case_data.add_step(index+1, status="pass", description=description.text, time=time.text)
                if status.text == "failed":
                    error_element = elem[3]
                    func = error_element[0]
                    func_error_line = error_element[1]
                    func_error_message = error_element[2]
                    self.steps.step_fail(description.text,
                                         error_message=str(func_error_message.text),
                                         lines=str(func.text),
                                         error_line=str(func_error_line.text),
                                         time=time.text)
                    test_case_data.add_step(order=index+1,
                                            status="fail",
                                            description=description.text,
                                            method=func.text,
                                            error_line=func_error_line,
                                            time=time.text,
                                            error_message=func_error_message.text
                                            )

            self.steps.test_finish()
        console = root[-1]
        self.steps.write_console(console.text)
        self.controller.loaded_xml = True

        self.steps.text.see("1.0")

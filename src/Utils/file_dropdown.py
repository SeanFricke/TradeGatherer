import panel as pn


class FileDropdown:
    def __init__(self, title, options):
        self.title = title
        self.dropdown = pn.widgets.Select(name="Select " + title, options=options)
        self.custom_input = pn.Row(title + " Input: ", pn.widgets.TextInput())
        self.view = pn.Column(self.dropdown, self.custom_input)

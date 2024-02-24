import panel as pn
import front_page

class Controller:
    def __init__(self):
        """

        """
        self.front_page = front_page.FrontPage()
        self.tabs = pn.Tabs(
            ("Main", self.front_page.show()),
            ("Salary Info", pn.Column("Blep")),
            ("Interest Info", pn.Column("Blep")),
            dynamic=True
        )

    def serve(self):
        pn.serve(pn.template.FastListTemplate(

            title="Trade Gatherer - A repository for all things trading!", accent="#00BFFF",
            main=self.tabs

        ).servable())

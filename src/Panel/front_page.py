import os
from pathlib import Path
import panel as pn
import controller
import src.Utils.file_dropdown as file_dropdown
import src.Utils.constants as uc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FrontPage:
    def __init__(self):
        data_dir = "../../data/"
        self.observer = Observer()
        self.test_file = file_dropdown.FileDropdown(title="Hewwo ^w^:", options=self.update_file_options(data_dir))
        self.start_watching_dir(data_dir, self.test_file)
        
        self.import_file = pn.widgets.Button(name="Click me", button_type="primary")
        self.view = pn.Column(self.test_file.view, self.import_file)

    def start_watching_dir(self, path, dropdown):
        self.observer.schedule(FileWatcher(dropdown, path), path, recursive=True)
        self.observer.start()

    def update_file_options(self, path):
        files = [f for f in Path(path).iterdir() if f.is_file()]
        print(files + uc.SELECT_SPEC_OPTS)
        return files + uc.SELECT_SPEC_OPTS

    def show(self):
        return self.view


class FileWatcher(FileSystemEventHandler):
    def __init__(self, dropdown, path):
        self.dropdown = dropdown
        self.path = path

    def on_any_event(self, event):
        files = [f for f in Path(self.path).iterdir() if f.is_file()]
        self.dropdown.dropdown.options = files + uc.SELECT_SPEC_OPTS

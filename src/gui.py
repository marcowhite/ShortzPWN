import os

import dearpygui.dearpygui as dpg

from media.audio import Audio
from media.video import Video
from combine import Combiner


class FilesWindow:
    def __init__(self, label: str, files: list[str]):
        self.label = label
        self.files = {file: False for file in files}

    def create_table(self):
        def change_selection(sender, app_data, user_data):
            if user_data in self.files:
                self.files[user_data] = not self.files[user_data]

        def set_all_files(value: bool):
            for key in self.files.keys():
                self.files[key] = value
            self.update_checkboxes(value)

        def update_checkboxes(value: bool):
            for item in dpg.get_item_children(table, 1):  # 1 stands for the second column
                checkbox = dpg.get_item_children(item, 1)[0]  # Get the checkbox in each row
                dpg.set_value(checkbox, value)

        self.update_checkboxes = update_checkboxes

        with dpg.group() as group:

            with dpg.group(horizontal=True):
                dpg.add_text(self.label)
                dpg.add_button(label="Select All", callback=lambda: set_all_files(True))
                dpg.add_button(label="Deselect All", callback=lambda: set_all_files(False))

            with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                           borders_outerH=True, borders_innerV=True, borders_outerV=True) as table:
                dpg.add_table_column(label="Check")
                dpg.add_table_column(label="Name")
                for key, value in self.files.items():
                    with dpg.table_row():
                        checkbox_id = dpg.add_checkbox(default_value=value, user_data=key, callback=change_selection)
                        dpg.add_text(os.path.basename(key))
        return group


class MainWindow:
    def __init__(self):
        self.videos = Video.get_paths()
        self.audios = Audio.get_paths()

    def create_files_window(self, label: str, files: list[str]) -> FilesWindow:
        window = FilesWindow(label, files)
        with dpg.child_window(label=label, width=320, height=250) as child:
            table = window.create_table()
            dpg.move_item(table, parent=child)
        return window

    def create_main_window(self):
        with dpg.window(label="Main", tag="fullscreen"):
            with dpg.group(horizontal=True):
                video_window = self.create_files_window("Video", self.videos)
                audio_window = self.create_files_window("Audio", self.audios)

                user_data = (audio_window.files, video_window.files)

            dpg.add_separator()

            step = dpg.add_input_float(label="Step", default_value=3)
            end_time = dpg.add_input_int(label="End time", default_value=30)
            height = dpg.add_input_int(label="Height", default_value=1080)
            width = dpg.add_input_int(label="Width", default_value=1920)

            progress = dpg.add_text("Waiting...")

            def change_progress(text: str):
                dpg.set_value(progress, text)

            def handle_render(sender, app_data, user_data):
                selected_audio = [key for key, value in user_data[0].items() if value]
                selected_video = [key for key, value in user_data[1].items() if value]

                combiner = Combiner(
                    end_time=dpg.get_value(end_time),
                    step=dpg.get_value(step),
                    height=dpg.get_value(height),
                    width=dpg.get_value(width)
                )

                for text in combiner.combine(selected_video, selected_audio):
                    change_progress(text)

            dpg.add_button(label="Render", user_data=user_data, callback=handle_render)


def init_gui():
    dpg.create_context()
    dpg.create_viewport(title='ShortzPWN', width=685, height=500)

    main_window = MainWindow()
    main_window.create_main_window()

    dpg.setup_dearpygui()
    dpg.set_primary_window("fullscreen", True)
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

import os

import dearpygui.dearpygui as dpg

from media.audio import Audio
from media.video import Video
from combine import Combiner


class FilesWindow:
    def __init__(self, label: str, files: list):
        self.label = label
        self.files = {file: False for file in files}

    def create_table(self):
        def change_selection(sender, app_data, user_data):
            if user_data in self.files:
                self.files[user_data] = not self.files[user_data]

        with dpg.group() as group:
            with dpg.group(horizontal=True):
                dpg.add_text(self.label)

            with dpg.table(header_row=True, resizable=True, policy=dpg.mvTable_SizingStretchProp,
                           borders_outerH=True, borders_innerV=True, borders_outerV=True) as table:
                dpg.add_table_column(label="Check", parent=table)
                dpg.add_table_column(label="Name", parent=table)
                for key, value in self.files.items():
                    with dpg.table_row(parent=table):
                        dpg.add_checkbox(default_value=value, user_data=key, callback=change_selection)
                        dpg.add_text(str(key).split("/")[-1])

        return group


# def debug_menu():
#     with dpg.menu_bar():
#         with dpg.menu(label="Tools"):
#             dpg.add_menu_item(label="Show About", callback=lambda: dpg.show_tool(dpg.mvTool_About))
#             dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
#             dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc))
#             dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))
#             dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style))
#             dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font))
#             dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))

def init_gui():
    dpg.create_context()
    dpg.create_viewport(title=f'ShortzPWN', width=685, height=500)

    with dpg.window(label="Render", tag="fullscreen") as main_window:
        videos = Video.get_paths()
        audios = Audio.get_paths()

        with dpg.group(horizontal=True):
            VideoWindow = FilesWindow(label="Video", files=videos)
            with dpg.child_window(width=320, height=250) as video_child:
                video_table = VideoWindow.create_table()
                dpg.move_item(video_table, parent=video_child)

            AudioWindow = FilesWindow(label="Audio", files=audios)
            with dpg.child_window(label = "Audio",width=320, height=250) as audio_child:
                audio_table = AudioWindow.create_table()
                dpg.move_item(audio_table, parent=audio_child)

            user_data = (AudioWindow.files, VideoWindow.files)

        step = dpg.add_input_float(label="Step", default_value=3)
        end_time = dpg.add_input_int(label="End time", default_value=30)
        height = dpg.add_input_int(label="Height", default_value=1080)
        width = dpg.add_input_int(label="Width", default_value=1920)

        progress = dpg.add_text("Waiting...")

        def change_progress(text):
            dpg.set_value(progress, text)

        def handle_render(sender, app_data, user_data):
            selected_audio = [key for key, value in user_data[0].items() if value]
            selected_video = [key for key, value in user_data[1].items() if value]

            step_value = dpg.get_value(step)
            end_time_value = dpg.get_value(end_time)
            height_value = dpg.get_value(height)
            width_value = dpg.get_value(width)

            combiner = Combiner(end_time=end_time_value, step=step_value, height=height_value, width=width_value)
            for progress in combiner.combine(selected_video, selected_audio):
                change_progress(progress)

        dpg.add_button(label="Render", user_data=user_data, callback=handle_render)

    dpg.setup_dearpygui()
    dpg.set_primary_window("fullscreen", True)
    dpg.show_viewport()

    dpg.start_dearpygui()

    dpg.destroy_context()

import os


class Video:
    videos = []
    folder_path = os.path.join(os.getcwd(), "assets/video/")
    types = ('.MP4', ".AVI", ".MOV")

    @classmethod
    def get_paths(cls):
        for file_name in os.listdir(cls.folder_path):
            file_name = file_name.upper()

            if file_name.endswith(cls.types):
                file_path = os.path.join(cls.folder_path, file_name)
                cls.videos.append(file_path)

        return cls.videos

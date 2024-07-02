import os


class Audio:
    audios = []
    folder_path = os.path.join(os.getcwd(), "assets/audio/")
    types = ('.WAV', ".MP3")

    @classmethod
    def get_paths(cls):
        for file_name in os.listdir(cls.folder_path):
            file_name = file_name.upper()

            if file_name.endswith(cls.types):
                file_path = os.path.join(cls.folder_path, file_name)
                cls.audios.append(file_path)

        return cls.audios

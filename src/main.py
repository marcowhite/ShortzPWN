from combine import Combiner
from media.video import Video
from media.audio import Audio
from gui import init_gui

if __name__ == "__main__":
    videos = Video.get_paths()
    audios = Audio.get_paths()

    init_gui()

    # combiner = Combiner(end_time=148, step = 3)
    # for audio in audios:
    #     print("Combining audio with videos:", str.split(audio,"/")[-1])
    #     combiner.combine(videos, audio)
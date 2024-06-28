from combine import Combiner
from video import Video
from audio import Audio

if __name__ == "__main__":
    videos = Video.get_paths()
    audios = Audio.get_paths()
    combiner = Combiner(end_time=148, step = 0.3)
    for audio in audios:
        print("Combining audio with videos:", str.split(audio,"/")[-1])
        combiner.combine(videos, audio)

import os
import random
from datetime import datetime

import numpy as np
from moviepy.editor import *


class Combiner:

    def __init__(self, end_time=30, step=2.5):
        self.end_time: int = end_time
        self.step: float = step
        self.amount: int = 1
        self.save_dir = os.path.join(os.getcwd(), 'assets/@done/' + str(datetime.now().strftime("%d.%m.%y %H.%M.%S")))
        self.height: int = 1080
        self.width: int = 1920

    def __str__(self):
        string = (
            f"{self.amount} clip(s) {self.width}x{self.height} with step of {self.step} and {self.end_time}s duration")
        return string

    def _make_subclips_from_videos(self, videos):
        def create_subclips(clip, step):
            subclip_times = np.arange(0, clip.duration, step)
            subclips = list(map(lambda t_start: clip.subclip(t_start, min(t_start + step, clip.duration)),
                                filter(lambda t_start: t_start + step <= clip.duration, subclip_times)))
            return subclips

        clips = []
        random.shuffle(videos)
        processed = 0

        for video in videos:
            processed += 1
            clip = VideoFileClip(filename=video, target_resolution=(self.height, self.width))
            print(processed, "/", len(videos), str.split(clip.filename, '/')[-1], str(clip.duration))
            clips.append(create_subclips(clip, self.step))

        max_subclips = max(len(subclips) for subclips in clips)
        normalized_array_clips = []

        for i in range(max_subclips):
            for subclips in clips:
                if i < len(subclips):
                    normalized_array_clips.append(subclips[i])

        return normalized_array_clips

    def combine(self, videos, audio):
        print(self)

        subclips_from_videos = self._make_subclips_from_videos(videos)
        merge_clips = concatenate_videoclips(subclips_from_videos).subclip(0, self.end_time)
        audio_clip = AudioFileClip(audio)
        final_clip = merge_clips.set_audio(audio_clip)

        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)

        audio_file_name = str.split(audio, "/")[-1]
        audio_name = str.split(audio_file_name, '.')[0]
        path = os.path.join(self.save_dir, audio_name + ".mp4")

        final_clip.write_videofile(path)

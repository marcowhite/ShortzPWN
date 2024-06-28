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
        string = ("End time: " + str(self.end_time)
                  + "\nStep: " + str(self.step)
                  + "\nAmount: " + str(self.amount)
                  + "\nSave dir: " + str(self.save_dir)
                  + "\nHeight: " + str(self.height)
                  + "\nWidth: " + str(self.width)
                  )
        return string

    def _make_clips_from_videos(self, videos):
        clips = []

        random.shuffle(videos)

        processed = 0
        for video in videos:
            subclips = []
            processed += 1
            clip = VideoFileClip(filename=video, target_resolution=(self.height,self.width))

            print(processed, "/", len(videos), str.split(clip.filename, '/')[-1], str(clip.duration))

            start_time = 0
            while start_time + self.step < clip.duration:
                subclip = clip.subclip(t_start=start_time, t_end=start_time + self.step)
                start_time = start_time + self.step
                subclips.append(subclip)

            clips.append(subclips)

        max_subclips = max(len(subclips) for subclips in clips)
        normalized_array_clips = []

        for i in range(max_subclips):
            for subclips in clips:
                if i < len(subclips):
                    normalized_array_clips.append(subclips[i])

        return normalized_array_clips

    def _make_clips_from_videos_new(self, videos):
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
            clip = VideoFileClip(filename=video, target_resolution=(self.height,self.width))

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
        print("Starting with combine\n",self)

        clips = self._make_clips_from_videos_new(videos)

        merge_clips = concatenate_videoclips(clips).subclip(0, self.end_time)

        audio_clip = AudioFileClip(audio).subclip(0, self.end_time)

        final_clip = merge_clips.set_audio(audio_clip)

        if not os.path.isdir(self.save_dir):
            os.mkdir(self.save_dir)

        audio_file_name = str.split(audio, "/")[-1]
        audio_name = str.split(audio_file_name, '.')[0]
        path = os.path.join(self.save_dir, audio_name + ".mp4")

        final_clip.write_videofile(path)

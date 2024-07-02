import os
import random
from datetime import datetime

import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, afx


class Combiner:

    def __init__(self, end_time=30, step=2.5, height=1080, width=1920):
        self.end_time = end_time
        self.step = step
        self.height = height
        self.amount = 1
        self.width = width
        self.save_dir = os.path.join(os.getcwd(), 'assets/@done/', datetime.now().strftime("%d.%m.%y %H.%M.%S"))

    def __str__(self):
        return f"{self.amount} clip(s) {self.width}x{self.height} with step of {self.step} and {self.end_time}s duration"

    def _create_subclips(self, clip):
        subclip_times = np.arange(0, clip.duration, self.step)
        return [
            clip.subclip(t_start, min(t_start + self.step, clip.duration))
            for t_start in subclip_times if t_start + self.step <= clip.duration
        ]

    def _make_subclips_from_videos(self, videos):
        random.shuffle(videos)
        clips = []

        for index, video in enumerate(videos):
            clip = VideoFileClip(video, target_resolution=(self.height, self.width))
            yield f"Processing video {index + 1}/{len(videos)}: {os.path.basename(clip.filename)} ({clip.duration}s)"
            clips.extend(self._create_subclips(clip))

        yield "Subclips created and normalized."
        return clips

    def _combine_with_audio(self, video_clips, audio_file):
        concatenated_clip = concatenate_videoclips(video_clips).subclip(0, self.end_time)

        # Load and adjust the audio to match the video duration
        audio_clip = AudioFileClip(audio_file)
        audio_duration = concatenated_clip.duration
        if audio_clip.duration < audio_duration:
            audio_clip = afx.audio_loop(audio_clip, duration=audio_duration)
        else:
            audio_clip = audio_clip.subclip(0, audio_duration)

        # Set the audio of the concatenated and looped video clip
        final_clip = concatenated_clip.set_audio(audio_clip)

        if not os.path.isdir(self.save_dir):
            os.makedirs(self.save_dir)

        audio_name = os.path.splitext(os.path.basename(audio_file))[0]
        output_path = os.path.join(self.save_dir, f"{audio_name}.mp4")

        yield f"Starting final video rendering with {audio_name}"
        final_clip.write_videofile(output_path)
        yield f"Video saved to {os.path.basename(output_path)}"

    def combine(self, videos, audios):
        video_clips = yield from self._make_subclips_from_videos(videos)
        for audio in audios:
            yield from self._combine_with_audio(video_clips, audio)
        yield f"{len(audios)} videos rendered!"
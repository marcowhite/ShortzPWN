# Video and Audio Combiner

This project combines video clips with audio files, resizing the video to a specified resolution and adjusting the audio to match the video's duration. It also provides a GUI interface for user interaction.

## Features

- **Subclip Creation**: Create subclips from video files based on a specified step duration.
- **Video Concatenation**: Concatenate multiple video subclips into a single video.
- **Audio Adjustment**: Adjust the audio to match the duration of the concatenated video, either by looping or trimming.
- **Video Resizing**: Resize videos to a specified resolution.
- **Output**: Save the final combined video to a specified directory.
- **GUI Interface**: Interact with the application through a graphical user interface.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/video-audio-combiner.git
    cd video-audio-combiner
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Prepare your video and audio files in the `assets/video` and `assets/audio` directories respectively.
2. Run the application to open the GUI:
    ```sh
    python main.py
    ```

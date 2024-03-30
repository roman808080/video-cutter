#!/usr/bin/env python3
import os
import logging
import argparse
from contextlib import contextmanager

from pydub import AudioSegment

from split_audio import split_audio


MP3_EXTENSION = 'mp3'


@contextmanager
def ensure_file_removal(file_path):
    try:
        yield  # Perform file operations in the with block
    finally:
        # Cleanup action: Attempt to remove the file
        try:
            os.remove(file_path)
            logging.info(f"File successfully removed: {file_path}")

        except FileNotFoundError:
            logging.warning(f"File was already removed or does not exist: {file_path}")
        except Exception as e:
            logging.error(f"An error occurred while trying to remove the file: {e}")


def remove_file_extension(filename):
    """
    Removes the extension from a given filename.
    
    Parameters:
    - filename (str): The filename from which to remove the extension.
    
    Returns:
    - str: The filename without its extension.
    """
    # Split the filename into root and extension
    root, _ = os.path.splitext(filename)
    
    return root


def split_video(path_to_video, path_to_subtitles):
    mp3_file = f'{remove_file_extension(path_to_video)}.{MP3_EXTENSION}'

    with ensure_file_removal(file_path=mp3_file):
        audio = AudioSegment.from_file(path_to_video)
        audio.export(mp3_file, format=MP3_EXTENSION)

        split_audio(path_to_mp3=mp3_file, path_to_subtitles=path_to_subtitles)


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Split a video into chunks')

    parser.add_argument('-v', '--video', help='Path to the video file.', required=True)
    parser.add_argument('-s', '--subtitles', help='Path to the subtitles file.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    split_video(path_to_video=args.video, path_to_subtitles=args.subtitles)


if __name__ == "__main__":
    main()

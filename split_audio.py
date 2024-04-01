#!/usr/bin/env python3

import os
import json
import logging
import argparse

from moviepy.editor import AudioFileClip


def split_audio(path_to_mp3, path_to_subtitles, output_dir):
    # Load subtitles
    with open(path_to_subtitles, 'r') as file:
        subtitles = json.load(file)

    # Load the audio file
    audio_clip = AudioFileClip(path_to_mp3)

    # Process each subtitle entry
    for index, subtitle in enumerate(subtitles):
        # Calculate the end time of the clip
        start_time = subtitle['start']
        end_time = start_time + subtitle['duration']
        
        # Extract the specific audio segment
        audio_segment = audio_clip.subclip(start_time, end_time)
        
        # Define the output filename for the segment
        segment_filename = os.path.join(output_dir, f'segment_{index+1:03d}.mp3')

        # Write the audio segment to a file
        audio_segment.write_audiofile(segment_filename, logger=None)  # logger=None to suppress the progress bar

        yield index, subtitle, segment_filename

    # Close the original audio clip to release resources
    # TODO: Add with statement for audio_clip.
    audio_clip.close()


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    parser = argparse.ArgumentParser(description='Split audio into chunks')

    # the video should be first converted to audio by using:
    # ffmpeg -i input_video.mp4 -q:a 0 -map a output_audio.mp3

    parser.add_argument('-a', '--audio',
                        help='Path to the audio file.',
                        required=True)
    parser.add_argument('-s', '--subtitles',
                        help='Path to the subtitles file.',
                        required=True)
    parser.add_argument('-p', '--path',
                        help='The output path.',
                        required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Make sure that the folder exists
    os.makedirs(args.path, exist_ok=True)

    split_audio(path_to_mp3=args.audio, path_to_subtitles=args.subtitles, output_dir=args.path)

    for index, subtitle, segment_filename in split_audio(path_to_mp3=args.audio,
                                                         path_to_subtitles=args.subtiles,
                                                         output_dir=args.path):
        pass


if __name__ == "__main__":
    main()

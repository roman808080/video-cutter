#!/usr/bin/env python3

import json
import argparse


from moviepy.editor import AudioFileClip


def split_audio(path_to_mp3, path_to_subtitles):
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
        segment_filename = f'segment_{index+1:03d}.mp3'
        
        # Write the audio segment to a file
        audio_segment.write_audiofile(segment_filename, logger=None)  # logger=None to suppress the progress bar

        print(f"Segment {segment_filename} has been created.")

    # Close the original audio clip to release resources
    audio_clip.close()


def main():
    parser = argparse.ArgumentParser(description='Split audio into chunks')

    # the video should be first converted to audio by using:
    # ffmpeg -i input_video.mp4 -q:a 0 -map a output_audio.mp3

    parser.add_argument('-a', '--audio', help='Path to the audio file.', required=True)
    parser.add_argument('-s', '--subtitles', help='Path to the subtitles file.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    split_audio(path_to_mp3=args.mp3, path_to_subtitles=args.subtitles)

if __name__ == "__main__":
    main()

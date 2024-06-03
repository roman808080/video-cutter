#!/usr/bin/env python3

import os
import json
import logging
import argparse
import pysrt
from googletrans import Translator

from moviepy.editor import AudioFileClip


def srt_to_json(srt_file_path):
    # Replace the .srt extension with .json
    json_file_path = os.path.splitext(srt_file_path)[0] + '.json'
    
    subs = pysrt.open(srt_file_path)
    subs_data = []

    for sub in subs:
        # Convert start and end times to seconds
        start_seconds = sub.start.hours * 3600 + sub.start.minutes * 60 + sub.start.seconds + sub.start.milliseconds / 1000
        end_seconds = sub.end.hours * 3600 + sub.end.minutes * 60 + sub.end.seconds + sub.end.milliseconds / 1000

        # Calculate duration
        duration = end_seconds - start_seconds
        
        sub_data = {
            "start": round(start_seconds, 2),
            "duration": round(duration, 2),
            "text": sub.text
        }
        subs_data.append(sub_data)

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(subs_data, json_file, ensure_ascii=False, indent=4)

    logging.info(f"Converted {srt_file_path} to {json_file_path}")

    return json_file_path


# TODO: Move the next function into more logical place
def translate_subtitles(json_file_path, source_lang='auto', dest_lang='en'):
    # Create the path for the translated file
    base, ext = os.path.splitext(json_file_path)
    translated_file_path = f"{base}_en{ext}"
    
    # Initialize the translator
    translator = Translator()
    
    # Read the original subtitles from the JSON file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        subs_data = json.load(json_file)
    
    # Translate each subtitle
    for sub in subs_data:
        translated_text = translator.translate(sub["text"], src=source_lang, dest=dest_lang).text
        sub["text"] = translated_text
    
    # Save the translated subtitles to a new JSON file
    with open(translated_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(subs_data, json_file, ensure_ascii=False, indent=4)
    
    logging.info(f"Translated subtitles saved to: {translated_file_path}")
    return translated_file_path


def split_audio(path_to_mp3, path_to_subtitles, output_dir, buffer_time=0.33):
    # Make sure that output_dir exists
    os.makedirs(output_dir, exist_ok=True)

    # Load subtitles
    with open(path_to_subtitles, 'r') as file:
        subtitles = json.load(file)

    # Load the audio file
    audio_clip = AudioFileClip(path_to_mp3)
    duration = audio_clip.duration

    # Process each subtitle entry
    for index, subtitle in enumerate(subtitles):
        # Calculate the end time of the clip
        start_time = subtitle['start']
        end_time = start_time + subtitle['duration'] + buffer_time
        # Make sure that we use proper timing
        if end_time > duration:
            end_time = duration

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


# NOTE: The script was temporary remade to work with srt files
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
    parser.add_argument('-l', '--lang',
                        help='The original lang of the subs.',
                        required=True)

    # Parse the arguments
    args = parser.parse_args()

    # Make sure that the folder exists
    os.makedirs(args.path, exist_ok=True)

    json_subtitles = srt_to_json(srt_file_path=args.subtitles)
    translate_subtitles(json_file_path=json_subtitles, source_lang='cs')

    for index, subtitle, segment_filename in split_audio(path_to_mp3=args.audio,
                                                         path_to_subtitles=json_subtitles,
                                                         output_dir=args.path):
        pass


if __name__ == "__main__":
    main()

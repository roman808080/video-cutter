#!/usr/bin/env python3

import os
import sys
import shutil
import logging
import argparse

from urllib.parse import urlparse, parse_qs

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


DEFAULT_SOURCE_LANGUAGE = 'en'


def get_youtube_video_id(url):
    """
    Extracts the YouTube video ID from a given URL.

    Parameters:
    - url: str. The full URL of the YouTube video.

    Returns:
    - str. The YouTube video ID.
    """
    # Parse the URL
    parsed_url = urlparse(url)
    
    # Extract query parameters as a dictionary
    query_params = parse_qs(parsed_url.query)
    
    # Return the value associated with the 'v' parameter
    return query_params['v'][0] if 'v' in query_params else None


def remove_mp4_suffix(file_name):
    if file_name.endswith('.mp4'):
        return file_name[:-4]
    return file_name


def get_stream(url):
    yt = YouTube(url)
    return yt.streams.get_highest_resolution()


def get_video_name(url):
    return get_stream(url).default_filename


def download_youtube_video(video_url, path):
    """
    Downloads a video and all its subtitles from YouTube.
    
    Parameters:
    - video_url: str. The URL of the YouTube video.
    - path: str. The directory path to save the video and subtitles.
    """

    # Download video
    stream = get_stream(url=video_url)

    logging.info(f"Downloading video: {stream.title}")
    stream.download(output_path=path)
    logging.info(f"Video downloaded successfully: {stream.default_filename}")

    # TODO: Make sure that we return mp4 file name, right now,
    # it is only the name without the extentsion.
    return os.path.join(path, f'{stream.default_filename}.mp4')


def download_subtitles(video_url, path):
    video_id = get_youtube_video_id(url=video_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    video_name = get_video_name(url=video_url)

    downloaded_subtitles = {}
    for transcript in transcript_list:
        youtube_video_name = remove_mp4_suffix(file_name=video_name)

        language_code = transcript.language_code
        file_name = f'{youtube_video_name} ({language_code}).json'

        if transcript.is_generated:
            language_code = f'{transcript.language_code}_gen'
            file_name = f'{youtube_video_name} ({language_code}).json'

        file_path = os.path.join(path, file_name)

        formatter = JSONFormatter()
        text = transcript.fetch()
        json_formatted = formatter.format_transcript(text)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_formatted)

        logging.info(f'Downloaded {file_path}, amount of lines: {len(text)}')

        # Return downloaded subtitles
        downloaded_subtitles[language_code] = file_path

    return downloaded_subtitles


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Download videos and subtiles from YouTube.')

    download_options = ['all', 'video', 'subtitles'] # TODO: Add a dictionary

    # Add the -l/--link argument
    parser.add_argument('-l', '--link', help='The link to the video', required=True)

    parser.add_argument('--source-language', help='The name of the source language', default=DEFAULT_SOURCE_LANGUAGE)
    parser.add_argument('--target-language', help='The name of the target language', default=DEFAULT_SOURCE_LANGUAGE)

    parser.add_argument('-d', '--download', choices=download_options,
                        default=download_options[0],
                        help='Downloading all, video, subtitles')

    parser.add_argument('-p', '--path', help='The path to the output folder')

    # Parse the arguments
    args = parser.parse_args()

    output_dir = 'youtube_output_dir'
    if args.path is not None:
        output_dir = args.path

    # Make sure that the folder exists
    os.makedirs(output_dir, exist_ok=True)

    if args.download == download_options[0]:
        download_youtube_video(video_url=args.link, path=output_dir)
        download_subtitles(video_url=args.link, path=output_dir)

    elif args.download == download_options[1]:
        download_youtube_video(video_url=args.link, path=output_dir)

    elif args.download == download_options[2]:
        download_subtitles(video_url=args.link, path=output_dir)


if __name__ == "__main__":
    main()

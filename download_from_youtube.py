#!/usr/bin/env python3

import os
import sys
import shutil
import argparse

from urllib.parse import urlparse, parse_qs

from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


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
    print(f"Downloading video: {stream.title}")
    stream.download(output_path=path)
    print(f"Video downloaded successfully: {stream.default_filename}")


def download_subtitles(video_url, path):
    video_id = get_youtube_video_id(url=video_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    video_name = get_video_name(url=video_url)

    for transcript in transcript_list:
        youtube_video_name = remove_mp4_suffix(file_name=video_name)
        file_name = f'{youtube_video_name} ({transcript.language_code}).json'
        if transcript.is_generated:
            file_name = f'{youtube_video_name} ({transcript.language_code}, gen).json'

        file_path = os.path.join(path, file_name)

        formatter = JSONFormatter()
        text = transcript.fetch()
        json_formatted = formatter.format_transcript(text)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_formatted)

        print(f'Downloaded {file_path}, amount of lines: {len(text)}')


def main():
    parser = argparse.ArgumentParser(description='Download videos and subtiles from YouTube.')

    # Add the -l/--link argument
    parser.add_argument('-l', '--link', help='The link to the video', required=True)

    # Parse the arguments
    args = parser.parse_args()

    output_dir = 'youtube_output_dir'
    os.makedirs(output_dir, exist_ok=True)

    download_youtube_video(video_url=args.link, path=output_dir)
    download_subtitles(video_url=args.link, path=output_dir)


if __name__ == "__main__":
    main()

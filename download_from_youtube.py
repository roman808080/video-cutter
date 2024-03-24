import os
import sys
import shutil
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


def download_youtube_video_and_subtitles(video_url, path):
    """
    Downloads a video and all its subtitles from YouTube.
    
    Parameters:
    - video_url: str. The URL of the YouTube video.
    - path: str. The directory path to save the video and subtitles.
    """
    yt = YouTube(video_url)
    
    # Download video
    print(f"Downloading video: {yt.title}")
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=path)
    print(f"Video downloaded successfully: {stream.default_filename}")

    video_id = get_youtube_video_id(url=video_url)
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

    for transcript in transcript_list:
        youtube_video_name = remove_mp4_suffix(file_name=stream.default_filename)
        file_name = f'{youtube_video_name} ({transcript.language_code}).json'
        file_path = os.path.join(path, file_name)

        formatter = JSONFormatter()
        text = transcript.fetch()
        json_formatted = formatter.format_transcript(text)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json_formatted)
        
        print(f'Downloaded {file_path}, amount of lines: {len(text)}')


def main():
    video_url = sys.argv[1]

    output_dir = 'youtube_output_dir'
    os.makedirs(output_dir, exist_ok=True)

    download_youtube_video_and_subtitles(video_url=video_url, path=output_dir)


if __name__ == "__main__":
    main()

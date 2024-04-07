#!/usr/bin/env python3

import os
import json
import shutil
import tempfile
import logging
import argparse
from contextlib import contextmanager

from create_course import (COURSE_INFO, LESSON_INFO,
                           SOURCE_AUDIO_DIR, dump_file,
                           create_lesson)

from download_from_youtube import (download_youtube_video,
                                   get_video_name,
                                   download_subtitles)

from split_video import split_video


@contextmanager
def temp_directory():
    temp_dir = tempfile.mkdtemp()  # Create a temporary directory
    try:
        yield temp_dir  # Provide the temporary directory to the caller
    finally:
        shutil.rmtree(temp_dir)  # Clean up the temporary directory when done


def import_lesson(course_path, video_link,
                  source_abbreviation, target_abbreviation):

    # Getting course_info
    course_info_path = os.path.join(course_path, COURSE_INFO)
    course_info = None

    with open(course_info_path, 'r') as file:
        course_info = json.load(file)

    lesson_number = len(course_info['lessons']) + 1

    with temp_directory() as temp_processing_folder:
        video_name = get_video_name(url=video_link)
        video_path = download_youtube_video(video_url=video_link,
                                            path=temp_processing_folder)
        downloaded_subtitles = download_subtitles(video_url=video_link,
                                                path=temp_processing_folder)

        # Splitting audio
        audio_chunks_path = os.path.join(course_path, f'{lesson_number}', SOURCE_AUDIO_DIR)
        path_to_subtitles = downloaded_subtitles[target_abbreviation]

        # TODO: Adding a comparison between the source and target subtitles.
        # TODO: Get name of the lesson without .mp4 suffix.

        create_lesson(lesson_name=video_name, lesson_number=lesson_number,
                      lesson_path=os.path.join(course_path, f'{lesson_number}'),
                      link=video_link)

        for index, subtitle, segment_filename in split_video(path_to_video=video_path,
                                                            path_to_subtitles=path_to_subtitles,
                                                            output_dir=audio_chunks_path):

            logging.info(f'The next chunk was processed: index = {index}, '
                        f'subtitle={subtitle}, segment={segment_filename}.')

        # {
            # 'name': '<name>',
            # 'source-link': '<link>',
            # 'path': '<path-to-the-lesson>'
        # },

        lesson = {
            'name': video_name,
            'source-link': video_link,
            'path': f'{lesson_number}'
        }

        course_info['lessons'].append(lesson)

        # Dump the course info back
        dump_file(folder_path=course_path,
                file_name=COURSE_INFO,
                data=course_info)


def main():
    # A course should be create before using this script

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Import a lesson to a course')

    parser.add_argument('-c', '--course-path', help='The path to the course.', required=True)
    parser.add_argument('-v', '--video-link', help='The link to the video.', required=True)

    # TODO: We do not need to know the exact abbreviation of the target and source languages.
    parser.add_argument('-s', '--source-language', help='Abbreviation of the source language', required=True)
    parser.add_argument('-t', '--target-language', help='Abbreviation of the target language', required=True)

    # Parse the arguments
    args = parser.parse_args()

    logging.info(f'{args.course_path} {args.video_link}')

    import_lesson(course_path=args.course_path, video_link=args.video_link,
                  source_abbreviation=args.source_language,
                  target_abbreviation=args.target_language)


if __name__ == "__main__":
    main()

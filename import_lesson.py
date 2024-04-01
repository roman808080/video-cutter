#!/usr/bin/env python3

import os
import json
import logging
import argparse

from create_course import COURSE_INFO, LESSON_INFO


def import_lesson(course_path, video_link,
                  source_abbreviation, destination_abbreviation):

    # Getting course_info
    course_info_path = os.path.join(path, file_name)
    course_info = None

    with open(course_info_path, 'r') as file:
        course_info = json.load(file)

    lesson_number = len(course_info['lessons'])


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


if __name__ == "__main__":
    main()
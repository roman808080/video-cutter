#!/usr/bin/env python3
import os
import json
import argparse

from anki_utlis import generate_id


COURSE_INFO = 'course-info.json'
LESSON_INFO = 'lesson-info.json'
SOURCE_AUDIO_DIR = 'source-audio'

DEFAULT_INDENT = 4


# TODO: Rename to have a better name.
# It should resemble that it reads from json.

# TODO: Move dump_file and read_json_from_file to utils.py

def dump_file(folder_path, file_name, data, indent=DEFAULT_INDENT):
    os.makedirs(folder_path, exist_ok=True)
    info_file_path = os.path.join(folder_path, file_name)

    with open(info_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=indent)


def read_json_from_file(file_path):
    """
    Read JSON data from a file.

    Parameters:
    - file_path (str): Path to the JSON file.

    Returns:
    - dict: Parsed JSON data.
    """
    with open(file_path, 'r') as file:
        json_data = json.load(file)
    return json_data


# A structure of a course:
#
# course_dir/
#   course-info.json
#
#   lessons/
#     lesson_<i>/
#       lesson-info.json
#
#       source-audio/
#         audio-info.json
#         segment_001.mp3
#         ...
#         segment_999.mp3


def create_course(course_name, course_path,
                  source_language,
                  target_language,
                  link=None,
                  description=''):

    model_id = generate_id()
    deck_id = generate_id()

    course_structure = {
        'name': course_name,
        'description': description,

        'source_language': source_language,
        'target_language': target_language,

        'lessons': [
            # {
                # 'name': '<name>',
                # 'source-link': '<link>',
                # 'path': '<path-to-the-lesson>'
            # },
        ],

        'anki': {
            'model_id': model_id,
            'deck_id': deck_id,
        },

        'link': link,
    }

    dump_file(folder_path=course_path, file_name=COURSE_INFO,
              data=course_structure)


def create_lesson(lesson_name, lesson_number, lesson_path, link=None,
                  description=''):

    lesson_structure = {
        'name': lesson_name,
        'number': lesson_number,
        'description': description,

        'phrases': [
            # {
                # 'source': '<phrase-in-source-language>',
                # 'target': '<phrase-in-target-language>',

                # 'source_audio': 'path-to-source-audio'
                # 'target_audio': 'path-to-target-audio'

                # 'comment': '<some-comment-regarding-the-prase>'
            # },
        ],

        'link': link,
    }

    dump_file(folder_path=lesson_path, file_name=LESSON_INFO,
              data=lesson_structure)


def read_lesson(lesson_path):
    return read_json_from_file(file_path=lesson_path)


def main():
    parser = argparse.ArgumentParser(description='This script creates an empty course.')

    parser.add_argument('-c', '--course', help='The course name.', required=True)
    parser.add_argument('-p', '--path', help='The path to the course.', required=True)

    parser.add_argument('-s', '--source-language', help='The name of the source language.', required=True)
    parser.add_argument('-t', '--target-language', help='The name of the target language.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    create_course(course_name=args.course, course_path=args.path,
                  source_language=args.source_language,
                  target_language=args.target_language)


if __name__ == "__main__":
    main()

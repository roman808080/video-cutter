#!/usr/bin/env python3
import os
import json
import argparse

from anki_utlis import generate_id


COURSE_INFO = 'course-info.json'
DEFAULT_INDENT = 4


# course_dir/
#   course-info.json
#
#   lessons/
#     lesson_<i>/
#       lesson-info.json
#
#       anki/
#         lesson_<i>.apkg
#       source-audio/
#         audio-info.json
#         segment_001.mp3
#         ...
#         segment_999.mp3
#
#       processed-audio/
#         phrase_001.mp3
#         ...
#         phrase_999.mp3


def create_course(course_name, course_path=None):
    model_id = generate_id()
    deck_id = generate_id()

    course_structure = {
        'name': course_name,
        'lessons': [
            # {
                # 'name': '<name>',
                # 'source-link': '<link>',
                # 'anki_deck_path': '<path>',
                # 'audio_config_path': '<path>',
            # },
        ],
        'anki': {
            'model_id': model_id,
            'deck_id': deck_id,
        },
    }

    os.makedirs(course_path, exist_ok=True)
    info_file_path = os.path.join(course_path, COURSE_INFO)

    with open(info_file_path, 'w') as json_file:
        json.dump(course_structure, json_file, indent=DEFAULT_INDENT)

def main():
    parser = argparse.ArgumentParser(description='This script creates an empty course.')

    parser.add_argument('-c', '--course', help='The course name.', required=True)
    parser.add_argument('-p', '--path', help='The path to the course.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    create_course(course_name=args.course, course_path=args.path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import json
import argparse

from anki_utlis import generate_id


COURSE_INFO = 'course-info.json'
LESSON_INFO = 'lesson-info.json'

DEFAULT_INDENT = 4


def dump_file(folder_path, file_name, data, indent=DEFAULT_INDENT):
    os.makedirs(folder_path, exist_ok=True)
    info_file_path = os.path.join(folder_path, file_name)

    with open(info_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=indent)


# A structure of a course:
#
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


def create_course(course_name, course_path, link=None,
                  description=''):

    model_id = generate_id()
    deck_id = generate_id()

    course_structure = {
        'name': course_name,
        'description': description,

        'lessons': [
            # {
                # 'name': '<name>',
                # 'source-link': '<link>',
                # 'anki_deck_path': '<path>',
                # 'audio_config_path': '<path>',
                # 'path': '<path-to-the-lesson>'
            # },
        ],

        'anki': {
            'model_id': model_id,
            'deck_id': deck_id,
        },

        'link': link,
        'sub_courses': [],
    }

    dump_file(folder_path=course_path, file_name=COURSE_INFO,
              data=course_structure)


def create_lesson(lesson_name, lesson_number, source_language,
                  target_language, lesson_path, link=None,
                  description=''):

    lesson_structure = {
        'name': lesson_name,
        'number': number,
        'description': description,

        'source_language': source_language,
        'target_language': target_language,

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
        'sub_lessons': [],
    }

    dump_file(folder_path=lesson_path, file_name=LESSON_INFO,
              data=lesson_structure)


def main():
    parser = argparse.ArgumentParser(description='This script creates an empty course.')

    parser.add_argument('-c', '--course', help='The course name.', required=True)
    parser.add_argument('-p', '--path', help='The path to the course.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    create_course(course_name=args.course, course_path=args.path)


if __name__ == "__main__":
    main()

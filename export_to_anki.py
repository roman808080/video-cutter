#!/usr/bin/env python3

import json
import os
import argparse
import genanki

from create_course import COURSE_INFO


parser = argparse.ArgumentParser(description='Export to Anki.')

parser.add_argument('-c', '--course-path', help='The course path.', required=True)
# Parse the arguments
args = parser.parse_args()


# Path to your course-info.json file
course_info_path = os.path.join(args.course_path, COURSE_INFO)

# Load course info
with open(course_info_path, 'r') as file:
    course_info = json.load(file)

MODEL_ID = course_info['anki']['model_id']
DECK_ID = course_info['anki']['deck_id']
TARGET_LANGUAGE = course_info['target_language']

# Define the Anki model using information from course-info.json
my_model = genanki.Model(
    MODEL_ID,
    'Simple Model with Audio',
    fields=[
        {'name': 'English'},
        {'name': TARGET_LANGUAGE},
        {'name': 'Audio'},
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{English}}<br>{{Audio}}',  # Question format
            'afmt': '{{FrontSide}}<hr id="answer">{{' + TARGET_LANGUAGE + '}}',  # Answer format
        },
    ]
)

# Create a new Anki deck
my_deck = genanki.Deck(
    DECK_ID,
    course_info['name']
)

output_path = 'output_deck.apkg'

# Collect audio files to be added to the Anki package
audio_files = []

for lesson in course_info['lessons']:
    lesson_path = os.path.join(os.path.dirname(course_info_path), lesson['path'], 'lesson-info.json')
    
    # Load lesson info
    with open(lesson_path, 'r') as file:
        lesson_info = json.load(file)
    
    # Add cards for each phrase in the lesson
    for phrase in lesson_info['phrases']:
        if phrase['source_audio']:
            audio_path = os.path.join(os.path.dirname(lesson_path), 'source-audio', os.path.basename(phrase['source_audio']))
            print(audio_path)

            # Ensure the audio file exists before adding it to the list
            if os.path.exists(audio_path) and audio_path not in audio_files:
                audio_files.append(audio_path)
        
        note = genanki.Note(
            model=my_model,
            fields=[
                # TODO: source and target subtitles should be swapped.
                phrase['target'],  # English field
                phrase['source'],  # Target language field
                '[sound:{}]'.format(os.path.basename(phrase['source_audio'])) if phrase['source_audio'] else '',  # Audio field
            ]
        )
        my_deck.add_note(note)

# Package the deck and include the audio files
genanki.Package(my_deck, media_files=audio_files).write_to_file(output_path)

print(f"Deck created: {output_path}")

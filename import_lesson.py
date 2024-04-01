#!/usr/bin/env python3

import os
import json
import logging
import argparse


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    parser = argparse.ArgumentParser(description='Import a lesson to a course')

    parser.add_argument('-c', '--course-path', help='The path to the course.', required=True)
    parser.add_argument('-v', '--video-link', help='The link to the video.', required=True)

    # Parse the arguments
    args = parser.parse_args()

    logging.info(f'{args.course_path} {args.video_link}')


if __name__ == "__main__":
    main()
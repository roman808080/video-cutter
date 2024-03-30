#!/usr/bin/env python3

import random

def generate_id():
    return random.randrange(1 << 30, 1 << 31)

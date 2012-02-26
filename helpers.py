# -*- coding: utf-8 -*-

import string
import random

def random_code():
    """Generates random code for image"""

    return ''.join([random.choice(string.letters) for _ in range(5)])
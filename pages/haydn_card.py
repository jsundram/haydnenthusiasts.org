"""
Context generator for the Haydn Info Card
"""

import os
from pathlib import Path
from datetime import datetime


def get_context():
    card_root = Path('./external/haydn-info-card/output/')

    # Get sorted PDF files based on dates in filenames
    # filenames look like 'Haydn Info Card - Sundram - 2024-04-14.pdf'
    latest_card = sorted(
        card_root.glob('*.pdf'),
        key=lambda f: datetime.strptime(f.stem.split(' - ')[-1], '%Y-%m-%d'),
        reverse=True
    )[0]
    # if this barfs on the line above because the list is empty, you may need
    # to `git submodule update --init --recursive` to pull in haydn-info-card

    return {'card': latest_card.name}

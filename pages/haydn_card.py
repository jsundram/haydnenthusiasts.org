"""
Context generator for the Haydn Info Card
"""

from pathlib import Path
from datetime import datetime


def get_context():
    card_root = Path('./external/haydn-info-card/output/')

    # Filenames look like 'Haydn Info Card - Sundram - 2024-04-14.pdf'
    # Parse the date part out of the filename, and get the latest one.
    latest_card = max(
        card_root.glob('*.pdf'),
        key=lambda f: datetime.strptime(f.stem.split(' - ')[-1], '%Y-%m-%d'),
    )
    # If this barfs on the line above because the list is empty, you may need
    # to `git submodule update --init --recursive` to pull in haydn-info-card

    return {'card': latest_card.name}

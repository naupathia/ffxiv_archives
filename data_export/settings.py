
import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = f"{ROOT_PATH}\\_dumps\\input"
OUTPUT_PATH = f"{ROOT_PATH}\\_dumps\\output"

SKIP_LINES = 3
SPEAKER_SKIPS = ("SEQ", "TODO",)
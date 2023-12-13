import os

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
INPUT_PATH = f"{ROOT_PATH}\\_dumps\\input"

VERSION_NAME = os.listdir(INPUT_PATH)[-1]

DATA_PATH = f"{INPUT_PATH}\\{VERSION_NAME}\\exd"
OUTPUT_PATH = f"{ROOT_PATH}\\_dumps\\output"

import pathlib
from data_export.settings import DATA_PATH, OUTPUT_PATH
from . import scrub

def output_cutscenes():

    docs = []
    
    dir = pathlib.Path(f"{DATA_PATH}\\cut_scene")

    with open(f"{OUTPUT_PATH}\\cut_scenes.txt", "w+", encoding="UTF-8") as fh:

        for file_path in scrub.iter_dir_files(dir):

            file_name = file_path.stem
            contents = scrub.parse_speaker_transcript(file_path, 4)

            result = {
                "file_name": file_name,
                "transcript": contents,
                "raw": scrub.flatten_speaker_dialogue(contents)
            }
            result["data_type"] = "CUTSCENE"

            fh.write('\n')
            fh.write('---------------------------------------------------------------------')
            fh.write('\n')
            fh.write(scrub.print_speaker_dialogue(contents))
            fh.write('\n')

            print(f'processed cutscene: {file_name}')

            docs.append(result)

    return docs
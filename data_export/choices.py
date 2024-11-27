

INPUT_FILE = 'C:\\Users\\naupa.LAURENPC2\\dev\\ffxiv_archives\\data_export\\_dumps\\output\\dump.txt'
CUTSCENES_TEXT = 'Cutscenes '

def count_dialogue_choices():

    total_counts = {}

    with open(INPUT_FILE, 'rt', encoding="UTF-8") as fh:
        text = fh.read()
        scenes = text.split('[CUTSCENE]')
        for scene in scenes:
            # print('parsing cutscene')
            # print(scene)
            pos = scene.find(CUTSCENES_TEXT)
            if pos <= 0:
                continue

            xpac = scene[pos + 10:pos + 11]
            print(f'xpac num: {xpac}')

            counts = scene.count('What will you say?')

            if xpac in total_counts:
                total_counts[xpac] += counts
            else:
                total_counts[xpac] = counts


    print(total_counts)


import os
from scipy.misc import imread


def _gen(params, stride=1, offset=0, infinite=False):
    filenames, data_split, phase, base_dir = params

    loop_condition = True
    while loop_condition:
        for idx in range(offset, len(filenames), stride):
            filename = filenames[idx]
            image = os.path.join(base_dir, filename.replace("_annotated.png", ".png"))

            if data_split and idx % data_split == 0 and phase == PHASE_TRAIN:
                continue

            if data_split and idx % data_split != 0 and phase == PHASE_VALIDATION:
                continue

            feature = imread(image, mode="RGB")
            label = imread(filename, mode="RGB")
            yield ({"image": feature},
                   {"label": label})
        loop_condition = infinite


def kamaro_robotour(base_dir, phase, data_split=10):
    filenames = [f for f in os.listdir(os.path.join(base_dir)) if f.endswith("_annotated.png")]

    return _gen, (filenames, data_split, phase, base_dir)

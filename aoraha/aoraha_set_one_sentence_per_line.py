import os

DATASET_FILENAME = "assembled_aoraha_dataset.txt"
PROCESSED_FILENAME = "aoraha_opsl.txt"

data = open(os.path.join("data", DATASET_FILENAME), "r", encoding="utf-8").read()


with open(os.path.join("data", PROCESSED_FILENAME), "wb") as f:
    x = data.replace("\n", " ")
    x = x.replace(". ", ".\n").replace("\n ", "\n")
    f.write(x.encode("utf-8"))
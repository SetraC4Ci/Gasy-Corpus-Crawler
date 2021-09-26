import os

arr = os.listdir("./data/")

with open(os.path.join("data", "assembled_aoraha_dataset.txt"), "wb") as f:
    for filename in arr:
        if(filename.startswith("aoraha") and filename.endswith(".txt")):
            with open(os.path.join("data", filename), "r", encoding="utf-8") as infile:
                for line in infile:
                    f.write(line.encode("utf-8"))

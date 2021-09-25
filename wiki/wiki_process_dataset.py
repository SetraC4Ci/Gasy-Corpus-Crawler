import os

with open(os.path.join("data", "processed_wiki_dataset.txt"), "ab") as f:
    with open(os.path.join("data", "assembled_wiki_dataset.txt"), "r", encoding="utf-8") as inf:
        for line in inf:
            s = line.split(" ")
            if len(s) > 3 and not line.strip().endswith(")") and not "Ity no lisitry ny zavatra madinidinika ao amin'ny habakabaka." in line and not line.strip().startswith("Hita tao amin'ny") and not "Misy zavatra tsy ampy anatin'ity fizaràna ity" in line:
                f.write(line.encode("utf-8"))

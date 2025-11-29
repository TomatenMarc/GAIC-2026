import pandas as pd
from pathlib import Path
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/ABSTRCT"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_abstrct = df_sample[df_sample["dataset"] == "ABSTRCT"]

df_abstrct = df_abstrct.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_abstrct['dataset_id_clean'] = (
    df_abstrct['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

valid_ids = set(df_abstrct['dataset_id_clean'])
data_dir = Path(os.getcwd()+"/data/")  # <-- update if needed

# remove all .ann files
for ann_file in data_dir.glob("*.ann"):
    os.remove(ann_file)

for txt_file in data_dir.glob("*.txt"):
    if txt_file.stem not in valid_ids:
        os.remove(txt_file)

txt_found = [i.stem for i in list(data_dir.glob("*.txt"))]
assert sorted(valid_ids) == sorted(txt_found), "Every sample has a .txt file."

for _, row in df_abstrct.iterrows():
    file = open(os.getcwd() + "/data/" + row.dataset_id_clean + ".txt")
    assert row.sentence in file.read(), f"{row.sentence} not in {row.sentence}."

df_abstrct["dataset_id"] = df_abstrct["dataset"] + "-" + df_abstrct["dataset_id"]
df_abstrct.rename(columns={"dataset_id": "id"}, inplace=True)
df_abstrct = df_abstrct[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_abstrct.rename(columns={"dataset_id_clean": "document"}, inplace=True)
df_abstrct["document"] = df_abstrct["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_abstrct["guidelines"] = f"{base_url}/guidelines/AnnotationGuidelines.pdf"
df_abstrct["paper"] = "https://ecai2020.eu/papers/1470_paper"

df_abstrct.info()
df_abstrct = df_abstrct[["id", "paper", "document", "guidelines", "split", "label", "sentence"]]

for split in ["train", "dev", "test"]:
    df_ = df_abstrct[df_abstrct["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"ABSTRCT-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/abstrct_{split}.jsonl", orient="records", lines=True)
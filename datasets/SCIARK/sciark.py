import pandas as pd
from pathlib import Path
import json
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/SCIARK"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_sciark = df_sample[df_sample["dataset"] == "SCIARK"]

df_sciark = df_sciark.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_sciark['dataset_id_clean'] = (
    df_sciark['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

valid_ids = set(df_sciark['dataset_id_clean'])
data_dir = Path(os.getcwd()+"/data/")  # <-- update if needed

with open(os.getcwd() + "/data/SciARK.json", "r", encoding="utf-8") as f:
    text_data = json.load(f)
    text_data = {
        key.replace(".txt", ""): value
        for key, value in text_data.items()
    }

for id in valid_ids:
    assert id in text_data.keys()
    with open(os.getcwd() + "/data/" + id.replace("/", "_").replace(" ", "_") + ".txt", "w", encoding="utf-8") as out:
        out.write("\n".join(text_data[id]["sentences"]))

df_sciark["dataset_id"] = df_sciark["dataset_id"].apply(lambda row: row.replace("/", "_").replace(" ", "_"))
df_sciark["dataset_id_clean"] = df_sciark["dataset_id_clean"].apply(lambda row: row.replace("/", "_").replace(" ", "_"))

valid_ids = set(df_sciark['dataset_id_clean'])

for file in data_dir.glob("*.txt"):
    if file.stem not in valid_ids:
        os.remove(file)

os.remove(os.getcwd() + "/data/SciARK.json")
txt_files = set([file.stem for file in data_dir.glob("*.txt")])
assert sorted(txt_files) == sorted(valid_ids)
assert sorted(txt_files) == sorted(set((df_sciark['dataset_id'].str.rsplit('_', n=1).str[0])))

for _, row in df_sciark.iterrows():
    file = open(os.getcwd() + "/data/" + row.dataset_id_clean + ".txt")
    assert row.sentence in file.read(), f"{row.sentence} not in {row.dataset_id_clean}."

df_sciark["dataset_id"] = df_sciark["dataset"] + "-" + df_sciark["dataset_id"]
df_sciark.rename(columns={"dataset_id": "id"}, inplace=True)
df_sciark = df_sciark[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_sciark.rename(columns={"dataset_id_clean": "document"}, inplace=True)

unique_document_names = df_sciark["document"].unique()
anonymized_document_names = [f"SCIARK-{i+1}" for i in range(len(unique_document_names))]

for original, new in zip(unique_document_names, anonymized_document_names):
    os.rename(os.getcwd() + "/data/" + original + ".txt", os.getcwd() + "/data/" + new + ".txt")

df_sciark["document"] = df_sciark["document"].apply(lambda row: dict(zip(unique_document_names, anonymized_document_names))[row])
df_sciark["document"] = df_sciark["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_sciark["guidelines"] = "-"
df_sciark["paper"] = f"{base_url}/paper/SCIARK.pdf"

df_sciark.info()
df_sciark = df_sciark[["id", "paper", "document", "guidelines", "split", "label", "sentence"]]
for split in ["train", "dev", "test"]:
    df_ = df_sciark[df_sciark["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"SCIARK-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/sciark_{split}.jsonl", orient="records", lines=True)

for txt_file in data_dir.glob("*.txt"):
    if txt_file.stem not in anonymized_document_names:
        os.remove(txt_file)
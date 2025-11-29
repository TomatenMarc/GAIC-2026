import pandas as pd
from pathlib import Path
import json
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/FINARG"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_finarg = df_sample[df_sample["dataset"] == "FINARG"]

df_finarg = df_finarg.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")
df_finarg["sentence"] = df_finarg["sentence"].apply(lambda row: row.replace("I' ll", "I'll") if "I' ll" in row else row)

df_finarg['dataset_id_clean'] = (
    df_finarg['dataset_id']
    .str.rsplit('_', n=2)
    .str[0]
)

#print(len(set(df_finarg[df_finarg["split"] == "test"]["dataset_id_clean"].unique()) - set(df_finarg[df_finarg["split"] != "test"]["dataset_id_clean"].unique())))

valid_ids = set(df_finarg['dataset_id_clean'])
data_dir = Path(os.getcwd()+"/data/")  # <-- update if needed

for txt_file in data_dir.glob("*.json"):
    if txt_file.stem not in valid_ids:
        os.remove(txt_file)


json_found = [i.stem for i in list(data_dir.glob("*.json"))]
if len(json_found) > 0:
    assert sorted(valid_ids) == sorted(json_found) or sorted(valid_ids) == sorted(txt_found), "Not every sample has a .json or .txt file."
    for _, row in df_finarg.iterrows():
        path = os.getcwd() + "/data/" + row.dataset_id_clean + ".json"
        with open(path, "r", encoding="utf-8") as f:
            text_data = json.load(f)["data"]["my_text"]
        with open(path.replace('.json', '.txt'), "w", encoding="utf-8") as out:
            out.write(text_data)

    for txt_file in data_dir.glob("*.json"):
        os.remove(txt_file)
txt_found = [i.stem for i in list(data_dir.glob("*.txt"))]
assert sorted(valid_ids) == sorted(txt_found), "Not every sample has a .txt file."
for _, row in df_finarg.iterrows():
    file = open(os.getcwd() + "/data/" + row.dataset_id_clean + ".txt")
    assert row.sentence in file.read(), f"{row.sentence} not in {row.dataset_id_clean}."


df_finarg["dataset_id"] = df_finarg["dataset"] + "-" + df_finarg["dataset_id"]
df_finarg.rename(columns={"dataset_id": "id"}, inplace=True)
df_finarg = df_finarg[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_finarg.rename(columns={"dataset_id_clean": "document"}, inplace=True)
df_finarg["document"] = df_finarg["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_finarg["guidelines"] = "-"
df_finarg["paper"] = "https://aclanthology.org/2022.finnlp-1.22/"

for split in ["train", "dev", "test"]:
    df_ = df_finarg[df_finarg["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"FINARG-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/finarg_{split}.jsonl", orient="records", lines=True)
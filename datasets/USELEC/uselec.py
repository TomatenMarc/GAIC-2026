import pandas as pd
from pathlib import Path
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/USELEC"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_uselec = df_sample[df_sample["dataset"] == "USELEC"]

df_uselec = df_uselec.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_uselec['dataset_id_clean'] = (
    df_uselec['dataset_id']
    .str.rsplit('_', n=2)
    .str[0]
)

valid_ids = set(df_uselec['dataset_id_clean'])
data_dir = Path(os.getcwd()+"/data/")  # <-- update if needed

for txt_file in data_dir.glob("*.txt"):
    if txt_file.stem not in valid_ids:
        os.remove(txt_file)

txt_found = [i.stem for i in list(data_dir.glob("*.txt"))]
assert sorted(valid_ids) == sorted(txt_found), "Not every sample has a .txt file."

for _, row in df_uselec.iterrows():
    file = open(os.getcwd() + "/data/" + row.dataset_id_clean + ".txt")
    assert row.sentence in file.read(), f"{row.sentence} not in {row.sentence}."

df_uselec["dataset_id"] = df_uselec["dataset"] + "-" + df_uselec["dataset_id"]
df_uselec.rename(columns={"dataset_id": "id"}, inplace=True)
df_uselec = df_uselec[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_uselec.rename(columns={"dataset_id_clean": "document"}, inplace=True)

unique_document_names = df_uselec["document"].unique()
anonymized_document_names = [f"USELEC-{i+1}" for i in range(len(unique_document_names))]

for original, new in zip(unique_document_names, anonymized_document_names):
    os.rename(os.getcwd() + "/data/" + original + ".txt", os.getcwd() + "/data/" + new + ".txt")

df_uselec["document"] = df_uselec["document"].apply(lambda row: dict(zip(unique_document_names, anonymized_document_names))[row])
df_uselec["document"] = df_uselec["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_uselec["guidelines"] = f"{base_url}/guidelines/ElectDeb60To16_Guidelines.pdf"
df_uselec["paper"] = f"{base_url}/paper/USELEC.pdf"

df_uselec.info()
df_uselec = df_uselec[["id", "paper", "document", "guidelines", "split", "label", "sentence"]]

for split in ["train", "dev", "test"]:
    df_ = df_uselec[df_uselec["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"USELEC-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/uselec_{split}.jsonl", orient="records", lines=True)

for txt_file in data_dir.glob("*.txt"):
    if txt_file.stem not in anonymized_document_names:
        os.remove(txt_file)
import pandas as pd
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/AFS"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_afs = df_sample[df_sample["dataset"] == "AFS"]

df_afs = df_afs.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_afs['dataset_id_clean'] = (
    df_afs['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

df_afs.rename(columns={"dataset_id": "id"}, inplace=True)
df_afs = df_afs[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_afs.rename(columns={"dataset_id_clean": "document"}, inplace=True)

df_afs["document"] = "-"
df_afs["guidelines"] = "-"
df_afs["paper"] = "https://aclanthology.org/W16-3636.pdf"

for split in ["train", "dev", "test"]:
    df_ = df_afs[df_afs["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"AFS-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/afs_{split}.jsonl", orient="records", lines=True)
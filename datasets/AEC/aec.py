import pandas as pd
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/AEC"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_aec = df_sample[df_sample["dataset"] == "AEC"]

df_aec = df_aec.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_aec['dataset_id_clean'] = (
    df_aec['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

df_aec.rename(columns={"dataset_id": "id"}, inplace=True)
df_aec = df_aec[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_aec.rename(columns={"dataset_id_clean": "document"}, inplace=True)

df_aec["document"] = "-"
df_aec["guidelines"] = "-"
df_aec["paper"] = "https://aclanthology.org/W15-4631.pdf"

for split in ["train", "dev", "test"]:
    df_ = df_aec[df_aec["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"AEC-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/aec_{split}.jsonl", orient="records", lines=True)
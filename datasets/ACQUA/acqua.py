import pandas as pd
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/ACQUA"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_acqua = df_sample[df_sample["dataset"] == "ACQUA"]

df_acqua = df_acqua.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_acqua['dataset_id_clean'] = (
    df_acqua['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

df_acqua.rename(columns={"dataset_id": "id"}, inplace=True)
df_acqua = df_acqua[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_acqua.rename(columns={"dataset_id_clean": "document"}, inplace=True)

df_acqua["document"] = "-"
df_acqua["guidelines"] = "-"
df_acqua["paper"] = "https://aclanthology.org/W19-4516.pdf"

for split in ["train", "dev", "test"]:
    df_ = df_acqua[df_acqua["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"ACQUA-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/acqua_{split}.jsonl", orient="records", lines=True)
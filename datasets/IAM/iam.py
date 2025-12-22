import pandas as pd
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/IAM"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_iam = df_sample[df_sample["dataset"] == "IAM"]

df_iam = df_iam.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_iam['dataset_id_clean'] = (
    df_iam['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

df_iam.rename(columns={"dataset_id": "id"}, inplace=True)
df_iam = df_iam[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_iam.rename(columns={"dataset_id_clean": "document"}, inplace=True)

df_iam["document"] = "-"
df_iam["guidelines"] = "-"
df_iam["paper"] = f"{base_url}/paper/IAM.pdf"

for split in ["train", "dev", "test"]:
    df_ = df_iam[df_iam["split"] == split]
    print(df_.info())
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"IAM-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/iam_{split}.jsonl", orient="records", lines=True)
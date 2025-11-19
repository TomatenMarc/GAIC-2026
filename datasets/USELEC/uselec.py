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

df_uselec = df_uselec[["dataset", "dataset_id", "dataset_id_clean", "label", "sentence", "split"]]
df_uselec.rename(columns={"dataset_id_clean": "document"}, inplace=True)
df_uselec["document"] = df_uselec["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_uselec["guidelines"] = f"{base_url}/guidelines/ElectDeb60To16_Guidelines.pdf"
df_uselec["paper"] = "https://aclanthology.org/P19-1463/"

df_uselec = df_uselec[["dataset", "dataset_id", "paper", "document", "guidelines", "split", "label", "sentence"]]
df_uselec.to_csv(os.getcwd() + "/uselec.csv")
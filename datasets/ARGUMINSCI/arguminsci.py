import pandas as pd
from pathlib import Path
import os

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/ARGUMINSCI"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_arguminsci = df_sample[df_sample["dataset"] == "ARGUMINSCI"]

df_arguminsci = df_arguminsci.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_arguminsci['dataset_id_clean'] = (
    df_arguminsci['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

valid_ids = set(df_arguminsci['dataset_id_clean'])
data_dir = Path(os.getcwd()+"/data/")  # <-- update if needed

for txt_file in data_dir.glob("*.txt"):
    if txt_file.stem not in valid_ids:
        os.remove(txt_file)

txt_found = [i.stem for i in list(data_dir.glob("*.txt"))]
assert sorted(valid_ids) == sorted(txt_found), "Every sample has a .txt file."


for _, row in df_arguminsci.iterrows():
    file = open(os.getcwd() + "/data/" + row.dataset_id_clean + ".txt")
    assert row.sentence in file.read(), f"{row.sentence} not in {row.sentence}."



df_arguminsci = df_arguminsci[["dataset", "dataset_id", "dataset_id_clean", "label", "sentence", "split"]]
df_arguminsci.rename(columns={"dataset_id_clean": "document"}, inplace=True)
df_arguminsci["document"] = df_arguminsci["document"].apply(lambda row: f"{base_url}/data/{row}.txt")
df_arguminsci["guidelines"] = "-"
df_arguminsci["paper"] = "https://www.aclweb.org/anthology/W18-5206/"

df_arguminsci = df_arguminsci[["dataset", "dataset_id", "paper", "document", "guidelines", "split", "label", "sentence"]]
df_arguminsci.to_csv(os.getcwd() + "/arguminsci.csv")

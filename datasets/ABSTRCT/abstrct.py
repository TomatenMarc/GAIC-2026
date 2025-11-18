import pandas as pd
from pathlib import Path
import os

base_url = "https://github.com/TomatenMarc/GAIC-2026/"

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

print(df_abstrct.columns)

df_abstrct = df_abstrct[["dataset", "dataset_id", "dataset_id_clean", "label", "sentence"]]
df_abstrct.rename(columns={"dataset_id_clean": "document"}, inplace=True)
df_abstrct["document"] = df_abstrct["document"].apply(lambda row: f"{base_url}{row}.txt")

print(df_abstrct["document"])

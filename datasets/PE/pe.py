import pandas as pd
from pathlib import Path
import re
import os


def normalize_spacing(text: str) -> str:
    text = re.sub(r"\s*-\s*-\s*", " — ", text)
    text = re.sub(r"\s+-\s+", " — ", text)
    text = re.sub(r"\s*([/+])\s*", r"\1", text)
    text = re.sub(r"(\d),\s+(\d{3})", r"\1,\2", text)
    text = re.sub(r"\(\s+", "(", text)     # "( for example" -> "(for example"
    text = re.sub(r"\s+\)", ")", text)     # "company )" -> "company)"
    text = re.sub(r"\)([A-Za-z])", r") \1", text)
    text = re.sub(r"(\w)\s*’\s*(\w)", r"\1’\2", text)
    text = re.sub(r"(\w)\s+'\s*(\w)", r"\1'\2", text)
    text = re.sub(r"(\w)\s+'([,.;:!?])", r"\1'\2", text)
    text = re.sub(r"(s')(\w)", r"\1 \2", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,.;:!?])(?!\s|$)", r"\1 ", text)
    text = re.sub(r'(["“”])\s*(.*?)\s*(["“”])', r'\1\2\3', text)
    text = re.sub(r'(‘)\s*(.*?)\s*(’)', r'\1\2\3', text)
    text = re.sub(r'([A-Za-z0-9,])(["“‘])', r'\1 \2', text)
    text = re.sub(r'([”"’])([A-Za-z0-9])', r'\1 \2', text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"’\s+", "’", text)
    text = re.sub(r'(["“”])\s*(.*?)\s*(["“”])', r'\1\2\3', text)
    text = re.sub(r"(\w)'\s*(\w.*?)\s*'", r"\1 '\2'", text)
    return text.strip()

def rules(text):
    text = text.replace("' dug'deeper", "'dug' deeper")
    text = text.replace("'dug'deeper", "'dug' deeper")
    text = text.replace("one 's parents'", "one's parents'")
    text = text.replace("what 's", "what's")
    text = text.replace("as food,", "as food ,")
    text = text.replace("past 's", "past's")
    text = text.replace("people 's", "people's")
    text = text.replace("‘Trong Dong’drum", "‘Trong Dong’ drum")
    text = text.replace("‘Ha Long’bay", "‘Ha Long’ bay")
    text = text.replace("buildings — whether", "buildings -- whether")
    text = text.replace("they 've", "they've")
    text = text.replace("earth 's", "earth's")
    text = text.replace("What 's", "What's")
    text = text.replace("students’solid", "students’ solid")
    text = text.replace('"Keep running! ,"', '"Keep running!,"')
    text = text.replace("country —", "country-")
    text = text.replace("company — Apple —", "company- Apple-")
    text = text.replace("satiric, which", "satiric,which")
    text = text.replace("US — half", "US - half")
    text = text.replace("A+for", "A+ for")
    text = text.replace("40, 000", "40,000")
    text = text.replace("people'attention", "people' attention")
    text = text.replace("one 's", "one's")
    text = text.replace("— few close friends or a large number of friends —", "- few close friends or a large number of friends -")
    text = text.replace("it 's", "it's")
    text = text.replace("student'study", "student' study")
    text = text.replace("people'knowledge", "people' knowledge")
    text = text.replace("students 'attention", "students' attention")
    text = text.replace("factor — spiritual", "factor - spiritual")
    text = text.replace("cities' s", "cities's")
    text = text.replace("— socialization —", "- socialization-")
    text = text.replace("parents '", "parents'")
    text = text.replace("learn '", "learn'")
    text = text.replace("below: Competitive", "below:\nCompetitive")
    return text

base_url = "https://raw.githubusercontent.com/TomatenMarc/GAIC-2026/refs/heads/main/datasets/PE"

df_all = pd.read_csv('../../assets/all_data.csv')
df_sample = pd.read_csv('../../assets/sample_42.csv')
df_sample.rename(columns={"sentence": "processed_sentence"}, inplace=True)

df_pe = df_sample[df_sample["dataset"] == "PE"]

df_pe = df_pe.merge(df_all[["dataset_id", "sentence"]], on="dataset_id")

df_pe['dataset_id_clean'] = (
    df_pe['dataset_id']
    .str.rsplit('_', n=1)
    .str[0]
)

df_pe.rename(columns={"dataset_id": "id"}, inplace=True)
df_pe = df_pe[["id", "dataset_id_clean", "label", "sentence", "split"]]
df_pe.rename(columns={"dataset_id_clean": "document"}, inplace=True)


df_pe["sentence"] = df_pe["sentence"].apply(lambda x: rules(normalize_spacing(x)))
base_dir = Path(os.getcwd()) / "data"
for idx, row in df_pe.iterrows():
    sentence = row["sentence"]

    for file in base_dir.glob("*.txt"):
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()

        if sentence in text:
            df_pe.at[idx, "document"] = base_url + f"/data/{file.stem}.txt"
            break  # no need to check other files for this sentence

assert df_pe["document"].apply(lambda x: x.startswith("http")).all()

valid_ids = set(df_pe["document"].apply(lambda x: x.split("/")[-1].replace('.txt', '')).to_list())
for txt_file in Path(os.getcwd()+"/data/").glob("*.txt"):
    if txt_file.stem not in valid_ids:
        os.remove(txt_file)

df_pe["guidelines"] = f"{base_url}/guidelines/AnnotationGuidelines.pdf"
df_pe["paper"] = f"{base_url}/paper/PE.pdf"

for split in ["train", "dev", "test"]:
    df_ = df_pe[df_pe["split"] == split]
    df_ = df_[["id", "paper", "document", "guidelines", "label", "sentence"]]
    df_ = df_.reset_index(drop=True)
    df_["id"] = f"PE-{split}-" + (df_.index + 1).astype(str)
    df_.to_json(os.getcwd() + f"/pe_{split}.jsonl", orient="records", lines=True)
# :sparkles:GAIC-2026:sparkles:

## :hear_no_evil: Generalizability of Argument Identification in Context (GAIC) — CLEF 2026

This repository contains the datasets for the *Generalizability of Argument Identification in Context* shared task at [Touché](https://touche.webis.de/clef26/touche26-web/generalizable-argument-mining.html) @ [CLEF 2026](https://clef2026.clef-initiative.eu).
Participants are asked to build models that classify whether a sentence (with context and metadata) is an *Argument* or *No-Argument* sentence 
across diverse sources.

---

## :floppy_disk: Benchmark Overview

The table below lists the dataset folders in this repository under `./data/`.

⚠️ **Please cite the respective papers!**

| Dataset Folder | Description                                                                                                  | Source                                        | License              |
|----------------|--------------------------------------------------------------------------------------------------------------|-----------------------------------------------|----------------------|
| `ABSTRCT`      | Argument mining dataset from academic abstracts.                                                             | https://ecai2020.eu/papers/1470_paper         | CC BY-NC-SA 4.0      |
| `ACQUA`        | Comparative sentences expressing preference or superiority (e.g. Matlab vs. Python) across multiple domains. | https://aclanthology.org/W19-4516/            | CC BY 4.0            |
| `AEC`          | Sentences collected from discussions on the CreateDebate platform.                                           | https://aclanthology.org/W15-4631/            | Approved by authors. |
| `AFS`          | Sentences drawn from online debate platforms such as ProCon and iDebate.                                     | https://aclanthology.org/W16-3636/            | Approved by authors. |
| `ARGUMINSCI`   | Sentences originating from the Dr. Inventor scientific argumentation corpus.                                 | https://aclanthology.org/W18-5206/            | Approved by authors. |
| `FINARG`       | Sentences extracted from financial earnings calls of publicly traded companies.                              | https://aclanthology.org/2022.finnlp-1.22/    | GNU GPL 3.0          |
| `IAM`          | Sentences gathered from heterogeneous web sources.                                                           | https://aclanthology.org/2022.acl-long.162/   | Free license.        |
| `PE`           | Sentences taken from student-written persuasive essays.                                                      | https://aclanthology.org/J17-3005/            | CC BY-NC-ND 4.0      |
| `SCIARK`       | Sentences from scientific literature, including biomedical research articles.                                | https://aclanthology.org/2021.argmining-1.10/ | Free license.        |
| `USELEC`       | Sentences from U.S. presidential election debates and related political discourse.                           | https://aclanthology.org/P19-1463/            | Free license.        |

---

## :point_up: Participation Instructions

1. Read and follow the requirements for the task requirements on the [Touché](https://touche.webis.de/clef26/touche26-web/generalizable-argument-mining.html) shared task page.
2. Download the data and follow the further guidelines on the [TIRA](https://www.tira.io) platform.

---

## :v: Notice

1. The respective `train/dev/test` splits will be published sequentially in `./data/` as separate files (e.g., `train.jsonl`).
2. Each `train/dev/test` split will have a separate file containing the labels (e.g. `train_labels.jsonl`).
3. The paths in each split are relative to the `./data/` working directory and point to the respective files (e.g., `./ABSTRCT/data/ABSTRCT-1.txt`).
4. The data here is equivalent to the one published on the [TIRA](https://www.tira.io) platform.

---

## :rocket: Release Notes
**14.01.26**: The training and development data is released.

**01.03.26 (tentative)**: The test data will be released.

---

## :information_desk_person: Contact
* [Marc Feger](mailto:marc.feger@uni-duesseldorf.de?subject=GAIC-2026)
* [Katarina Boland](mailto:katarina.boland@uni-duesseldorf.de?subject=GAIC-2026)
* [Julia Romberg](mailto:julia.romberg@gesis.org?subject=GAIC-2026)
* [Stefan Dietze](mailto:stefan.dietze@gesis.org?subject=GAIC-2026)
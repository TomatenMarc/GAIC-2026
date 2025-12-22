wget https://raw.githubusercontent.com/afergadis/SciARK/refs/heads/main/dataset/SciARK.json
mkdir -p ./data
mv SciARK.json ./data

mkdir -p ./paper
wget https://aclanthology.org/2021.argmining-1.10.pdf
mv ./2021.argmining-1.10.pdf ./paper/SCIARK.pdf
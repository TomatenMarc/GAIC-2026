wget https://github.com/ElecDeb60To16/Dataset/raw/refs/heads/master/ElecDeb60To16.zip
wget https://github.com/ElecDeb60To16/Dataset/raw/refs/heads/master/ElectDeb60To16_Guidelines.pdf
mkdir -p ./data
mkdir -p ./guidelines
unzip -o ElecDeb60To16.zip -d ./data
mv ElectDeb60To16_Guidelines.pdf ./guidelines
rm -r ElecDeb60To16.zip
rm -r ./data/*.ann

mkdir -p ./paper
wget https://aclanthology.org/P19-1463.pdf
mv ./P19-1463.pdf ./paper/USELEC.pdf
wget https://github.com/Alaa-Ah/The-FinArg-Dataset-Argument-Mining-in-Financial-Earnings-Calls/raw/refs/heads/main/FinArg.zip
wget https://raw.githubusercontent.com/Alaa-Ah/The-FinArg-Dataset-Argument-Mining-in-Financial-Earnings-Calls/refs/heads/main/LICENSE
mkdir -p data/

unzip FinArg.zip -d ./data
mv ./data/argument\ mining/* ./data

rm -r ./data/argument\ mining/
rm -r FinArg.zip
rm -r ./data/*.ann
wget http://data.dws.informatik.uni-mannheim.de/sci-arg/compiled_corpus.zip
mkdir -p ./data
unzip compiled_corpus.zip -d ./
mv ./compiled_corpus/* ./data

rm -r ./compiled_corpus.zip
rm -r ./compiled_corpus
rm -r ./data/*.ann
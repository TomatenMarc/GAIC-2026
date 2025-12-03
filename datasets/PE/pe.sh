wget "https://tudatalib.ulb.tu-darmstadt.de/bitstreams/1ae1718d-7e65-42ba-9e84-dbf52fe92f56/download" -O myfile.zip
mkdir -p ./data
mkdir -p ./guidelines
unzip -o myfile.zip -d ./data
unzip -o ./data/ArgumentAnnotatedEssays-2.0/brat-project-final.zip -d ./data
mv ./data/brat-project-final/*.txt ./data
mv ./data/ArgumentAnnotatedEssays-2.0/guideline.pdf ./guidelines/AnnotationGuidelines.pdf

rm -r -- ./data/__MACOSX
rm -r -- ./data/ArgumentAnnotatedEssays-2.0
rm -r -- ./data/brat-project-final
rm -r myfile.zip

i=1
for f in ./data/*.txt; do
    dir=$(dirname "$f")
    mv "$f" "$dir/PE_${i}.txt"
    i=$((i+1))
done

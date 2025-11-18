wget https://gitlab.com/tomaye/abstrct/-/archive/master/abstrct-master.zip
unzip -o abstrct-master.zip -d ./

# Define source and destination directories
src_dir="./abstrct-master/AbstRCT_corpus/data"
dest_dir="./data"

# Create destination directory if it doesn't exist
mkdir -p "$dest_dir"

# Iterate over all .ann files in the source directory
find "$src_dir" -type f -name "*.ann" | while read -r ann_file; do
    # Derive corresponding .txt file
    txt_file="${ann_file%.ann}.txt"

    # Check if the .txt file exists
    if [[ -f "$txt_file" ]]; then
        # Extract parent directory name
        parent_dir=$(basename "$(dirname "$ann_file")")

        # Get base filenames
        ann_filename=$(basename "$ann_file")
        txt_filename=$(basename "$txt_file")

        # Define new filenames with parent directory prefix
        new_ann="${parent_dir}_${ann_filename}"
        new_txt="${parent_dir}_${txt_filename}"

        # Copy .ann file if not already present
        if [[ ! -e "$dest_dir/$new_ann" ]]; then
            cp "$ann_file" "$dest_dir/$new_ann"
            echo "Copied: $new_ann"
        else
            echo "Skipped duplicate: $new_ann"
        fi

        # Copy .txt file if not already present
        if [[ ! -e "$dest_dir/$new_txt" ]]; then
            cp "$txt_file" "$dest_dir/$new_txt"
            echo "Copied: $new_txt"
        else
            echo "Skipped duplicate: $new_txt"
        fi
    else
        echo "Missing .txt for: $ann_file"
    fi
done

mkdir ./guidelines
mv ./abstrct-master/AbstRCT_corpus/AnnotationGuidelines.pdf ./guidelines/AnnotationGuidelines.pdf
rm -r abstrct-master.zip
rm -r abstrct-master
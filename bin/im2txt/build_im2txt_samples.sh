
pwd=`sudo pwd`
cd `dirname $0`
cd ../../samples/im2txt/

# Location to save the MSCOCO data.
MSCOCO_DIR="${HOME}/program/test/tensorFlow_test/samples/im2txt/im2txt/data/mscoco"

# Build the preprocessing script.
bazel build //im2txt:download_and_preprocess_mscoco

# Run the preprocessing script.
bazel-bin/im2txt/download_and_preprocess_mscoco "${MSCOCO_DIR}"

cd $pwd

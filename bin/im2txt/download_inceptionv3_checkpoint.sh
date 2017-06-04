
pwd=`sudo pwd`
cd `dirname $0`
cd ../../samples/im2txt/

# Location to save the Inception v3 checkpoint.
INCEPTION_DIR="${HOME}/program/test/tensorFlow_test/samples/im2txt/im2txt/data"
mkdir -p ${INCEPTION_DIR}

wget "http://download.tensorflow.org/models/inception_v3_2016_08_28.tar.gz"
tar -xvf "inception_v3_2016_08_28.tar.gz" -C ${INCEPTION_DIR}
rm "inception_v3_2016_08_28.tar.gz"

cd $pwd
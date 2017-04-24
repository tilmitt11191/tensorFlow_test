INSTALL_DIR=/usr/local/tensorflow
sudo apt-get install -y libcupti-dev
sudo apt-get install -y python-dev python-virtualenv 
sudo mkdir $INSTALL_DIR/
sudo chmod -R 755 $INSTALL_DIR
virtualenv --system-site-packages $INSTALL_DIR/
source ~/tensorflow/bin/activate
#cpu only
sudo pip3 install --upgrade tensorflow
#gpu support
sudo pip3 install --upgrade tensorflow-gpu
#https://www.tensorflow.org/install/install_linux#the_url_of_the_tensorflow_python_package
#python3.5
#cpu only
sudo pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow-1.0.1-cp35-cp35m-linux_x86_64.whl
#gpu support
sudo pip3 install --upgrade https://storage.googleapis.com/tensorflow/linux/gpu/tensorflow_gpu-1.0.1-cp35-cp35m-linux_x86_64.whl

mkdir tensorFlow_test
cd tensorFlow_test
python -v
python -V
pip
python -m pip -V
sudo apt-get install python-pip
sudo pip install --upgrade virtualenv
python -m pip -V
virtualenv --system-site-packages ~/lib/tensorflow
ls ~/lib/tensorflow
cd ~/lib/tensorflow
source bin/activate
pip install --upgrade tensorflow
python
pwd
cd ~/f/program/test/tensorFlow_test
ls
mkdir tutorials
cd tutorials

sudo pip3 install numpy
sudo pip install setuptools
sudo pip install theano

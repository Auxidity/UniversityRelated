Author : Daniel Kortesmaa

Dependancies of scripts stt.py & caller.py

```python
sudo apt install python3-pip

sudo apt install bison swig python3 python3-dev

sudo apt-get install libportaudio2 libportaudiocpp0 #Not 1000% sure this is neccesary. Used for another STT initially, switched away.  





sudo apt-get install portaudio19-dev

pip3 install SpeechRecognition

#Update ~/.bashrc with export PATH="$PATH:/home/{USERNAME}/.local/bin" if you get not in path warning

pip3 install pyaudio

```
Dependancies of file_reader.py 
```python
#This might change based on the GUI peoples preferred solution
sudo apt-get install python3-tk
```



Dependancies of api_call.py 
NOTE : deprecated

```python
pip3 install openai
```

Dependancies of python2 SDK

```python
sudo apt update && sudo apt upgrade

#Optionally dl IDE & Gedit for easier code manipulation

#dl the SDK and extract//I have the entire lib on git if needed

tar -xzf my.sdk.tar.gz -C /destination/folder/

#sudo apt install wget if wget missing

sudo apt install python2

wget https://bootstrap.pypa.io/pip/2.7/get-pip.py

sudo python2 get-pip.py



gedit ~/.bashrc

#At the very end of the file append the following
export PYTHONPATH=${PYTHONPATH}:PATH/TO/NAOQI/LIB/PYTHON2.7/site-packages/
export PATH=$PATH:/PATH/TO/PIP2/

source ~/.bashrc

sudo apt install python2.7-dev

#in IDE select python 2.7.18 for compiling (ctrl+shift + p -> python select interp´´´ reter -> 2.7.18 under usr/bin/python2)

# POSSIBLY need to link the naoqi in IDE and add to path inside IDE, should show as a quick fix. Possible to need .src file aswell with filepaths on project location

```

Application dependancies
```python
#api_call_memory.py
#gui_skeleton.py
#client_comm.py
#chatbot_text.py
```

Docker dependanices
```python
#Dockerfile can be used as is, can be cleaned up to not install the exceptions. Restructure later.

#Currently installs everything under scripts/

# Exceptions for later :  chatbot_text.py, client_comm.py & gui_skeleton.py
```

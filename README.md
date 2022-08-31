# Installation
```
cmsrel CMSSW_12_3_0
cd CMSSW_12_3_0
cmsenv
cd ..
python3 -m venv H3env
source H3env/bin/activate
pip install --upgrade pip
pip install coffea #Some errors reported here, but coffea is installed
pip install jupyter
git clone git@github.com:mroguljic/H3PO.git
```

# Running the notebooks
```
 cd H3PO
 jupyter notebook --no-browser --port=8889
```

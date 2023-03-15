#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /users/fbilandzija/CMSSW_12_3_0/
eval `scramv1 runtime -sh`
cd /users/fbilandzija/
source H3env/bin/activate

export WORK_DIR=/users/fbilandzija/H3PO/Analysis
cd /users/fbilandzija/H3PO/Analysis

echo $WORK_DIR/background.py $*
python $WORK_DIR/background.py $*

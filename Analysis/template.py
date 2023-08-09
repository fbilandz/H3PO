from paths import CMSSW_DIR, H3_DIR, H3ENV_DIR

selection_condor = """universe              = vanilla
executable            = EXEC
output                = OUTPUT/output_$(Process).out
error                 = OUTPUT/output_$(Process).err
log                   = OUTPUT/output_$(Process).log
Arguments = "$(args)"
use_x509userproxy = true
Queue args from ARGFILE
queue
"""

skim_template='''#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {0}
eval `scramv1 runtime -sh`
cd {1}
source H3env/bin/activate
export WORK_DIR={2}
cd JOB_DIR
echo $WORK_DIR/skimming.py $*
python $WORK_DIR/skimming.py $*
'''.format(CMSSW_DIR,H3ENV_DIR,H3_DIR)
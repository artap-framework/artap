#!/bin/sh

# args
s=$@

/opt/matlab-R2018b/bin/matlab -nodisplay -nosplash -nodesktop -r ${s%.m}

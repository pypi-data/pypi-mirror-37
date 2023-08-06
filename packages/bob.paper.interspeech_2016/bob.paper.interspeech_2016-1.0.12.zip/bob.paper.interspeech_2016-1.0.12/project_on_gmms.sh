
#name of the database
database=$1
#number of bands used to compute features
bands=$2
#features names
features=(scfc20 rfcc20 imfcc20 mfcc20 lfcc20 scmc20 ssfc20)

for f in "${features[@]}"; do
    echo "=============================================================="
    echo "Project on GMMs found for '${f}' features of ${database} database"
    echo "=============================================================="

    command="-d ${database} -P physical_access -p mod-4hz --preprocessed-directory preprocessing_mod4hz -e ${f}  --extracted-directory extracted_${f}_onlydeltas_${bands} -a gmm --projector-file Projector_gmm_${f}_onlydeltas_${bands}_spoof.hdf5 --projected-directory projected_gmm_${f}_onlydeltas_${bands} -s temp --score-directories gmm_${f}_onlydeltas_${bands} --groups dev eval -g modest --skip-projector-training -vv"

    echo $command
    bin/spoof.py  $command 
done



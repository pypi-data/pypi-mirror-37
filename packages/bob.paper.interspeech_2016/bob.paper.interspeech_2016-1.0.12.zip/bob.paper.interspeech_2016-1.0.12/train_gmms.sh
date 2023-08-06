
#name of the database
database=$1
#number of bands used to compute features
bands=$2

#features names
#features=(scfc20 rfcc20 imfcc20 mfcc20 lfcc20 scmc20 ssfc20)
features=(mfcc20)
#protocol names
protocols=(licit spoof)

for f in "${features[@]}"; do
  for p in "${protocols[@]}"; do
    echo "=============================================================="
    echo "Train GMM for '${f}' features using '${p}' protocol of '${database}' database"
    echo "=============================================================="
 
    command="-d ${database}-${p} -p mod-4hz --preprocessed-directory preprocessing_mod4hz -e ${f}  --extracted-directory extracted_${f}_onlydeltas_${bands} -a gmm-tomi --projector-file Projector_gmm_${f}_onlydeltas_${bands}_${p}.hdf5 -s temp --kmeans-directory kmeans_${f}_onlydeltas_${bands}_${p}   --gmm-directory gmm_${f}_onlydeltas_${bands}_${p} --groups world -g modest --skip-enroller-training -vv"

    echo $command
    bin/train_gmm.py  $command
  done
done



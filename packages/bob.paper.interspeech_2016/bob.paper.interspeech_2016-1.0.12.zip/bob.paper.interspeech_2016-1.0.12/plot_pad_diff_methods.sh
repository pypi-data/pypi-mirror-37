
# Specify path to the folder with results
prefix="./scores/"


function plot {

  titles=""
  realfiles=""
  attackfiles=""
  thr=""
  names=$1
  features=$2
  labels=$4
  thresholds=$3
  for i in "${!names[@]}"; do
    realfiles="$realfiles$prefix${names[$i]}/${features[$i]}/scores-eval-real "
    attackfiles="$attackfiles$prefix${names[$i]}/${features[$i]}/scores-eval-attack "
    titles="$titles${labels[$i]} "
    thr="$thr${thresholds[$i]} "
  done
  realfiles="$realfiles"
  attackfiles="$attackfiles"
  titles="$titles"
  thr="$thr"

  echo "bin/pad_diff_sys_scores.py -r $realfiles -a $attackfiles -l $titles --thresholds $thr  -o plots_compare_pads"

  bin/pad_diff_sys_scores.py -r $realfiles -a $attackfiles -l $titles --thresholds $thr -o plots_compare_pads
}

# uncomment to produce Figure 2(a) of the paper
#names=(avspoof_asvspoof2logic avspoof_asvspoof2phys asvspoof_pad)
#features=(gmm_mfcc20_onlydeltas_20 gmm_mfcc20_onlydeltas_20 gmm_mfcc20_onlydeltas_20)
#labels=('MFCC,AVspoof-LA(Eval)' 'MFCC,AVspoof-PA(Eval)' 'MFCC,ASVspoof(Eval)')
#thresholds=(0.289056 0.289056 0.289056)
#plot $names $features $thresholds $labels

# uncomment to produce Figure 2(b) of the paper
names=(avspoof_logic avspoof_logic2phys asvspoof_avspoof2pad)
features=(gmm_mfcc20_onlydeltas_20 gmm_mfcc20_onlydeltas_20 gmm_mfcc20_onlydeltas_20)
labels=('MFCC,AVspoof-LA(Eval)' 'MFCC,AVspoof-PA(Eval)' 'MFCC,ASVspoof(Eval)')
thresholds=(0.618269 0.618269 0.618269)
plot $names $features $thresholds $labels

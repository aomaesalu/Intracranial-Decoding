python2 ./descriptive_analysis.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl
python2 ./partition_data.py data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl data/train.pkl data/test.pkl
python2 ./svm.py data/train.pkl data/test.pkl
python2 ./random_forest.py data/train.pkl data/test.pkl

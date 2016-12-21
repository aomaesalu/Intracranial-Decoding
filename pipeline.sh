#!/bin/bash

# Define file paths
raw_data_file='data/stim_probe_category_ON_meangamma_bipolar_noscram_artif_brodmann_resppositive.pkl'
filtered_data_file='data/filtered.pkl'
partition_file='data/partition.pkl'
grid_search_file='data/results.pkl'
ensemble_file='data/ensemble.pkl'

# Set cross-validation parameters
partitions=10
iterations=10

# Set grid search parameters
trials=10000

# Split file name and extension
partition_file_name=${partition_file%.*}
partition_file_extension=${partition_file##*.}

# Filter the raw data by classes
printf '# Pipeline: Filtering data by classes'
python ./filter_by_class.py $raw_data_file $filtered_data_file 10 20 30 40 50
printf '\n\n'

# Descriptive analysis of the data set. This is not necessaryly a part of the
# pipeline, as the data set does not change, but it is still currently included
# for the purposes of clarity.
printf '# Pipeline: Descriptive analysis\n'
python ./descriptive_analysis.py $filtered_data_file
printf '\n'

# Data partitioning. We use stratified k-fold cross-validation N times.
printf '# Pipeline: Partitioning data %d times into %d equal sets\n' $iterations $partitions
for (( i=1; i<=iterations; i++ ))
do
    python ./partition_data.py $filtered_data_file $partition_file_name'-'$i'.'$partition_file_extension $partitions --even
done
printf '\n'

# Classification and grid search
printf '# Pipeline: Classification and grid search\n'
python ./classify.py $partition_file $grid_search_file $partitions $iterations $trials
printf '\n'

# Ensemble construction, classification and scoring
printf '# Pipeline: Ensemble construction, classification and scoring\n'
python ./ensemble.py $partition_file $partitions $iterations $grid_search_file 0.1 0.1 $ensemble_file
printf '\n'

#!/bin/bash
#The name of the job is pipeline_simple
#SBATCH -J pipeline_simple
 
#The job requires 100 compute nodes
#SBATCH -N 100
 
#The job requires 1 task per node
#SBATCH --ntasks-per-node=1
 
#The maximum walltime of the job is a 2 hours
#SBATCH -t 02:00:00
 
#Here we call srun to launch the uname command in parallel

# This pipeline is used either on a local computer or a remote server. Grid
# search is applied to all of the algorithms in question. Only the best
# classification function and parameters are returned for each input file.

# TODO: Heatmaps

function strrep {
  replaced=${1/TIMEWINDOW/$2}
  echo ${replaced//FREQUENCYBAND/$3}
}

# Define raw file_paths
raw_data_file='data/raw/stim_probe_category_ON_meanFREQUENCYBAND_LFP_bipolar_noscram_artif_brodmann_wTIMEWINDOW_FREQUENCYBAND_resppositive.pkl'
raw_filtered_data_file='data/filtered/TIMEWINDOW_FREQUENCYBAND.pkl'
raw_partitioned_data_file='data/partitioned/TIMEWINDOW_FREQUENCYBAND.pkl'
raw_classification_file='data/classification/TIMEWINDOW_FREQUENCYBAND.pkl'
raw_classification_score_file='data/score/TIMEWINDOW_FREQUENCYBAND.pkl'
result_file='data/result/result_simple.pkl'
result_plot_file='plots/result_simple.png'

# Initialise the values of time windows and frequency bands researched
time_windows="50 150 250"
frequency_bands="theta alpha beta lowgamma highgamma"

# Set cross-validation parameters
partitions=10
iterations=10

# Iterate through each time window
for time_window in $time_windows
do

  # Iterate through each frequency band
  for frequency_band in $frequency_bands
  do

    # Construct file names specific to the current time window and freqeuncy
    # band
    data_file=$(strrep $raw_data_file $time_window $frequency_band)
    filtered_data_file=$(strrep $raw_filtered_data_file $time_window $frequency_band)
    partitioned_data_file=$(strrep $raw_partitioned_data_file $time_window $frequency_band)
    classification_file=$(strrep $raw_classification_file $time_window $frequency_band)
    classification_score_file=$(strrep $raw_classification_score_file $time_window $frequency_band)

    # Split file name and extension
    partitioned_data_file_name=${partitioned_data_file%.*}
    partitioned_data_file_extension=${partitioned_data_file##*.}

    # Filter the raw data by classes
    printf '# Pipeline (%d, %s): Filtering data by classes' $time_window $frequency_band
    srun python ./filter_by_class.py $data_file $filtered_data_file 10 20 30 40 50
    printf '\n\n'

    # # Descriptive analysis of the data set. This is not necessaryly a part of
    # # the pipeline, as the data set does not change, but it is still currently
    # # included for the purposes of clarity.
    # printf '# Pipeline (%d, %s): Descriptive analysis\n' $time_window $frequency_band
    # python ./descriptive_analysis.py $filtered_data_file
    # printf '\n'

    # Data partitioning. We use stratified k-fold cross-validation N times.
    printf '# Pipeline (%d, %s): Partitioning data %d times into %d equal sets\n' $time_window $frequency_band $iterations $partitions
    for (( i=1; i<=iterations; i++ ))
    do
        srun python ./partition_data.py $filtered_data_file $partitioned_data_file_name'-'$i'.'$partitioned_data_file_extension $partitions --even
    done
    printf '\n'

    # Classification
    printf '# Pipeline (%d, %s): Classification\n' $time_window $frequency_band
    srun python ./classify.py $partitioned_data_file $classification_file $partitions $iterations
    printf '\n'

    # Filter the best result
    printf '# Pipeline (%d, %s): Result selection\n' $time_window $frequency_band
    srun python ./filter_best.py $classification_file $classification_score_file
    printf '\n'

  done

done

# Integrate the ensemble scores for all of the different time windows and
# frequency bands
srun python ./integrate_scores.py $raw_classification_score_file $result_file "${time_windows}" "${frequency_bands}"

# Visualise the integrated results as a heat map
python ./visualise.py $result_file $result_plot_file

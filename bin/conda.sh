source bin/utils.sh

condaEnv=$(echo $CONDA_DEFAULT_ENV)
if [ ! -z $condaEnv ]; then
    print "conda environment is active"
    conda deactivate
    print "conda environment deactivated"
fi

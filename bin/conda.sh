condaEnv=$(echo $CONDA_DEFAULT_ENV)
if [ ! -z $condaEnv ]; then
    echo "conda environment is active"
    conda deactivate
    echo "conda environment deactivated"
fi

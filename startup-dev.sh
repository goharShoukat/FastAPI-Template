source bin/conda.sh
./bin/install_brew.sh
./bin/install_pipx.sh
./bin/install_poetry.sh

cd app
poetry run start

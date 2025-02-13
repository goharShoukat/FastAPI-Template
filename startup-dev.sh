source bin/conda.sh
source bin/cleanup.sh

./bin/install_brew.sh
./bin/install_pip.sh
./bin/install_pipx.sh
./bin/install_poetry.sh

trap cleanup EXIT

(
    cd app
    poetry run start
)

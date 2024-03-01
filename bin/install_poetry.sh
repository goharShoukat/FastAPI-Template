# check and install poetry
if ! command -v poetry &>/dev/null; then
    echo "poetry is not installed"
    pipx install poetry
    echo "poetry is installed"
    export PATH=~/.local/bin:$PATH
fi

if [ -f poetry.lock ]; then
    echo 'Lock file found. Skipping installation'
else
    echo 'Lock file not found. Installing packages'
    poetry install
    echo "packages installed"
fi

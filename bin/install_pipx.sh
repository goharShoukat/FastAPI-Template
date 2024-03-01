command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# check and install pipx
if ! command -v pipx &>/dev/null; then
    echo "Installing pipx"
    brew install pipx
    echo "pipx installed"
fi

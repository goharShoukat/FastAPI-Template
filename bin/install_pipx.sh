source utils.sh

# check and install pipx
if ! command_exists pipx; then
    print "Installing pipx"
    brew install pipx
    print "pipx installed"
fi

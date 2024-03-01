source bin/utils.sh

# check and install poetry
if ! command -v poetry &>/dev/null; then
    print "poetry is not installed"
    pipx install poetry
    print "poetry is installed"
    export PATH=~/.local/bin:$PATH
fi

if [ -f poetry.lock ]; then
    print 'Lock file found. Skipping installation'
else
    print 'Lock file not found. Installing packages'
    poetry install
    print "packages installed"
fi

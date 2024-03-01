source bin/utils.sh
source bin/os_detection.sh

os=$(get_os)

# check os and install pipx
if ! command_exists pipx; then
    print "Installing pipx"
    if [ $os=='OSX' ]; then
        brew install pipx
    elif [ $os=='WINDOWS' ]; then
        pip install pipx
        python3 -m pipx ensurepath
        print "There is a possibility that pipx is still not added to the environment variables."
        print "If that is the case, you'll have to manually add it to the environment variables"
        print "This script only handles installing pipx to your machine"
    fi
    print "pipx installed"
fi

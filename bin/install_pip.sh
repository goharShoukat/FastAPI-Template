# source bin/utils.sh
source utils.sh
if ! command_exists python3 -m ensurepip --default-pi; then
    print "pip is not installed"
    print "Please download pip by downloading Python from python.org"
    print "Re-run the server after reinstalling python"
    print "If this still doesn't resolve your errors, please reach out to Gohar Shoukat"
fi

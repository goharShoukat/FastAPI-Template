source utils.sh

# check if brew is installed
if ! command -v brew &>/dev/null; then
    pretty_print "Installing Homebrew, an OSX package manager, follow the instructions..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    if ! grep -qs "recommended by brew doctor" ~/.zshrc; then
        print "Put Homebrew location earlier in PATH ..."
        printf '\n# recommended by brew doctor\n' >>~/.zshrc
        printf 'export PATH="/usr/local/bin:$PATH"\n' >>~/.zshrc
        export PATH="/usr/local/bin:$PATH"

        print "Updating brew formulas"
        brew update
    fi
else
    print "Found an existing installation of Homebrew"
fi

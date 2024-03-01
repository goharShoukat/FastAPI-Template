command_exists() {
    command -v "$1" >/dev/null 2>&1
}
pretty_print() {
    printf "\n%b\n" "$1"
}

if ! command -v brew &>/dev/null; then
    pretty_print "Installing Homebrew, an OSX package manager, follow the instructions..."
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    if ! grep -qs "recommended by brew doctor" ~/.zshrc; then
        pretty_print "Put Homebrew location earlier in PATH ..."
        printf '\n# recommended by brew doctor\n' >>~/.zshrc
        printf 'export PATH="/usr/local/bin:$PATH"\n' >>~/.zshrc
        export PATH="/usr/local/bin:$PATH"

        pretty_print "Updating brew formulas"
        brew update
    fi
else
    pretty_print "Found an existing installation of Homebrew"
fi

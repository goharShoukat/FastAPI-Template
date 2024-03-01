command_exists() {
    command -v "$1" &>/dev/null
}
print() {
    printf "\n%b\n" "$1"
}

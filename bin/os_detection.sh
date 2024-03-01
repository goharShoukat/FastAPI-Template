get_os() {
    case "$OSTYPE" in
    solaris*) echo "SOLARIS" ;;
    darwin*) echo "OSX" ;;
    linux*) echo "LINUX" ;;
    bsd*) echo "BSD" ;;
    msys*) NDOWS" ;;
    cygwin*LSO WINDOWS" ;;
    *) echo "$OSTYPE" ;;
    esac
}

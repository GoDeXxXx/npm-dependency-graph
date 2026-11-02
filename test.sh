#!/bin/sh
# все тесты: модульные тесты Python, затем сверка реализаций обхода на
# других языках с ожидаемыми выводами из repos/expected
# (перед сверкой нужно собрать реализации: sh build.sh)
cd "$(dirname "$0")" || exit 1

python3 -m unittest discover -s python -p "test_*.py" -v || exit 1

failed=0

# $1 - название реализации, остальное - команда ее запуска
check() {
    label=$1
    shift
    count=0
    bad=0
    while read -r file package depth filter mode expected; do
        case "$file" in
            "" | "#"*) continue ;;
        esac
        count=$((count + 1))
        if ! "$@" "repos/$file" "$package" "$depth" "$filter" "$mode" 2>&1 |
            cmp -s - "repos/expected/$expected"; then
            echo "  $label: не совпал вывод для $file $package $depth $filter $mode"
            bad=$((bad + 1))
        fi
    done < repos/cases.txt
    for file in repos/errors/*.txt; do
        if "$@" "$file" A 10 - forward > /dev/null 2>&1; then
            echo "  $label: нет ошибки для $file"
            bad=$((bad + 1))
        fi
    done
    if [ "$bad" -eq 0 ]; then
        echo "$label: совпали все $count случаев, ошибки в файлах найдены"
    else
        echo "$label: расхождений $bad"
        failed=1
    fi
}

# $1 - название, $2 - файл, который должен существовать, $3 - нужная команда
ready() {
    if ! command -v "$3" > /dev/null; then
        echo "$1: команда $3 не найдена, пропущено"
        return 1
    fi
    if [ ! -e "$2" ]; then
        echo "$1: нет $2, сначала выполните sh build.sh"
        return 1
    fi
    return 0
}

echo
echo "Сверка реализаций обхода с repos/expected:"
ready JavaScript javascript/deps.js node && check JavaScript node javascript/deps.js
ready Java java/out/deps.class java && check Java java -cp java/out deps
ready Kotlin kotlin/deps.jar java && check Kotlin java -jar kotlin/deps.jar
ready "C#" csharp/bin/deps.dll dotnet && check "C#" dotnet csharp/bin/deps.dll
ready Go go/deps go && check Go go/deps
ready Rust rust/deps rustc && check Rust rust/deps
exit $failed

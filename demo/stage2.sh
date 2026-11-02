#!/bin/sh
# этап 2: прямые зависимости пакета из реестра npm (нужен интернет)
cd "$(dirname "$0")/.." || exit 1

run() {
    printf '\n$ ./start.sh'
    printf ' %s' "$@"
    printf '\n'
    ./start.sh "$@"
    printf '(код возврата %s)\n' "$?"
}

echo "== прямые зависимости из https://registry.npmjs.org"
run --package express
run --package axios
run --package @babel/core
echo
echo "== пакет без зависимостей"
run --package ms
echo
echo "== другой репозиторий с тем же форматом npm (зеркало)"
run --package axios --repo https://registry.npmmirror.com
echo
echo "== ошибки"
run --package no-such-package-for-lab-work-15
run --package express --repo https://registry.npmjs.invalid
run --package express --repo https://example.com
run --package A --repo repos/simple.txt --test-mode

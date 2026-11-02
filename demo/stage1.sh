#!/bin/sh
# этап 1: вывод параметров и обработка ошибок во всех параметрах
cd "$(dirname "$0")/.." || exit 1

run() {
    printf '\n$ ./start.sh'
    printf ' %s' "$@"
    printf '\n'
    ./start.sh "$@"
    printf '(код возврата %s)\n' "$?"
}

echo "== параметры по умолчанию"
run --package express
echo
echo "== все параметры заданы"
run --package lodash --repo http://localhost:4873 --output deps.png --ascii-tree --max-depth 3 --filter test
echo
echo "== тестовый режим"
run --package A --repo repos/simple.txt --test-mode

echo
echo "== ошибки: имя пакета"
run
run --package Express
run --package a --repo repos/simple.txt --test-mode
echo
echo "== ошибки: репозиторий"
run --package express --repo registry.npmjs.org
run --package express --repo ftp://registry.npmjs.org
run --package express --repo repos/simple.txt
run --package A --repo repos/missing.txt --test-mode
echo
echo "== ошибки: режим работы с тестовым репозиторием"
run --package A --test-mode
run --package A --repo repos/simple.txt --test-mode=yes
echo
echo "== ошибки: файл с изображением"
run --package express --output graph.jpg
run --package express --output missing/graph.png
run --package express --output ""
echo
echo "== ошибки: режим ASCII-дерева"
run --package express --ascii-tree=yes
echo
echo "== ошибки: глубина анализа"
run --package express --max-depth abc
run --package express --max-depth 0
run --package express --max-depth 1000
echo
echo "== ошибки: подстрока для фильтрации"
run --package express --filter " "
run --package express --filter press
echo
echo "== неизвестный параметр"
run --package express --verbose

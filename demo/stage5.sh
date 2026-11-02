#!/bin/sh
# этап 5: текст PlantUML, картинка PNG и ASCII-дерево
# (для PNG нужна Java, для пакетов npm нужен интернет)
cd "$(dirname "$0")/.." || exit 1
OUT=$(mktemp -d)
echo "Картинки сохраняются в $OUT"

run() {
    printf '\n$ ./start.sh'
    printf ' %s' "$@"
    printf '\n'
    ./start.sh "$@"
    printf '(код возврата %s)\n' "$?"
}

echo
echo "== тестовый репозиторий: ASCII-дерево, циклы и повторы"
run --package A --repo repos/complex.txt --test-mode --max-depth 10 --ascii-tree --output "$OUT/complex.png"
echo
echo "Текст PlantUML:"
cat "$OUT/complex.puml"
echo
echo "== без --ascii-tree граф выводится списком"
run --package A --repo repos/cycle.txt --test-mode --output "$OUT/cycle.png"
echo
echo "== обратные зависимости в виде дерева"
run --package K --repo repos/complex.txt --test-mode --reverse --ascii-tree --output "$OUT/reverse.png"
echo
echo "== три пакета из реестра npm"
run --package express --max-depth 10 --ascii-tree --output "$OUT/express.png"
run --package axios --max-depth 10 --ascii-tree --output "$OUT/axios.png"
run --package yargs --max-depth 10 --ascii-tree --output "$OUT/yargs.png"
echo
echo "== ошибки"
run --package A --repo repos/simple.txt --test-mode --output "$OUT/missing/graph.png"
run --package A --repo repos/simple.txt --test-mode --output "$OUT/graph.svg"
echo
ls -l "$OUT"

#!/bin/sh
# этап 4: обратные зависимости (кто зависит от пакета) на тестовых
# репозиториях, тем же обходом в ширину
cd "$(dirname "$0")/.." || exit 1

run() {
    printf '\n$'
    printf ' %s' "$@"
    printf '\n'
    "$@"
    printf '(код возврата %s)\n' "$?"
}

echo "== общая зависимость: от D зависят B и C, от них A"
cat repos/simple.txt
run ./start.sh --package D --repo repos/simple.txt --test-mode --reverse
run ./start.sh --package D --repo repos/simple.txt --test-mode --reverse --max-depth 1
echo
echo "== цепочка и глубина"
run ./start.sh --package F --repo repos/chain.txt --test-mode --reverse --max-depth 10
run ./start.sh --package F --repo repos/chain.txt --test-mode --reverse --max-depth 2
echo
echo "== циклы"
run ./start.sh --package D --repo repos/cycle.txt --test-mode --reverse
run ./start.sh --package B --repo repos/self.txt --test-mode --reverse
echo
echo "== фильтр"
run ./start.sh --package E --repo repos/filter.txt --test-mode --reverse
run ./start.sh --package E --repo repos/filter.txt --test-mode --reverse --filter X
echo
echo "== граф с несколькими циклами"
cat repos/complex.txt
run ./start.sh --package K --repo repos/complex.txt --test-mode --reverse --max-depth 10
run ./start.sh --package E --repo repos/complex.txt --test-mode --reverse --max-depth 2
run ./start.sh --package Q --repo repos/complex.txt --test-mode --reverse --filter H
echo
echo "== ошибки"
run ./start.sh --package express --reverse
run ./start.sh --package Z --repo repos/complex.txt --test-mode --reverse
echo
echo "== тот же обход в реализациях на других языках (нужна сборка: sh build.sh)"
run node javascript/deps.js repos/complex.txt K 10 - reverse
run java -cp java/out deps repos/complex.txt K 10 - reverse
run java -jar kotlin/deps.jar repos/complex.txt K 10 - reverse
run dotnet csharp/bin/deps.dll repos/complex.txt K 10 - reverse
run go/deps repos/complex.txt K 10 - reverse
run rust/deps repos/complex.txt K 10 - reverse

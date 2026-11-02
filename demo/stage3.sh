#!/bin/sh
# этап 3: граф зависимостей (BFS без рекурсии), глубина, фильтр, циклы,
# режим тестового репозитория
cd "$(dirname "$0")/.." || exit 1

run() {
    printf '\n$ ./start.sh'
    printf ' %s' "$@"
    printf '\n'
    ./start.sh "$@"
    printf '(код возврата %s)\n' "$?"
}

echo "== тестовый репозиторий: общие зависимости"
cat repos/simple.txt
run --package A --repo repos/simple.txt --test-mode
echo
echo "== глубина анализа"
cat repos/chain.txt
run --package A --repo repos/chain.txt --test-mode --max-depth 3
run --package A --repo repos/chain.txt --test-mode --max-depth 10
run --package C --repo repos/chain.txt --test-mode
echo
echo "== циклические зависимости"
cat repos/cycle.txt
run --package A --repo repos/cycle.txt --test-mode
run --package C --repo repos/cycle.txt --test-mode --max-depth 2
cat repos/self.txt
run --package A --repo repos/self.txt --test-mode
echo
echo "== фильтр по подстроке"
cat repos/filter.txt
run --package A --repo repos/filter.txt --test-mode
run --package A --repo repos/filter.txt --test-mode --filter X
echo
echo "== граф с несколькими циклами"
cat repos/complex.txt
run --package A --repo repos/complex.txt --test-mode --max-depth 10
run --package A --repo repos/complex.txt --test-mode --max-depth 2
run --package A --repo repos/complex.txt --test-mode --filter K
run --package G --repo repos/complex.txt --test-mode
echo
echo "== ошибки в тестовом репозитории"
for file in repos/errors/*.txt; do
    run --package A --repo "$file" --test-mode
done
run --package Z --repo repos/simple.txt --test-mode
echo
echo "== настоящий репозиторий npm (нужен интернет)"
run --package axios --max-depth 2
run --package express --max-depth 2 --filter type

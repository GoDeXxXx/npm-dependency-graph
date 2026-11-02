package main

import (
	"fmt"
	"io"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const ARGS_COUNT = 5

var name_pattern = regexp.MustCompile(`^[A-Z]+$`)

// обход графа тестового репозитория в ширину без рекурсии
// file_path - файл с описанием графа, start_name - анализируемый пакет,
// max_depth - глубина, filter_text - подстрока для пропуска пакетов,
// reverse_mode - искать обратные зависимости,
// comment_char и separator - символы комментария и двоеточия в файле,
// out и err_out - потоки для вывода
func Run_Bfs(file_path string, start_name string, max_depth int, filter_text string, reverse_mode bool, comment_char string, separator string, out io.Writer, err_out io.Writer) int {
	data, err := os.ReadFile(file_path)
	if err != nil {
		fmt.Fprintln(err_out, "Ошибка: не удалось прочитать файл "+file_path)
		return 1
	}
	lines := strings.Split(string(data), "\n")
	// слишком большие файлы не читаем
	if len(lines) > 100000 {
		fmt.Fprintln(err_out, "Ошибка: слишком большой файл "+file_path)
		return 1
	}
	// разбор строк вида "A: B C", порядок пакетов храним отдельно
	repo := map[string][]string{}
	names := []string{}
	for i, line := range lines {
		comment_pos := strings.Index(line, comment_char)
		if comment_pos >= 0 {
			line = line[:comment_pos]
		}
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		where := file_path + ", строка " + strconv.Itoa(i+1)
		colon_pos := strings.Index(line, separator)
		if colon_pos < 0 {
			fmt.Fprintln(err_out, "Ошибка: "+where+": нет двоеточия после имени пакета")
			return 1
		}
		package_name := strings.TrimSpace(line[:colon_pos])
		deps := strings.Fields(line[colon_pos+1:])
		for _, item := range append([]string{package_name}, deps...) {
			if !name_pattern.MatchString(item) {
				fmt.Fprintln(err_out, "Ошибка: "+where+": имя пакета '"+item+"' должно состоять из больших латинских букв")
				return 1
			}
		}
		if _, found := repo[package_name]; found {
			fmt.Fprintln(err_out, "Ошибка: "+where+": пакет "+package_name+" описан повторно")
			return 1
		}
		seen := map[string]bool{}
		for _, dep := range deps {
			if seen[dep] {
				fmt.Fprintln(err_out, "Ошибка: "+where+": у пакета "+package_name+" повторяется зависимость")
				return 1
			}
			seen[dep] = true
		}
		repo[package_name] = deps
		names = append(names, package_name)
	}
	if len(names) == 0 {
		fmt.Fprintln(err_out, "Ошибка: в файле "+file_path+" нет ни одного пакета")
		return 1
	}
	// все зависимости должны быть описаны в файле
	for _, package_name := range names {
		for _, dep := range repo[package_name] {
			if _, found := repo[dep]; !found {
				fmt.Fprintln(err_out, "Ошибка: пакет "+dep+", от которого зависит "+package_name+", не описан в файле "+file_path)
				return 1
			}
		}
	}
	if _, found := repo[start_name]; !found {
		fmt.Fprintln(err_out, "Ошибка: пакет "+start_name+" не описан в файле "+file_path)
		return 1
	}
	// для обратных зависимостей разворачиваем все ребра
	graph := repo
	if reverse_mode {
		graph = map[string][]string{}
		for _, package_name := range names {
			graph[package_name] = []string{}
		}
		for _, package_name := range names {
			for _, dep := range repo[package_name] {
				graph[dep] = append(graph[dep], package_name)
			}
		}
	}
	// обход в ширину: очередь и глубина каждого пакета
	depth := map[string]int{start_name: 0}
	queue := []string{start_name}
	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]
		if depth[current] >= max_depth {
			continue
		}
		result := []string{}
		for _, dep := range graph[current] {
			if filter_text != "" && strings.Contains(dep, filter_text) {
				continue
			}
			result = append(result, dep)
			if _, found := depth[dep]; !found {
				depth[dep] = depth[current] + 1
				queue = append(queue, dep)
			}
		}
		fmt.Fprint(out, strings.TrimRight(current+": "+strings.Join(result, " "), " ")+"\n")
	}
	return 0
}

// разбор аргументов командной строки и запуск обхода
func main() {
	args := os.Args[1:]
	if len(args) != ARGS_COUNT {
		fmt.Fprintln(os.Stderr, "Использование: go/deps <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>")
		os.Exit(1)
	}
	max_depth, err := strconv.Atoi(args[2])
	if err != nil || max_depth < 1 || max_depth > 100 {
		fmt.Fprintln(os.Stderr, "Ошибка: глубина анализа должна быть целым числом от 1 до 100")
		os.Exit(1)
	}
	if args[4] != "forward" && args[4] != "reverse" {
		fmt.Fprintln(os.Stderr, "Ошибка: направление должно быть forward или reverse")
		os.Exit(1)
	}
	filter_text := args[3]
	if filter_text == "-" {
		filter_text = ""
	}
	if filter_text != "" && strings.Contains(args[1], filter_text) {
		fmt.Fprintln(os.Stderr, "Ошибка: анализируемый пакет "+args[1]+" сам содержит подстроку "+filter_text)
		os.Exit(1)
	}
	os.Exit(Run_Bfs(args[0], args[1], max_depth, filter_text, args[4] == "reverse", "#", ":", os.Stdout, os.Stderr))
}

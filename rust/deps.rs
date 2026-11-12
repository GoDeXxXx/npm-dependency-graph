use std::collections::{HashMap, HashSet, VecDeque};
use std::env;
use std::fs;
use std::io::{self, Write};
use std::process;

pub const args_count: usize = 5;

// проверка имени пакета: только большие латинские буквы
pub fn IsValidName(name: &str) -> bool {
    !name.is_empty() && name.chars().all(|c| c.is_ascii_uppercase())
}

// обход графа тестового репозитория в ширину без рекурсии
// filePath - файл с описанием графа, startName - анализируемый пакет,
// maxDepth - глубина, filterText - подстрока для пропуска пакетов,
// reverseMode - искать обратные зависимости,
// commentChar и separator - символы комментария и двоеточия в файле,
// out и err - потоки для вывода
pub fn RunBfs(filePath: &str, startName: &str, maxDepth: usize, filterText: &str, reverseMode: bool, commentChar: char, separator: char, out: &mut dyn Write, err: &mut dyn Write) -> i32 {
    let text = match fs::read_to_string(filePath) {
        Ok(text) => text,
        Err(_) => {
            let _ = writeln!(err, "Ошибка: не удалось прочитать файл {}", filePath);
            return 1;
        }
    };
    // метку порядка байтов (BOM) в начале файла пропускаем
    let text = text.trim_start_matches('\u{feff}').to_string();
    let lines: Vec<&str> = text.lines().collect();
    // слишком большие файлы не читаем
    if lines.len() > 100000 {
        let _ = writeln!(err, "Ошибка: слишком большой файл {}", filePath);
        return 1;
    }
    // разбор строк вида "A: B C", порядок пакетов храним отдельно
    let mut repo: HashMap<String, Vec<String>> = HashMap::new();
    let mut names: Vec<String> = Vec::new();
    for (index, rawLine) in lines.iter().enumerate() {
        let mut line: &str = rawLine;
        if let Some(commentPos) = line.find(commentChar) {
            line = &line[..commentPos];
        }
        let line = line.trim();
        if line.is_empty() {
            continue;
        }
        let place = format!("{}, строка {}", filePath, index + 1);
        let colonPos = match line.find(separator) {
            Some(position) => position,
            None => {
                let _ = writeln!(err, "Ошибка: {}: нет двоеточия после имени пакета", place);
                return 1;
            }
        };
        let packageName = line[..colonPos].trim().to_string();
        let deps: Vec<String> = line[colonPos + 1..].split_whitespace().map(|item| item.to_string()).collect();
        let mut allNames = vec![packageName.clone()];
        allNames.extend(deps.iter().cloned());
        for item in &allNames {
            if !IsValidName(item) {
                let _ = writeln!(err, "Ошибка: {}: имя пакета '{}' должно состоять из больших латинских букв", place, item);
                return 1;
            }
        }
        if repo.contains_key(&packageName) {
            let _ = writeln!(err, "Ошибка: {}: пакет {} описан повторно", place, packageName);
            return 1;
        }
        let unique: HashSet<&String> = deps.iter().collect();
        if unique.len() != deps.len() {
            let _ = writeln!(err, "Ошибка: {}: у пакета {} повторяется зависимость", place, packageName);
            return 1;
        }
        repo.insert(packageName.clone(), deps);
        names.push(packageName);
    }
    if names.is_empty() {
        let _ = writeln!(err, "Ошибка: в файле {} нет ни одного пакета", filePath);
        return 1;
    }
    // все зависимости должны быть описаны в файле
    for packageName in &names {
        for dep in &repo[packageName] {
            if !repo.contains_key(dep) {
                let _ = writeln!(err, "Ошибка: пакет {}, от которого зависит {}, не описан в файле {}", dep, packageName, filePath);
                return 1;
            }
        }
    }
    if !repo.contains_key(startName) {
        let _ = writeln!(err, "Ошибка: пакет {} не описан в файле {}", startName, filePath);
        return 1;
    }
    // для обратных зависимостей разворачиваем все ребра
    let mut graph: HashMap<String, Vec<String>> = HashMap::new();
    if reverseMode {
        for packageName in &names {
            graph.insert(packageName.clone(), Vec::new());
        }
        for packageName in &names {
            for dep in &repo[packageName] {
                graph.get_mut(dep).unwrap().push(packageName.clone());
            }
        }
    } else {
        graph = repo.clone();
    }
    // обход в ширину: очередь и глубина каждого пакета
    let mut depth: HashMap<String, usize> = HashMap::new();
    depth.insert(startName.to_string(), 0);
    let mut queue: VecDeque<String> = VecDeque::new();
    queue.push_back(startName.to_string());
    while let Some(current) = queue.pop_front() {
        let currentDepth = depth[&current];
        if currentDepth >= maxDepth {
            continue;
        }
        let mut result: Vec<String> = Vec::new();
        for dep in &graph[&current] {
            if !filterText.is_empty() && dep.contains(filterText) {
                continue;
            }
            result.push(dep.clone());
            if !depth.contains_key(dep) {
                depth.insert(dep.clone(), currentDepth + 1);
                queue.push_back(dep.clone());
            }
        }
        let _ = writeln!(out, "{}", format!("{}: {}", current, result.join(" ")).trim_end());
    }
    let _ = out.flush();
    0
}

// разбор аргументов командной строки и запуск обхода
fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    if args.len() != args_count {
        eprintln!("Использование: rust/deps <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>");
        process::exit(1);
    }
    let maxDepth: usize = args[2].parse().unwrap_or(0);
    if maxDepth < 1 || maxDepth > 100 {
        eprintln!("Ошибка: глубина анализа должна быть целым числом от 1 до 100");
        process::exit(1);
    }
    if args[4] != "forward" && args[4] != "reverse" {
        eprintln!("Ошибка: направление должно быть forward или reverse");
        process::exit(1);
    }
    let filterText: &str = if args[3] == "-" { "" } else { &args[3] };
    if !filterText.is_empty() && args[1].contains(filterText) {
        eprintln!("Ошибка: анализируемый пакет {} сам содержит подстроку {}", args[1], filterText);
        process::exit(1);
    }
    let code = RunBfs(&args[0], &args[1], maxDepth, filterText, args[4] == "reverse", '#', ':', &mut io::stdout(), &mut io::stderr());
    process::exit(code);
}

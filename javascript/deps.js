'use strict';

const fs = require('fs');

const args_count = 5;
const name_pattern = /^[A-Z]+$/;

// обход графа тестового репозитория в ширину без рекурсии
// file_path - файл с описанием графа, start_name - анализируемый пакет,
// max_depth - глубина, filter_text - подстрока для пропуска пакетов,
// reverse_mode - искать обратные зависимости,
// comment_char и separator - символы комментария и двоеточия в файле,
// out и err - потоки для вывода
function run_bfs(file_path, start_name, max_depth, filter_text, reverse_mode, comment_char, separator, out, err) {
  let text;
  try {
    text = fs.readFileSync(file_path, 'utf8');
  } catch (error) {
    err.write('Ошибка: не удалось прочитать файл ' + file_path + '\n');
    return 1;
  }
  // метку порядка байтов (BOM) в начале файла пропускаем
  if (text.charCodeAt(0) === 0xfeff) {
    text = text.substring(1);
  }
  const lines = text.split('\n');
  // слишком большие файлы не читаем
  if (lines.length > 100000) {
    err.write('Ошибка: слишком большой файл ' + file_path + '\n');
    return 1;
  }
  // разбор строк вида "A: B C"
  const repo = new Map();
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i];
    const comment_pos = line.indexOf(comment_char);
    if (comment_pos >= 0) {
      line = line.substring(0, comment_pos);
    }
    line = line.trim();
    if (line === '') {
      continue;
    }
    const where = file_path + ', строка ' + (i + 1);
    const colon_pos = line.indexOf(separator);
    if (colon_pos < 0) {
      err.write('Ошибка: ' + where + ': нет двоеточия после имени пакета\n');
      return 1;
    }
    const package_name = line.substring(0, colon_pos).trim();
    const deps = line.substring(colon_pos + 1).split(/\s+/).filter((item) => item !== '');
    for (const item of [package_name].concat(deps)) {
      if (!name_pattern.test(item)) {
        err.write('Ошибка: ' + where + ": имя пакета '" + item + "' должно состоять из больших латинских букв\n");
        return 1;
      }
    }
    if (repo.has(package_name)) {
      err.write('Ошибка: ' + where + ': пакет ' + package_name + ' описан повторно\n');
      return 1;
    }
    if (new Set(deps).size !== deps.length) {
      err.write('Ошибка: ' + where + ': у пакета ' + package_name + ' повторяется зависимость\n');
      return 1;
    }
    repo.set(package_name, deps);
  }
  if (repo.size === 0) {
    err.write('Ошибка: в файле ' + file_path + ' нет ни одного пакета\n');
    return 1;
  }
  // все зависимости должны быть описаны в файле
  for (const [package_name, deps] of repo) {
    for (const dep of deps) {
      if (!repo.has(dep)) {
        err.write('Ошибка: пакет ' + dep + ', от которого зависит ' + package_name + ', не описан в файле ' + file_path + '\n');
        return 1;
      }
    }
  }
  if (!repo.has(start_name)) {
    err.write('Ошибка: пакет ' + start_name + ' не описан в файле ' + file_path + '\n');
    return 1;
  }
  // для обратных зависимостей разворачиваем все ребра
  let graph = repo;
  if (reverse_mode) {
    graph = new Map();
    for (const package_name of repo.keys()) {
      graph.set(package_name, []);
    }
    for (const [package_name, deps] of repo) {
      for (const dep of deps) {
        graph.get(dep).push(package_name);
      }
    }
  }
  // обход в ширину: очередь и глубина каждого пакета
  const depth = new Map([[start_name, 0]]);
  const queue = [start_name];
  let head = 0;
  while (head < queue.length) {
    const current = queue[head];
    head += 1;
    if (depth.get(current) >= max_depth) {
      continue;
    }
    const result = [];
    for (const dep of graph.get(current)) {
      if (filter_text !== '' && dep.includes(filter_text)) {
        continue;
      }
      result.push(dep);
      if (!depth.has(dep)) {
        depth.set(dep, depth.get(current) + 1);
        queue.push(dep);
      }
    }
    out.write((current + ': ' + result.join(' ')).trimEnd() + '\n');
  }
  return 0;
}

// разбор аргументов командной строки и запуск обхода
function main(argv) {
  if (argv.length !== args_count) {
    process.stderr.write('Использование: node deps.js <файл репозитория> <пакет> <глубина> <фильтр или -> <forward или reverse>\n');
    return 1;
  }
  const max_depth = Number(argv[2]);
  if (!Number.isInteger(max_depth) || max_depth < 1 || max_depth > 100) {
    process.stderr.write('Ошибка: глубина анализа должна быть целым числом от 1 до 100\n');
    return 1;
  }
  if (argv[4] !== 'forward' && argv[4] !== 'reverse') {
    process.stderr.write('Ошибка: направление должно быть forward или reverse\n');
    return 1;
  }
  const filter_text = argv[3] === '-' ? '' : argv[3];
  if (filter_text !== '' && argv[1].includes(filter_text)) {
    process.stderr.write('Ошибка: анализируемый пакет ' + argv[1] + ' сам содержит подстроку ' + filter_text + '\n');
    return 1;
  }
  return run_bfs(argv[0], argv[1], max_depth, filter_text, argv[4] === 'reverse', '#', ':', process.stdout, process.stderr);
}

process.exitCode = main(process.argv.slice(2));

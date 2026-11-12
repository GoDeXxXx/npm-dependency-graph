import argparse
import os
import re
import sys
from functools import partial
from urllib.parse import urlparse

from filerepo import RepoFileError, read_repo_file
from graph import bfs, format_graph, reverse_edges
from registry import RegistryError, get_dependencies
from render import RenderError, ascii_tree, save_png, save_text, to_plantuml

DEFAULT_REPO = "https://registry.npmjs.org"
DEFAULT_OUTPUT = "graph.png"
DEFAULT_DEPTH = "5"
NPM_NAME = r"(@[A-Za-z0-9~-][A-Za-z0-9._~-]*/)?[A-Za-z0-9~-][A-Za-z0-9._~-]*"
DIGITS = "[0-9]+"
TEST_NAME = "[A-Z]+"


# ошибка в параметрах командной строки
class option_error(Exception):
    pass


# описание параметров командной строки
def parse_args(argv):
    parser = argparse.ArgumentParser(
        prog="depviz",
        description="Визуализация графа зависимостей npm-пакета")
    parser.add_argument("--package", help="имя анализируемого пакета")
    parser.add_argument("--repo", default=DEFAULT_REPO,
                        help="URL-адрес репозитория или путь к файлу "
                             "тестового репозитория")
    parser.add_argument("--test-mode", action="store_true",
                        help="режим работы с тестовым репозиторием")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="имя файла с изображением графа")
    parser.add_argument("--ascii-tree", action="store_true",
                        help="вывод зависимостей в виде ASCII-дерева")
    parser.add_argument("--max-depth", default=DEFAULT_DEPTH,
                        help="максимальная глубина анализа зависимостей")
    parser.add_argument("--filter",
                        help="подстрока: пакеты с ней в имени не учитываются")
    parser.add_argument("--reverse", action="store_true",
                        help="вывести обратные зависимости (пакеты, которые "
                             "зависят от данного), только в тестовом режиме")
    return parser.parse_args(argv)


# проверка всех параметров, на выходе словарь с настройками
def CheckOptions(packageName, repoPath, testMode, outputFile, asciiTree,
                 maxDepth, filterText, reverseMode):
    # имя пакета
    if not packageName:
        message = "не задано имя пакета (--package)"
        raise option_error(message)
    if testMode:
        # в тестовом репозитории пакеты называются большими латинскими буквами
        if not re.fullmatch(TEST_NAME, packageName):
            message = ("в тестовом репозитории имя пакета состоит "
                       f"из больших латинских букв: {packageName}")
            raise option_error(message)
    else:
        # ограничения npm на имя пакета
        if len(packageName) > 214:
            message = "имя пакета npm длиннее 214 символов"
            raise option_error(message)
        if not re.fullmatch(NPM_NAME, packageName):
            message = f"недопустимое имя пакета npm: {packageName}"
            raise option_error(message)
    # репозиторий: URL-адрес или путь к файлу
    if not repoPath:
        message = "не задан репозиторий (--repo)"
        raise option_error(message)
    if testMode:
        if not os.path.isfile(repoPath):
            message = f"файл тестового репозитория не найден: {repoPath}"
            raise option_error(message)
    else:
        try:
            address = urlparse(repoPath)
        except ValueError as error:
            message = f"неверный URL-адрес репозитория: {repoPath}"
            raise option_error(message) from error
        if address.scheme not in ("http", "https") or not address.netloc:
            message = f"неверный URL-адрес репозитория: {repoPath} (если это путь к файлу тестового репозитория, добавьте --test-mode)"
            raise option_error(message)
    # файл с изображением графа
    if not outputFile:
        message = "не задано имя файла с изображением (--output)"
        raise option_error(message)
    if not outputFile.lower().endswith(".png"):
        message = f"файл с изображением должен иметь расширение .png: {outputFile}"
        raise option_error(message)
    if os.path.isdir(outputFile):
        message = f"{outputFile} является папкой, а не файлом"
        raise option_error(message)
    folder = os.path.dirname(outputFile)
    if folder and not os.path.isdir(folder):
        message = f"папка для файла с изображением не найдена: {folder}"
        raise option_error(message)
    # максимальная глубина анализа
    if not re.fullmatch(DIGITS, maxDepth):
        message = f"глубина анализа должна быть целым положительным числом: {maxDepth}"
        raise option_error(message)
    depthValue = int(maxDepth)
    if depthValue < 1 or depthValue > 100:
        message = f"глубина анализа должна быть от 1 до 100: {maxDepth}"
        raise option_error(message)
    # подстрока для фильтрации пакетов
    if filterText is not None:
        if not filterText.strip():
            message = "подстрока для фильтрации не может быть пустой"
            raise option_error(message)
        if filterText in packageName:
            message = (f"анализируемый пакет {packageName} сам "
                       f"содержит подстроку {filterText}")
            raise option_error(message)
    # обратные зависимости ищутся только в тестовом репозитории
    if reverseMode and not testMode:
        message = "обратные зависимости можно получить только для тестового репозитория (--test-mode): в реестре npm нет списка пакетов, которые зависят от данного"
        raise option_error(message)
    return {
        "package": packageName,
        "repository": repoPath,
        "test_mode": testMode,
        "output": outputFile,
        "ascii_tree": asciiTree,
        "max_depth": depthValue,
        "filter": filterText or "",
        "reverse": reverseMode,
    }


def main(argv):
    args = parse_args(argv)
    try:
        options = CheckOptions(args.package, args.repo, args.test_mode,
                               args.output, args.ascii_tree, args.max_depth,
                               args.filter, args.reverse)
        if options["test_mode"]:
            repo = read_repo_file(options["repository"])
            if options["package"] not in repo:
                raise RepoFileError(f"пакет {options['package']} не описан "
                                    f"в файле {options['repository']}")
            if options["reverse"]:
                repo = reverse_edges(repo)
            get_deps = repo.get
        else:
            get_deps = partial(get_dependencies, options["repository"])
        order, edges = bfs(options["package"], options["max_depth"],
                           options["filter"], get_deps)
        if options["ascii_tree"]:
            print(ascii_tree(options["package"], edges))
        else:
            print(format_graph(order, edges))
        # текст PlantUML сохраняется рядом с картинкой
        text = to_plantuml(order, edges, options["reverse"])
        puml = os.path.splitext(options["output"])[0] + ".puml"
        save_text(text, puml)
        save_png(text, options["output"])
    except (option_error, RegistryError, RepoFileError, RenderError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    print(f"Граф сохранен в {options['output']}, текст PlantUML в {puml}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

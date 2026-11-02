import argparse
import os
import re
import sys
from functools import partial
from urllib.parse import urlparse

from filerepo import RepoFileError, read_repo_file
from graph import bfs, format_graph
from registry import RegistryError, get_dependencies

DEFAULT_REPO = "https://registry.npmjs.org"
DEFAULT_OUTPUT = "graph.png"
DEFAULT_DEPTH = "5"
NPM_NAME = r"(@[a-z0-9~-][a-z0-9._~-]*/)?[a-z0-9~-][a-z0-9._~-]*"
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
    return parser.parse_args(argv)


# проверка всех параметров, на выходе словарь с настройками
def CheckOptions(packageName, repoPath, testMode, outputFile, asciiTree,
                 maxDepth, filterText):
    # имя пакета
    if not packageName:
        raise option_error("не задано имя пакета (--package)")
    if testMode:
        # в тестовом репозитории пакеты называются большими латинскими буквами
        if not re.fullmatch(TEST_NAME, packageName):
            raise option_error("в тестовом репозитории имя пакета состоит "
                               f"из больших латинских букв: {packageName}")
    else:
        # ограничения npm на имя пакета
        if len(packageName) > 214:
            raise option_error("имя пакета npm длиннее 214 символов")
        if not re.fullmatch(NPM_NAME, packageName):
            raise option_error(f"недопустимое имя пакета npm: {packageName}")
    # репозиторий: URL-адрес или путь к файлу
    if not repoPath:
        raise option_error("не задан репозиторий (--repo)")
    if testMode:
        if not os.path.isfile(repoPath):
            raise option_error(f"файл тестового репозитория не найден: {repoPath}")
    else:
        address = urlparse(repoPath)
        if address.scheme not in ("http", "https") or not address.netloc:
            raise option_error(f"неверный URL-адрес репозитория: {repoPath} (если это путь к файлу тестового репозитория, добавьте --test-mode)")
    # файл с изображением графа
    if not outputFile:
        raise option_error("не задано имя файла с изображением (--output)")
    if not outputFile.lower().endswith(".png"):
        raise option_error(f"файл с изображением должен иметь расширение .png: {outputFile}")
    if os.path.isdir(outputFile):
        raise option_error(f"{outputFile} является папкой, а не файлом")
    folder = os.path.dirname(outputFile)
    if folder and not os.path.isdir(folder):
        raise option_error(f"папка для файла с изображением не найдена: {folder}")
    # максимальная глубина анализа
    if not maxDepth.isdigit():
        raise option_error(f"глубина анализа должна быть целым положительным числом: {maxDepth}")
    depthValue = int(maxDepth)
    if depthValue < 1 or depthValue > 100:
        raise option_error(f"глубина анализа должна быть от 1 до 100: {maxDepth}")
    # подстрока для фильтрации пакетов
    if filterText is not None:
        if not filterText.strip():
            raise option_error("подстрока для фильтрации не может быть пустой")
        if filterText in packageName:
            raise option_error(f"анализируемый пакет {packageName} сам "
                               f"содержит подстроку {filterText}")
    return {
        "package": packageName,
        "repository": repoPath,
        "test_mode": testMode,
        "output": outputFile,
        "ascii_tree": asciiTree,
        "max_depth": depthValue,
        "filter": filterText or "",
    }


def main(argv):
    args = parse_args(argv)
    try:
        options = CheckOptions(args.package, args.repo, args.test_mode,
                               args.output, args.ascii_tree, args.max_depth,
                               args.filter)
        if options["test_mode"]:
            repo = read_repo_file(options["repository"])
            if options["package"] not in repo:
                raise RepoFileError(f"пакет {options['package']} не описан "
                                    f"в файле {options['repository']}")
            get_deps = repo.get
        else:
            get_deps = partial(get_dependencies, options["repository"])
        order, edges = bfs(options["package"], options["max_depth"],
                           options["filter"], get_deps)
    except (option_error, RegistryError, RepoFileError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 1
    print(format_graph(order, edges))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

import re

NAME = re.compile("[A-Z]+")


# ошибка в файле тестового репозитория
class RepoFileError(Exception):
    pass


# чтение тестового репозитория: строки вида "A: B C", после # комментарий
def read_repo_file(path):
    try:
        with open(path, encoding="utf-8-sig") as file:
            lines = file.read().splitlines()
    except (OSError, UnicodeDecodeError) as error:
        raise RepoFileError(f"не удалось прочитать файл {path}") from error
    repo = {}
    for number, line in enumerate(lines, 1):
        text = line.split("#")[0].strip()
        if not text:
            continue
        where = f"{path}, строка {number}"
        name, colon, rest = text.partition(":")
        name = name.strip()
        deps = rest.split()
        if not colon:
            raise RepoFileError(f"{where}: нет двоеточия после имени пакета")
        for item in [name] + deps:
            if not NAME.fullmatch(item):
                raise RepoFileError(f"{where}: имя пакета '{item}' должно "
                                    "состоять из больших латинских букв")
        if name in repo:
            raise RepoFileError(f"{where}: пакет {name} описан повторно")
        if len(set(deps)) != len(deps):
            raise RepoFileError(f"{where}: у пакета {name} повторяется "
                                "зависимость")
        repo[name] = deps
    if not repo:
        raise RepoFileError(f"в файле {path} нет ни одного пакета")
    for name, deps in repo.items():
        for dep in deps:
            if dep not in repo:
                raise RepoFileError(f"пакет {dep}, от которого зависит "
                                    f"{name}, не описан в файле {path}")
    return repo

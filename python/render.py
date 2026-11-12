import os
import subprocess
from collections import deque

PLANTUML_JAR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "plantuml", "plantuml.jar")
PLANTUML_TIMEOUT = 300


# ошибка при сохранении графа
class RenderError(Exception):
    pass


# текст графа на языке PlantUML. Стрелка X --> Y значит "X зависит от Y",
# поэтому для обратных зависимостей стрелки разворачиваются
def to_plantuml(order, edges, reverse=False):
    ids = {}
    lines = ["@startuml", "!pragma layout smetana"]
    for name in order:
        for item in [name] + edges[name]:
            if item not in ids:
                ids[item] = f"p{len(ids)}"
                lines.append(f'rectangle "{item}" as {ids[item]}')
    for name in order:
        for dep in edges[name]:
            if reverse:
                lines.append(f"{ids[dep]} --> {ids[name]}")
            else:
                lines.append(f"{ids[name]} --> {ids[dep]}")
    lines.append("@enduml")
    return "\n".join(lines) + "\n"


# запись текста PlantUML в файл
def save_text(text, path):
    try:
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
    except OSError as error:
        raise RenderError(f"не удалось записать файл {path}") from error


# рисование PNG программой PlantUML (нужна Java 11+), раскладка smetana
# встроена в PlantUML, поэтому Graphviz не нужен. Java запускается в фоновом
# режиме (headless), без значка в доке и окон
def save_png(text, path):
    command = ["java", "-Djava.awt.headless=true", "-DPLANTUML_LIMIT_SIZE=16384",
               "-jar", PLANTUML_JAR, "-tpng", "-charset", "UTF-8", "-pipe"]
    try:
        result = subprocess.run(command, input=text.encode("utf-8"),
                                capture_output=True, check=False,
                                timeout=PLANTUML_TIMEOUT)
    except FileNotFoundError as error:
        raise RenderError("для рисования PNG нужна Java: "
                          "команда java не найдена") from error
    except subprocess.TimeoutExpired as error:
        raise RenderError("PlantUML не успел нарисовать граф") from error
    if result.returncode != 0 or not result.stdout.startswith(b"\x89PNG"):
        message = result.stderr.decode("utf-8", "replace").strip()
        raise RenderError(f"PlantUML не смог нарисовать граф: {message}")
    try:
        with open(path, "wb") as file:
            file.write(result.stdout)
    except OSError as error:
        raise RenderError(f"не удалось записать файл {path}") from error


# дочерние пакеты для стека: последний ребенок кладется первым,
# чтобы снимался со стека последним
def stack_items(edges, name, prefix, path):
    children = edges.get(name, [])
    items = []
    for index, child in enumerate(children):
        items.append((child, prefix, index == len(children) - 1, path))
    items.reverse()
    return items


# родитель каждого пакета в дереве: пакет, из которого обход в ширину
# пришел в него первым. Тогда уровень пакета в дереве равен его глубине
def tree_parents(root, edges):
    parent = {root: None}
    queue = deque([root])
    while queue:
        name = queue.popleft()
        for dep in edges.get(name, []):
            if dep not in parent:
                parent[dep] = name
                queue.append(dep)
    return parent


# зависимости в виде ASCII-дерева, обход в глубину на стеке без рекурсии.
# Пакет раскрывается один раз, под своим родителем из tree_parents, поэтому
# дерево не глубже --max-depth. В других местах пакет со своими
# зависимостями помечается (повтор), пакет из числа предков - (цикл)
def ascii_tree(root, edges):
    parent = tree_parents(root, edges)
    lines = [root]
    stack = stack_items(edges, root, "", (root,))
    while stack:
        name, prefix, last, path = stack.pop()
        branch = "`-- " if last else "|-- "
        if name in path:
            lines.append(prefix + branch + name + " (цикл)")
            continue
        if parent[name] != path[-1]:
            mark = " (повтор)" if edges.get(name) else ""
            lines.append(prefix + branch + name + mark)
            continue
        lines.append(prefix + branch + name)
        child_prefix = prefix + ("    " if last else "|   ")
        stack.extend(stack_items(edges, name, child_prefix, path + (name,)))
    return "\n".join(lines)

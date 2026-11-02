from collections import deque


# обход графа зависимостей в ширину без рекурсии.
# get_deps(name) возвращает прямые зависимости пакета.
# Пакеты на глубине max_depth не раскрываются, пакеты с подстрокой skip
# в имени не учитываются. Каждый пакет попадает в очередь один раз,
# поэтому циклы не приводят к зацикливанию.
def bfs(root, max_depth, skip, get_deps):
    depth = {root: 0}
    order = []
    edges = {}
    queue = deque([root])
    while queue:
        name = queue.popleft()
        if depth[name] >= max_depth:
            continue
        order.append(name)
        edges[name] = []
        for dep in get_deps(name):
            if skip and skip in dep:
                continue
            edges[name].append(dep)
            if dep not in depth:
                depth[dep] = depth[name] + 1
                queue.append(dep)
    return order, edges


# граф в виде строк "пакет: зависимости" в порядке обхода
def format_graph(order, edges):
    lines = [f"{name}: {' '.join(edges[name])}".rstrip() for name in order]
    return "\n".join(lines)


# обратные зависимости: для каждого пакета список пакетов, которые от него
# зависят, в порядке их описания в репозитории
def reverse_edges(repo):
    result = {name: [] for name in repo}
    for name, deps in repo.items():
        for dep in deps:
            result[dep].append(name)
    return result

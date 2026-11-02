import os
import unittest
from contextlib import redirect_stderr, redirect_stdout
from functools import partial
from io import StringIO

from depviz import main
from filerepo import read_repo_file
from graph import bfs, format_graph, reverse_edges
from registry import get_dependencies
from registry_snapshot import SNAPSHOT
from test_registry import start_registry

REPOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "repos")


# чтение списка случаев repos/cases.txt
def read_cases():
    cases = []
    with open(os.path.join(REPOS, "cases.txt"), encoding="utf-8") as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                cases.append(line.split())
    return cases


# граф по тестовому репозиторию в виде текста
def run_bfs(repo, root, depth, skip=""):
    order, edges = bfs(root, depth, skip, repo.get)
    return format_graph(order, edges)


class BfsTest(unittest.TestCase):

    def test_simple(self):
        repo = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        order, edges = bfs("A", 5, "", repo.get)
        self.assertEqual(order, ["A", "B", "C", "D"])
        self.assertEqual(edges["C"], ["D"])

    def test_depth(self):
        repo = {"A": ["B"], "B": ["C"], "C": ["D"], "D": []}
        self.assertEqual(run_bfs(repo, "A", 1), "A: B")
        self.assertEqual(run_bfs(repo, "A", 2), "A: B\nB: C")

    def test_filter(self):
        repo = {"A": ["B", "XB"], "B": ["XC"], "XB": ["C"], "XC": [],
                "C": []}
        self.assertEqual(run_bfs(repo, "A", 5, "X"), "A: B\nB:")

    def test_cycle(self):
        repo = {"A": ["B"], "B": ["A"]}
        self.assertEqual(run_bfs(repo, "A", 100), "A: B\nB: A")

    def test_self_loop(self):
        self.assertEqual(run_bfs({"A": ["A"]}, "A", 100), "A: A")

    def test_no_recursion_on_long_chain(self):
        size = 5000
        repo = {f"P{i}": [f"P{i + 1}"] for i in range(size)}
        repo[f"P{size}"] = []
        order, _ = bfs("P0", size + 1, "", repo.get)
        self.assertEqual(len(order), size + 1)

    def test_each_package_is_asked_once(self):
        repo = read_repo_file(os.path.join(REPOS, "complex.txt"))
        asked = []

        def get_deps(name):
            asked.append(name)
            return repo[name]

        order, _ = bfs("A", 100, "", get_deps)
        self.assertEqual(asked, order)
        self.assertEqual(len(asked), len(set(asked)))

    def test_reverse_edges(self):
        repo = {"A": ["B", "C"], "B": ["C"], "C": []}
        self.assertEqual(reverse_edges(repo),
                         {"A": [], "B": ["A"], "C": ["A", "B"]})

    def test_reverse_uses_same_bfs(self):
        repo = reverse_edges({"A": ["B"], "B": ["C"], "C": [], "D": ["C"]})
        self.assertEqual(run_bfs(repo, "C", 10), "C: B D\nB: A\nD:\nA:")
        self.assertEqual(run_bfs(repo, "C", 1), "C: B D")

    def test_cases_from_file(self):
        for file, root, depth, skip, mode, expected in read_cases():
            with self.subTest(file=file, root=root, expected=expected):
                repo = read_repo_file(os.path.join(REPOS, file))
                if mode == "reverse":
                    repo = reverse_edges(repo)
                skip = "" if skip == "-" else skip
                path = os.path.join(REPOS, "expected", expected)
                with open(path, encoding="utf-8") as answer:
                    self.assertEqual(run_bfs(repo, root, int(depth), skip),
                                     answer.read().rstrip("\n"))


# обход настоящего формата npm через поддельный репозиторий
class RegistryGraphTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server, cls.url = start_registry()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def snapshot_deps(self, name):
        return SNAPSHOT[name]["dependencies"]

    def test_same_as_snapshot(self):
        for root in ["express", "axios", "yargs", "@babel/core"]:
            with self.subTest(root=root):
                online = bfs(root, 4, "",
                             partial(get_dependencies, self.url))
                offline = bfs(root, 4, "", self.snapshot_deps)
                self.assertEqual(online, offline)

    def test_filter_and_depth(self):
        order, edges = bfs("express", 3, "type",
                           partial(get_dependencies, self.url))
        self.assertNotIn("type-is", order)
        self.assertNotIn("mime-types", order)
        self.assertNotIn("content-type", edges["express"])
        self.assertIn("accepts", order)
        for deps in edges.values():
            self.assertFalse([dep for dep in deps if "type" in dep])

    def run_main(self, argv):
        out = StringIO()
        err = StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_main_online(self):
        code, out, _ = self.run_main(["--package", "axios", "--repo",
                                      self.url, "--max-depth", "2"])
        self.assertEqual(code, 0)
        first = out.splitlines()[0]
        deps = " ".join(SNAPSHOT["axios"]["dependencies"])
        self.assertEqual(first, f"axios: {deps}")

    def test_main_test_mode(self):
        code, out, _ = self.run_main(["--package", "A", "--repo",
                                      os.path.join(REPOS, "cycle.txt"),
                                      "--test-mode", "--filter", "D"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "A: B\nB: C\nC: A\n")

    def test_main_reverse(self):
        code, out, _ = self.run_main(["--package", "D", "--repo",
                                      os.path.join(REPOS, "cycle.txt"),
                                      "--test-mode", "--reverse"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "D: C\nC: B\nB: A\nA: C\n")

    def test_main_unknown_package(self):
        code, _, err = self.run_main(["--package", "Z", "--repo",
                                      os.path.join(REPOS, "simple.txt"),
                                      "--test-mode"])
        self.assertEqual(code, 1)
        self.assertIn("пакет Z не описан", err)


if __name__ == "__main__":
    unittest.main()

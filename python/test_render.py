import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from unittest.mock import patch

from depviz import main
from filerepo import read_repo_file
from graph import bfs, reverse_edges
from render import RenderError, ascii_tree, save_png, save_text, to_plantuml

REPOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "repos")
HAS_JAVA = shutil.which("java") is not None


# обход тестового репозитория для проверки рисования
def graph_of(repo, root, depth=10):
    return bfs(root, depth, "", repo.get)


class PlantUmlTest(unittest.TestCase):

    def test_simple(self):
        order, edges = graph_of({"A": ["B", "C"], "B": ["C"], "C": []}, "A")
        self.assertEqual(to_plantuml(order, edges).splitlines(), [
            "@startuml",
            "!pragma layout smetana",
            'rectangle "A" as p0',
            'rectangle "B" as p1',
            'rectangle "C" as p2',
            "p0 --> p1",
            "p0 --> p2",
            "p1 --> p2",
            "@enduml",
        ])

    def test_npm_names_and_cycle(self):
        edges = {"@babel/core": ["debug", "@babel/types"], "debug": ["ms"],
                 "@babel/types": ["@babel/core"]}
        order = ["@babel/core", "debug", "@babel/types"]
        text = to_plantuml(order, edges)
        self.assertIn('rectangle "@babel/core" as p0', text)
        self.assertIn('rectangle "ms" as p3', text)
        self.assertIn("p2 --> p0", text)

    def test_not_expanded_packages_are_drawn(self):
        order, edges = graph_of({"A": ["B"], "B": ["C"], "C": []}, "A", 1)
        text = to_plantuml(order, edges)
        self.assertIn('rectangle "B" as p1', text)
        self.assertNotIn('"C"', text)

    def test_versions_in_labels(self):
        order, edges = graph_of({"A": ["B", "C"], "B": [], "C": []}, "A")
        text = to_plantuml(order, edges, versions={"A": "1.2.3", "B": "0.1.0"})
        self.assertIn('rectangle "A\\n1.2.3" as p0', text)
        self.assertIn('rectangle "B\\n0.1.0" as p1', text)
        self.assertIn('rectangle "C" as p2', text)

    def test_reverse_arrows(self):
        repo = reverse_edges({"A": ["C"], "B": ["C"], "C": []})
        order, edges = graph_of(repo, "C")
        lines = to_plantuml(order, edges, reverse=True).splitlines()
        self.assertIn("p1 --> p0", lines)
        self.assertIn("p2 --> p0", lines)
        self.assertNotIn("p0 --> p1", lines)


class AsciiTreeTest(unittest.TestCase):

    def test_tree(self):
        repo = {"A": ["B", "C"], "B": ["D", "E"], "C": [], "D": [], "E": []}
        order, edges = graph_of(repo, "A")
        self.assertEqual(ascii_tree("A", edges), "\n".join([
            "A",
            "|-- B",
            "|   |-- D",
            "|   `-- E",
            "`-- C",
        ]))

    def test_cycle_and_repeat(self):
        order, edges = graph_of({"A": ["B", "C"], "B": ["C"], "C": ["A"]},
                                "A")
        self.assertEqual(ascii_tree("A", edges), "\n".join([
            "A",
            "|-- B",
            "|   `-- C (повтор)",
            "`-- C",
            "    `-- A (цикл)",
        ]))

    def test_self_loop_and_leaf_repeat(self):
        order, edges = graph_of({"A": ["A", "B", "C"], "B": ["C"], "C": []},
                                "A")
        self.assertEqual(ascii_tree("A", edges), "\n".join([
            "A",
            "|-- A (цикл)",
            "|-- B",
            "|   `-- C",
            "`-- C",
        ]))

    def test_not_deeper_than_max_depth(self):
        repo = {"A": ["B", "C"], "B": ["C"], "C": ["D"], "D": ["E"], "E": []}
        order, edges = graph_of(repo, "A", 2)
        self.assertEqual(ascii_tree("A", edges), "\n".join([
            "A",
            "|-- B",
            "|   `-- C (повтор)",
            "`-- C",
            "    `-- D",
        ]))

    def test_tree_level_is_bfs_depth(self):
        repo = read_repo_file(os.path.join(REPOS, "complex.txt"))
        for depth in range(1, 8):
            order, edges = graph_of(repo, "A", depth)
            for line in ascii_tree("A", edges).splitlines()[1:]:
                level = line.index("-- ") // 4 + 1
                self.assertLessEqual(level, depth)

    def test_only_ascii_symbols_in_lines(self):
        order, edges = graph_of({"A": ["B"], "B": ["C"], "C": []}, "A")
        self.assertTrue(ascii_tree("A", edges).isascii())

    def test_complex_repo_has_every_package(self):
        repo = read_repo_file(os.path.join(REPOS, "complex.txt"))
        order, edges = graph_of(repo, "A")
        names = set()
        for line in ascii_tree("A", edges).splitlines():
            names.add(line.split("-- ")[-1].split(" (")[0])
        self.assertEqual(names, set(order))

    def test_long_chain_without_recursion(self):
        size = 3000
        repo = {f"P{i}": [f"P{i + 1}"] for i in range(size)}
        repo[f"P{size}"] = []
        order, edges = graph_of(repo, "P0", size + 1)
        self.assertEqual(len(ascii_tree("P0", edges).splitlines()), size + 1)


class FilesTest(unittest.TestCase):

    def test_save_text(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "graph.puml")
            save_text("@startuml\n@enduml\n", path)
            with open(path, encoding="utf-8") as file:
                self.assertEqual(file.read(), "@startuml\n@enduml\n")
            with self.assertRaises(RenderError):
                save_text("x", os.path.join(folder, "no", "graph.puml"))

    @unittest.skipUnless(HAS_JAVA, "нет Java")
    def test_save_png(self):
        order, edges = graph_of({"A": ["B"], "B": ["A"]}, "A")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "graph.png")
            save_png(to_plantuml(order, edges), path)
            with open(path, "rb") as file:
                self.assertEqual(file.read(8), b"\x89PNG\r\n\x1a\n")

    def test_no_java(self):
        with patch("render.subprocess.run", side_effect=FileNotFoundError):
            with self.assertRaises(RenderError) as error:
                save_png("@startuml\n@enduml\n", "graph.png")
        self.assertIn("нужна Java", str(error.exception))

    @unittest.skipUnless(HAS_JAVA, "нет Java")
    def test_plantuml_error(self):
        with patch("render.PLANTUML_JAR", "missing.jar"):
            with self.assertRaises(RenderError) as error:
                save_png("@startuml\n@enduml\n", "graph.png")
        self.assertIn("PlantUML не смог", str(error.exception))


# вся программа: дерево на экране, PNG и текст PlantUML в файлах
class MainTest(unittest.TestCase):

    @unittest.skipUnless(HAS_JAVA, "нет Java")
    def test_ascii_tree_and_files(self):
        with tempfile.TemporaryDirectory() as folder:
            output = os.path.join(folder, "cycle.png")
            out = StringIO()
            with redirect_stdout(out), redirect_stderr(StringIO()):
                code = main(["--package", "A", "--test-mode", "--repo",
                             os.path.join(REPOS, "cycle.txt"),
                             "--ascii-tree", "--output", output])
            self.assertEqual(code, 0)
            lines = out.getvalue().splitlines()
            self.assertEqual(lines[:5], ["A", "`-- B", "    `-- C",
                                         "        |-- A (цикл)",
                                         "        `-- D"])
            self.assertTrue(lines[5].startswith("Граф сохранен в"))
            self.assertTrue(os.path.isfile(output))
            with open(os.path.join(folder, "cycle.puml"),
                      encoding="utf-8") as file:
                self.assertIn("p2 --> p0", file.read())


if __name__ == "__main__":
    unittest.main()

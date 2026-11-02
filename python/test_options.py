import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO

from depviz import CheckOptions, main, option_error

HERE = os.path.dirname(os.path.abspath(__file__))
SIMPLE_REPO = os.path.join(HERE, "..", "repos", "simple.txt")
DEFAULTS = {
    "packageName": "express",
    "repoPath": "https://registry.npmjs.org",
    "testMode": False,
    "outputFile": "graph.png",
    "asciiTree": False,
    "maxDepth": "5",
    "filterText": None,
}


# проверка параметров командной строки
class OptionsTest(unittest.TestCase):

    # параметры по умолчанию, измененные передаются явно
    def check(self, **changes):
        values = dict(DEFAULTS)
        values.update(changes)
        return CheckOptions(**values)

    def assert_error(self, text, **changes):
        with self.assertRaises(option_error) as error:
            self.check(**changes)
        self.assertIn(text, str(error.exception))

    def test_defaults(self):
        options = self.check()
        self.assertEqual(options["package"], "express")
        self.assertEqual(options["max_depth"], 5)
        self.assertEqual(options["filter"], "")
        self.assertFalse(options["test_mode"])

    def test_package(self):
        self.check(packageName="@babel/core")
        self.check(packageName="lodash.merge")
        self.assert_error("не задано имя пакета", packageName=None)
        self.assert_error("не задано имя пакета", packageName="")
        self.assert_error("недопустимое имя", packageName="Express")
        self.assert_error("недопустимое имя", packageName=".hidden")
        self.assert_error("недопустимое имя", packageName="my package")
        self.assert_error("длиннее 214", packageName="a" * 215)

    def test_test_mode(self):
        options = self.check(packageName="A", repoPath=SIMPLE_REPO,
                             testMode=True)
        self.assertTrue(options["test_mode"])
        self.assert_error("больших латинских букв", packageName="a",
                          repoPath=SIMPLE_REPO, testMode=True)
        self.assert_error("больших латинских букв", packageName="A1",
                          repoPath=SIMPLE_REPO, testMode=True)

    def test_repo(self):
        self.check(repoPath="http://localhost:4873")
        self.assert_error("не задан репозиторий", repoPath="")
        self.assert_error("неверный URL-адрес", repoPath="registry.npmjs.org")
        self.assert_error("неверный URL-адрес", repoPath="ftp://example.com")
        self.assert_error("добавьте --test-mode", repoPath=SIMPLE_REPO)
        self.assert_error("не найден", packageName="A", testMode=True,
                          repoPath="missing.txt")
        self.assert_error("не найден", packageName="A", testMode=True,
                          repoPath=HERE)

    def test_output(self):
        self.check(outputFile="GRAPH.PNG")
        self.assert_error("не задано имя файла", outputFile="")
        self.assert_error("расширение .png", outputFile="graph.jpg")
        self.assert_error("не найдена", outputFile="missing/graph.png")
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "dir.png")
            os.mkdir(path)
            self.assert_error("является папкой", outputFile=path)
            self.check(outputFile=os.path.join(folder, "graph.png"))

    def test_depth(self):
        self.assertEqual(self.check(maxDepth="1")["max_depth"], 1)
        self.assertEqual(self.check(maxDepth="100")["max_depth"], 100)
        self.assert_error("целым положительным", maxDepth="abc")
        self.assert_error("целым положительным", maxDepth="-1")
        self.assert_error("целым положительным", maxDepth="2.5")
        self.assert_error("целым положительным", maxDepth="")
        self.assert_error("от 1 до 100", maxDepth="0")
        self.assert_error("от 1 до 100", maxDepth="101")

    def test_filter(self):
        self.assertEqual(self.check(filterText="test")["filter"], "test")
        self.assert_error("не может быть пустой", filterText="")
        self.assert_error("не может быть пустой", filterText="  ")
        self.assert_error("сам содержит", filterText="press")


# запуск всей программы
class MainTest(unittest.TestCase):

    def run_main(self, argv):
        out = StringIO()
        err = StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_error(self):
        code, out, err = self.run_main(["--max-depth", "x", "--package", "a"])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Ошибка: глубина анализа", err)


if __name__ == "__main__":
    unittest.main()

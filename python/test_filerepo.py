import os
import tempfile
import unittest

from filerepo import RepoFileError, read_repo_file

REPOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                     "repos")


# чтение файлов тестового репозитория
class RepoFileTest(unittest.TestCase):

    def read(self, name):
        return read_repo_file(os.path.join(REPOS, name))

    def assert_error(self, name, text):
        with self.assertRaises(RepoFileError) as error:
            self.read(name)
        self.assertIn(text, str(error.exception))

    def test_simple(self):
        self.assertEqual(self.read("simple.txt"),
                         {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []})

    def test_order_is_kept(self):
        repo = self.read("filter.txt")
        self.assertEqual(list(repo), ["A", "B", "C", "XA", "XB", "D", "E"])
        self.assertEqual(repo["A"], ["B", "XA", "C"])

    def test_cycles_are_allowed(self):
        self.assertEqual(self.read("cycle.txt")["C"], ["A", "D"])
        self.assertEqual(self.read("self.txt")["A"], ["A", "B"])

    def test_comments_spaces_and_line_ends(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "repo.txt")
            with open(path, "w", encoding="utf-8", newline="") as file:
                file.write("# repo\r\n\r\n  AB :  CD   E # comment\r\n"
                           "CD:\r\nE:#\r\n")
            self.assertEqual(read_repo_file(path),
                             {"AB": ["CD", "E"], "CD": [], "E": []})

    def test_byte_order_mark(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "repo.txt")
            with open(path, "w", encoding="utf-8-sig") as file:
                file.write("A: B\nB:\n")
            self.assertEqual(read_repo_file(path), {"A": ["B"], "B": []})

    def test_errors(self):
        self.assert_error("errors/no_colon.txt", "строка 3: нет двоеточия")
        self.assert_error("errors/lowercase.txt", "'b' должно состоять")
        self.assert_error("errors/duplicate.txt", "пакет A описан повторно")
        self.assert_error("errors/repeated.txt", "повторяется зависимость")
        self.assert_error("errors/undefined.txt", "пакет C, от которого")
        self.assert_error("errors/empty.txt", "нет ни одного пакета")
        self.assert_error("missing.txt", "не удалось прочитать")


if __name__ == "__main__":
    unittest.main()

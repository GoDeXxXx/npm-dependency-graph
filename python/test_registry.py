import json
import socket
import threading
import unittest
from contextlib import redirect_stderr, redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import StringIO
from urllib.parse import unquote

from depviz import main
from registry import RegistryError, get_dependencies, latest_url
from registry_snapshot import SNAPSHOT


# поддельный репозиторий npm: отвечает на /<имя>/latest по снимку реестра
class FakeRegistry(BaseHTTPRequestHandler):

    def do_GET(self):
        parts = self.path.split("/")
        name = unquote("/".join(parts[1:-1]))
        if name == "broken-json":
            body = b"<html>not json</html>"
        elif parts[-1] == "latest" and name in SNAPSHOT:
            body = json.dumps({"name": name, **SNAPSHOT[name]}).encode()
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


# запуск поддельного репозитория в отдельном потоке
def start_registry():
    server = HTTPServer(("127.0.0.1", 0), FakeRegistry)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_port}"


# свободный порт, на котором никто не слушает
def free_port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


class RegistryTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server, cls.url = start_registry()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_latest_url(self):
        self.assertEqual(latest_url("https://registry.npmjs.org/", "ms"),
                         "https://registry.npmjs.org/ms/latest")
        self.assertEqual(latest_url("http://host", "@babel/core"),
                         "http://host/@babel%2Fcore/latest")

    def test_dependencies(self):
        deps = get_dependencies(self.url, "express")
        self.assertEqual(deps, SNAPSHOT["express"]["dependencies"])
        self.assertEqual(list(deps), list(SNAPSHOT["express"]["dependencies"]))

    def test_scoped_package(self):
        deps = get_dependencies(self.url, "@babel/core")
        self.assertEqual(deps, SNAPSHOT["@babel/core"]["dependencies"])

    def test_no_dependencies(self):
        self.assertEqual(get_dependencies(self.url, "ms"), {})

    def test_not_found(self):
        with self.assertRaises(RegistryError) as error:
            get_dependencies(self.url, "no-such-package")
        self.assertIn("не найден", str(error.exception))

    def test_not_json(self):
        with self.assertRaises(RegistryError) as error:
            get_dependencies(self.url, "broken-json")
        self.assertIn("не JSON", str(error.exception))

    def test_no_connection(self):
        url = f"http://127.0.0.1:{free_port()}"
        with self.assertRaises(RegistryError) as error:
            get_dependencies(url, "express")
        self.assertIn("не удалось подключиться", str(error.exception))

    def run_main(self, argv):
        out = StringIO()
        err = StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(argv)
        return code, out.getvalue(), err.getvalue()

    def test_main_without_dependencies(self):
        code, out, _ = self.run_main(["--package", "ms", "--repo", self.url])
        self.assertEqual(code, 0)
        self.assertEqual(out, "ms:\n")

    def test_main_errors(self):
        code, out, err = self.run_main(["--package", "nope", "--repo",
                                        self.url])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertIn("Ошибка: пакет nope не найден", err)


if __name__ == "__main__":
    unittest.main()

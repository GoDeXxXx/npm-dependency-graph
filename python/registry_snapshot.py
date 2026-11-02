# снимок реестра npm для тестов без доступа к сети:
# поля version и dependencies последних версий пакетов из деревьев
# express, axios, yargs, @babel/core и eslint (получены 2 ноября 2026)
SNAPSHOT = {
    "@babel/code-frame": {
        "version": "8.0.6",
        "dependencies": {
            "js-tokens": "^10.0.0",
            "@babel/helper-validator-identifier": "^8.0.6",
        },
    },
    "@babel/compat-data": {
        "version": "8.0.5",
        "dependencies": {},
    },
    "@babel/core": {
        "version": "8.0.10",
        "dependencies": {
            "obug": "^3.0.0",
            "json5": "^2.2.3",
            "verkit": "^0.5.0",
            "gensync": "^1.0.0-beta.2",
            "empathic": "^2.0.1",
            "@babel/types": "^8.0.10",
            "@babel/parser": "^8.0.10",
            "@babel/helpers": "^8.0.10",
            "@types/gensync": "^1.0.5",
            "@babel/template": "^8.0.0",
            "@babel/traverse": "^8.0.10",
            "@babel/generator": "^8.0.10",
            "@babel/code-frame": "^8.0.6",
            "convert-source-map": "^2.0.0",
            "import-meta-resolve": "^4.2.0",
            "@babel/helper-compilation-targets": "^8.0.7",
        },
    },
    "@babel/generator": {
        "version": "8.0.10",
        "dependencies": {
            "jsesc": "^3.0.2",
            "@babel/types": "^8.0.10",
            "@types/jsesc": "^2.5.0",
            "@babel/parser": "^8.0.10",
            "@jridgewell/gen-mapping": "0.4.0-beta.0",
            "@jridgewell/trace-mapping": "^0.3.31",
        },
    },
    "@babel/helper-compilation-targets": {
        "version": "8.0.7",
        "dependencies": {
            "flru": "1.0.2",
            "verkit": "^0.5.0",
            "browserslist": "^4.24.0",
            "@babel/compat-data": "^8.0.5",
            "@babel/helper-validator-option": "^8.0.0",
        },
    },
    "@babel/helper-globals": {
        "version": "8.0.6",
        "dependencies": {},
    },
    "@babel/helper-string-parser": {
        "version": "8.0.8",
        "dependencies": {},
    },
    "@babel/helper-validator-identifier": {
        "version": "8.0.6",
        "dependencies": {},
    },
    "@babel/helper-validator-option": {
        "version": "8.0.0",
        "dependencies": {},
    },
    "@babel/helpers": {
        "version": "8.0.10",
        "dependencies": {
            "@babel/types": "^8.0.10",
            "@babel/template": "^8.0.0",
        },
    },
    "@babel/parser": {
        "version": "8.0.10",
        "dependencies": {
            "@babel/types": "^8.0.10",
        },
    },
    "@babel/template": {
        "version": "8.0.0",
        "dependencies": {
            "@babel/types": "^8.0.0",
            "@babel/parser": "^8.0.0",
            "@babel/code-frame": "^8.0.0",
        },
    },
    "@babel/traverse": {
        "version": "8.0.10",
        "dependencies": {
            "obug": "^3.0.0",
            "@babel/types": "^8.0.10",
            "@babel/parser": "^8.0.10",
            "@babel/template": "^8.0.0",
            "@babel/generator": "^8.0.10",
            "@babel/code-frame": "^8.0.6",
            "@babel/helper-globals": "^8.0.6",
        },
    },
    "@babel/types": {
        "version": "8.0.10",
        "dependencies": {
            "@babel/helper-string-parser": "^8.0.8",
            "@babel/helper-validator-identifier": "^8.0.6",
        },
    },
    "@cacheable/memory": {
        "version": "2.2.0",
        "dependencies": {
            "keyv": "^5.6.0",
            "hookified": "^1.15.1",
            "@keyv/bigmap": "^1.3.1",
            "@cacheable/utils": "^2.5.0",
        },
    },
    "@cacheable/utils": {
        "version": "2.5.0",
        "dependencies": {
            "keyv": "^5.6.0",
            "hashery": "^1.5.1",
        },
    },
    "@eslint-community/eslint-utils": {
        "version": "4.10.1",
        "dependencies": {
            "eslint-visitor-keys": "^3.4.3",
        },
    },
    "@eslint-community/regexpp": {
        "version": "4.12.2",
        "dependencies": {},
    },
    "@eslint/config-array": {
        "version": "0.23.5",
        "dependencies": {
            "debug": "^4.3.1",
            "minimatch": "^10.2.4",
            "@eslint/object-schema": "^3.0.5",
        },
    },
    "@eslint/config-helpers": {
        "version": "0.7.0",
        "dependencies": {
            "@eslint/core": "^1.2.1",
        },
    },
    "@eslint/core": {
        "version": "1.2.1",
        "dependencies": {
            "@types/json-schema": "^7.0.15",
        },
    },
    "@eslint/object-schema": {
        "version": "3.0.5",
        "dependencies": {},
    },
    "@eslint/plugin-kit": {
        "version": "0.7.3",
        "dependencies": {
            "levn": "^0.4.1",
            "@eslint/core": "^1.2.1",
        },
    },
    "@humanfs/core": {
        "version": "0.20.0",
        "dependencies": {
            "@humanfs/types": "^0.16.0",
        },
    },
    "@humanfs/node": {
        "version": "0.17.0",
        "dependencies": {
            "@humanfs/core": "^0.20.0",
            "@humanfs/types": "^0.16.0",
            "@humanwhocodes/retry": "^0.4.0",
        },
    },
    "@humanfs/types": {
        "version": "0.16.0",
        "dependencies": {},
    },
    "@humanwhocodes/module-importer": {
        "version": "1.0.1",
        "dependencies": {},
    },
    "@humanwhocodes/retry": {
        "version": "0.4.3",
        "dependencies": {},
    },
    "@isaacs/nonrecursive-glob-match": {
        "version": "1.0.3",
        "dependencies": {},
    },
    "@jridgewell/gen-mapping": {
        "version": "0.3.13",
        "dependencies": {
            "@jridgewell/trace-mapping": "^0.3.24",
            "@jridgewell/sourcemap-codec": "^1.5.0",
        },
    },
    "@jridgewell/resolve-uri": {
        "version": "3.1.2",
        "dependencies": {},
    },
    "@jridgewell/sourcemap-codec": {
        "version": "1.6.0",
        "dependencies": {},
    },
    "@jridgewell/trace-mapping": {
        "version": "0.3.31",
        "dependencies": {
            "@jridgewell/resolve-uri": "^3.1.0",
            "@jridgewell/sourcemap-codec": "^1.4.14",
        },
    },
    "@keyv/bigmap": {
        "version": "6.1.0",
        "dependencies": {
            "hashery": "^3.0.1",
            "hookified": "^3.0.3",
        },
    },
    "@types/esrecurse": {
        "version": "4.3.1",
        "dependencies": {},
    },
    "@types/estree": {
        "version": "1.0.10",
        "dependencies": {},
    },
    "@types/gensync": {
        "version": "1.0.5",
        "dependencies": {},
    },
    "@types/jsesc": {
        "version": "3.0.3",
        "dependencies": {},
    },
    "@types/json-schema": {
        "version": "7.0.15",
        "dependencies": {},
    },
    "accepts": {
        "version": "1.3.8",
        "dependencies": {
            "mime-types": "~2.1.34",
            "negotiator": "0.6.3",
        },
    },
    "acorn": {
        "version": "8.19.0",
        "dependencies": {},
    },
    "acorn-jsx": {
        "version": "5.3.2",
        "dependencies": {},
    },
    "agent-base": {
        "version": "9.0.0",
        "dependencies": {},
    },
    "ajv": {
        "version": "8.20.0",
        "dependencies": {
            "fast-uri": "^3.0.1",
            "fast-deep-equal": "^3.1.3",
            "require-from-string": "^2.0.2",
            "json-schema-traverse": "^1.0.0",
        },
    },
    "ansi-regex": {
        "version": "6.5.0",
        "dependencies": {},
    },
    "ansi-styles": {
        "version": "7.0.0",
        "dependencies": {},
    },
    "asynckit": {
        "version": "0.5.0",
        "dependencies": {},
    },
    "axios": {
        "version": "1.21.0",
        "dependencies": {
            "form-data": "^4.0.6",
            "proxy-from-env": "^2.1.0",
            "follow-redirects": "^1.16.0",
            "https-proxy-agent": "^5.0.1",
        },
    },
    "balanced-match": {
        "version": "5.0.0",
        "dependencies": {},
    },
    "baseline-browser-mapping": {
        "version": "2.11.34",
        "dependencies": {},
    },
    "body-parser": {
        "version": "2.4.0",
        "dependencies": {
            "qs": "^6.16.1",
            "bytes": "^3.1.2",
            "debug": "^4.4.3",
            "type-is": "^2.1.0",
            "raw-body": "^3.0.2",
            "iconv-lite": "^0.7.3",
            "http-errors": "^2.0.1",
            "on-finished": "^2.4.1",
            "content-type": "^2.1.0",
        },
    },
    "brace-expansion": {
        "version": "5.0.12",
        "dependencies": {
            "balanced-match": "^4.0.2",
        },
    },
    "browserslist": {
        "version": "4.29.5",
        "dependencies": {
            "caniuse-lite": "^1.0.30001819",
            "node-releases": "^2.0.60",
            "electron-to-chromium": "^1.5.464",
            "update-browserslist-db": "^1.3.4",
            "baseline-browser-mapping": "^2.11.33",
        },
    },
    "bytes": {
        "version": "3.1.2",
        "dependencies": {},
    },
    "cacheable": {
        "version": "2.5.0",
        "dependencies": {
            "keyv": "^5.6.0",
            "qified": "^0.10.1",
            "hookified": "^1.15.0",
            "@cacheable/utils": "^2.5.0",
            "@cacheable/memory": "^2.2.0",
        },
    },
    "call-bind-apply-helpers": {
        "version": "1.0.2",
        "dependencies": {
            "es-errors": "^1.3.0",
            "function-bind": "^1.1.2",
        },
    },
    "call-bound": {
        "version": "1.0.4",
        "dependencies": {
            "get-intrinsic": "^1.3.0",
            "call-bind-apply-helpers": "^1.0.2",
        },
    },
    "caniuse-lite": {
        "version": "1.0.30001820",
        "dependencies": {},
    },
    "cliui": {
        "version": "9.0.1",
        "dependencies": {
            "wrap-ansi": "^9.0.0",
            "strip-ansi": "^7.1.0",
            "string-width": "^7.2.0",
        },
    },
    "combined-stream": {
        "version": "1.0.8",
        "dependencies": {
            "delayed-stream": "~1.0.0",
        },
    },
    "content-disposition": {
        "version": "3.0.0",
        "dependencies": {},
    },
    "content-type": {
        "version": "3.1.1",
        "dependencies": {},
    },
    "convert-source-map": {
        "version": "2.0.0",
        "dependencies": {},
    },
    "cookie": {
        "version": "2.0.1",
        "dependencies": {},
    },
    "cookie-signature": {
        "version": "1.2.2",
        "dependencies": {},
    },
    "cross-spawn": {
        "version": "7.0.6",
        "dependencies": {
            "which": "^2.0.1",
            "path-key": "^3.1.0",
            "shebang-command": "^2.0.0",
        },
    },
    "debug": {
        "version": "4.4.3",
        "dependencies": {
            "ms": "^2.1.3",
        },
    },
    "deep-is": {
        "version": "0.1.4",
        "dependencies": {},
    },
    "delayed-stream": {
        "version": "1.0.0",
        "dependencies": {},
    },
    "depd": {
        "version": "2.0.0",
        "dependencies": {},
    },
    "dunder-proto": {
        "version": "1.0.1",
        "dependencies": {
            "gopd": "^1.2.0",
            "es-errors": "^1.3.0",
            "call-bind-apply-helpers": "^1.0.1",
        },
    },
    "ee-first": {
        "version": "1.1.1",
        "dependencies": {},
    },
    "electron-to-chromium": {
        "version": "1.5.472",
        "dependencies": {},
    },
    "empathic": {
        "version": "2.1.0",
        "dependencies": {},
    },
    "encodeurl": {
        "version": "3.0.0",
        "dependencies": {},
    },
    "es-define-property": {
        "version": "1.0.1",
        "dependencies": {},
    },
    "es-errors": {
        "version": "1.3.0",
        "dependencies": {},
    },
    "es-object-atoms": {
        "version": "1.1.2",
        "dependencies": {
            "es-errors": "^1.3.0",
        },
    },
    "es-set-tostringtag": {
        "version": "2.1.0",
        "dependencies": {
            "hasown": "^2.0.2",
            "es-errors": "^1.3.0",
            "get-intrinsic": "^1.2.6",
            "has-tostringtag": "^1.0.2",
        },
    },
    "escalade": {
        "version": "3.2.0",
        "dependencies": {},
    },
    "escape-html": {
        "version": "1.0.3",
        "dependencies": {},
    },
    "escape-string-regexp": {
        "version": "5.0.0",
        "dependencies": {},
    },
    "eslint": {
        "version": "10.14.0",
        "dependencies": {
            "ajv": "^6.14.0",
            "debug": "^4.3.2",
            "espree": "^11.2.0",
            "ignore": "^5.2.0",
            "esquery": "^1.7.0",
            "esutils": "^2.0.2",
            "find-up": "^5.0.0",
            "is-glob": "^4.0.0",
            "minimatch": "^10.2.6",
            "optionator": "^0.9.3",
            "cross-spawn": "^7.0.6",
            "glob-parent": "^6.0.2",
            "imurmurhash": "^0.1.4",
            "@eslint/core": "^1.2.1",
            "eslint-scope": "^9.1.2",
            "@humanfs/node": "^0.16.8",
            "@types/estree": "^1.0.6",
            "fast-deep-equal": "^3.1.3",
            "natural-compare": "^1.4.0",
            "file-entry-cache": "11.1.5 || >11.1.6 <12",
            "@eslint/plugin-kit": "^0.7.3",
            "eslint-visitor-keys": "^5.0.1",
            "@eslint/config-array": "^0.23.5",
            "@humanwhocodes/retry": "^0.4.2",
            "escape-string-regexp": "^4.0.0",
            "@eslint/config-helpers": "^0.7.0",
            "@eslint-community/regexpp": "^4.12.2",
            "@eslint-community/eslint-utils": "^4.8.0",
            "@humanwhocodes/module-importer": "^1.0.1",
            "json-stable-stringify-without-jsonify": "^1.0.1",
        },
    },
    "eslint-scope": {
        "version": "9.1.2",
        "dependencies": {
            "esrecurse": "^4.3.0",
            "estraverse": "^5.2.0",
            "@types/estree": "^1.0.8",
            "@types/esrecurse": "^4.3.1",
        },
    },
    "eslint-visitor-keys": {
        "version": "5.0.1",
        "dependencies": {},
    },
    "espree": {
        "version": "11.2.0",
        "dependencies": {
            "acorn": "^8.16.0",
            "acorn-jsx": "^5.3.2",
            "eslint-visitor-keys": "^5.0.1",
        },
    },
    "esquery": {
        "version": "1.7.0",
        "dependencies": {
            "estraverse": "^5.1.0",
        },
    },
    "esrecurse": {
        "version": "4.3.0",
        "dependencies": {
            "estraverse": "^5.2.0",
        },
    },
    "estraverse": {
        "version": "5.3.0",
        "dependencies": {},
    },
    "esutils": {
        "version": "2.0.3",
        "dependencies": {},
    },
    "etag": {
        "version": "1.8.1",
        "dependencies": {},
    },
    "express": {
        "version": "5.3.0",
        "dependencies": {
            "qs": "^6.16.0",
            "depd": "^2.0.0",
            "etag": "^1.8.1",
            "once": "^1.4.0",
            "send": "^1.1.0",
            "vary": "^1.1.2",
            "debug": "^4.4.0",
            "fresh": "^2.0.0",
            "cookie": "^0.7.1",
            "router": "^2.2.0",
            "accepts": "^2.0.0",
            "type-is": "^2.1.0",
            "parseurl": "^1.3.3",
            "statuses": "^2.0.1",
            "encodeurl": "^2.0.0",
            "mime-types": "^3.0.0",
            "proxy-addr": "^2.0.8",
            "body-parser": "^2.3.0",
            "escape-html": "^1.0.3",
            "http-errors": "^2.0.0",
            "on-finished": "^2.4.1",
            "content-type": "^2.0.0",
            "finalhandler": "^2.1.0",
            "range-parser": "^1.2.1",
            "serve-static": "^2.2.0",
            "cookie-signature": "^1.2.1",
            "merge-descriptors": "^2.0.0",
            "content-disposition": "^2.0.1",
        },
    },
    "fast-deep-equal": {
        "version": "3.1.3",
        "dependencies": {},
    },
    "fast-levenshtein": {
        "version": "3.0.0",
        "dependencies": {
            "fastest-levenshtein": "^1.0.7",
        },
    },
    "fast-uri": {
        "version": "4.2.3",
        "dependencies": {},
    },
    "fastest-levenshtein": {
        "version": "1.0.16",
        "dependencies": {},
    },
    "file-entry-cache": {
        "version": "11.1.5",
        "dependencies": {
            "flat-cache": "^6.1.23",
        },
    },
    "finalhandler": {
        "version": "2.1.1",
        "dependencies": {
            "debug": "^4.4.0",
            "parseurl": "^1.3.3",
            "statuses": "^2.0.1",
            "encodeurl": "^2.0.0",
            "escape-html": "^1.0.3",
            "on-finished": "^2.4.1",
        },
    },
    "find-up": {
        "version": "8.0.0",
        "dependencies": {
            "locate-path": "^8.0.0",
            "unicorn-magic": "^0.3.0",
        },
    },
    "flat-cache": {
        "version": "6.1.23",
        "dependencies": {
            "flatted": "^3.4.2",
            "cacheable": "^2.5.0",
            "hookified": "^1.15.0",
        },
    },
    "flatted": {
        "version": "3.4.4",
        "dependencies": {},
    },
    "flru": {
        "version": "1.0.2",
        "dependencies": {},
    },
    "follow-redirects": {
        "version": "1.16.2",
        "dependencies": {},
    },
    "form-data": {
        "version": "4.0.6",
        "dependencies": {
            "hasown": "^2.0.4",
            "asynckit": "^0.4.0",
            "mime-types": "^2.1.35",
            "combined-stream": "^1.0.8",
            "es-set-tostringtag": "^2.1.0",
        },
    },
    "forwarded": {
        "version": "0.2.0",
        "dependencies": {},
    },
    "fresh": {
        "version": "0.5.2",
        "dependencies": {},
    },
    "function-bind": {
        "version": "1.1.2",
        "dependencies": {},
    },
    "gensync": {
        "version": "1.0.0-beta.2",
        "dependencies": {},
    },
    "get-caller-file": {
        "version": "2.0.5",
        "dependencies": {},
    },
    "get-east-asian-width": {
        "version": "1.7.0",
        "dependencies": {},
    },
    "get-intrinsic": {
        "version": "1.3.0",
        "dependencies": {
            "gopd": "^1.2.0",
            "hasown": "^2.0.2",
            "es-errors": "^1.3.0",
            "get-proto": "^1.0.1",
            "has-symbols": "^1.1.0",
            "function-bind": "^1.1.2",
            "es-object-atoms": "^1.1.1",
            "math-intrinsics": "^1.1.0",
            "es-define-property": "^1.0.1",
            "call-bind-apply-helpers": "^1.0.2",
        },
    },
    "get-proto": {
        "version": "1.0.1",
        "dependencies": {
            "dunder-proto": "^1.0.1",
            "es-object-atoms": "^1.0.0",
        },
    },
    "glob-parent": {
        "version": "6.0.2",
        "dependencies": {
            "is-glob": "^4.0.3",
        },
    },
    "gopd": {
        "version": "1.2.0",
        "dependencies": {},
    },
    "has-symbols": {
        "version": "1.1.0",
        "dependencies": {},
    },
    "has-tostringtag": {
        "version": "1.0.2",
        "dependencies": {
            "has-symbols": "^1.0.3",
        },
    },
    "hashery": {
        "version": "3.0.5",
        "dependencies": {
            "hookified": "^3.0.4",
        },
    },
    "hasown": {
        "version": "2.0.4",
        "dependencies": {
            "function-bind": "^1.1.2",
        },
    },
    "hookified": {
        "version": "3.1.0",
        "dependencies": {},
    },
    "http-errors": {
        "version": "2.0.1",
        "dependencies": {
            "depd": "~2.0.0",
            "inherits": "~2.0.4",
            "statuses": "~2.0.2",
            "toidentifier": "~1.0.1",
            "setprototypeof": "~1.2.0",
        },
    },
    "https-proxy-agent": {
        "version": "9.1.0",
        "dependencies": {
            "debug": "^4.3.4",
            "agent-base": "9.0.0",
            "proxy-agent-negotiate": "1.1.0",
        },
    },
    "iconv-lite": {
        "version": "0.7.3",
        "dependencies": {
            "safer-buffer": ">= 2.1.2 < 3.0.0",
        },
    },
    "ignore": {
        "version": "7.0.14",
        "dependencies": {},
    },
    "import-meta-resolve": {
        "version": "4.2.0",
        "dependencies": {},
    },
    "imurmurhash": {
        "version": "0.1.4",
        "dependencies": {},
    },
    "inherits": {
        "version": "2.0.4",
        "dependencies": {},
    },
    "ipaddr.js": {
        "version": "2.5.0",
        "dependencies": {},
    },
    "is-extglob": {
        "version": "2.1.1",
        "dependencies": {},
    },
    "is-glob": {
        "version": "4.0.3",
        "dependencies": {
            "is-extglob": "^2.1.1",
        },
    },
    "is-promise": {
        "version": "4.0.0",
        "dependencies": {},
    },
    "isexe": {
        "version": "4.0.0",
        "dependencies": {},
    },
    "js-tokens": {
        "version": "10.0.0",
        "dependencies": {},
    },
    "jsesc": {
        "version": "3.1.0",
        "dependencies": {},
    },
    "json-schema-traverse": {
        "version": "1.0.0",
        "dependencies": {},
    },
    "json-stable-stringify-without-jsonify": {
        "version": "1.0.1",
        "dependencies": {},
    },
    "json5": {
        "version": "2.2.3",
        "dependencies": {},
    },
    "keyv": {
        "version": "6.1.0",
        "dependencies": {
            "hookified": "^3.0.3",
        },
    },
    "levn": {
        "version": "0.4.1",
        "dependencies": {
            "prelude-ls": "^1.2.1",
            "type-check": "~0.4.0",
        },
    },
    "locate-path": {
        "version": "8.0.0",
        "dependencies": {
            "p-locate": "^6.0.0",
        },
    },
    "math-intrinsics": {
        "version": "1.1.0",
        "dependencies": {},
    },
    "merge-descriptors": {
        "version": "2.0.0",
        "dependencies": {},
    },
    "mime-db": {
        "version": "1.54.0",
        "dependencies": {},
    },
    "mime-types": {
        "version": "3.0.2",
        "dependencies": {
            "mime-db": "^1.54.0",
        },
    },
    "minimatch": {
        "version": "11.0.4",
        "dependencies": {
            "brace-expansion": "^5.0.12",
            "@isaacs/nonrecursive-glob-match": "^1.0.3",
        },
    },
    "ms": {
        "version": "2.1.3",
        "dependencies": {},
    },
    "natural-compare": {
        "version": "1.4.0",
        "dependencies": {},
    },
    "negotiator": {
        "version": "1.1.0",
        "dependencies": {
            "content-type": "^2.1.0",
        },
    },
    "node-releases": {
        "version": "2.0.63",
        "dependencies": {},
    },
    "object-inspect": {
        "version": "1.13.4",
        "dependencies": {},
    },
    "obug": {
        "version": "3.0.0",
        "dependencies": {},
    },
    "on-finished": {
        "version": "2.4.2",
        "dependencies": {
            "ee-first": "1.1.1",
        },
    },
    "once": {
        "version": "1.4.0",
        "dependencies": {
            "wrappy": "1",
        },
    },
    "optionator": {
        "version": "0.9.4",
        "dependencies": {
            "levn": "^0.4.1",
            "deep-is": "^0.1.3",
            "word-wrap": "^1.2.5",
            "prelude-ls": "^1.2.1",
            "type-check": "^0.4.0",
            "fast-levenshtein": "^2.0.6",
        },
    },
    "p-limit": {
        "version": "7.3.3",
        "dependencies": {
            "yocto-queue": "^1.2.1",
        },
    },
    "p-locate": {
        "version": "7.0.0",
        "dependencies": {
            "p-limit": "^7.2.0",
        },
    },
    "parseurl": {
        "version": "1.3.3",
        "dependencies": {},
    },
    "path-key": {
        "version": "4.0.0",
        "dependencies": {},
    },
    "path-to-regexp": {
        "version": "9.0.0",
        "dependencies": {},
    },
    "picocolors": {
        "version": "1.1.1",
        "dependencies": {},
    },
    "prelude-ls": {
        "version": "1.2.1",
        "dependencies": {},
    },
    "proxy-addr": {
        "version": "2.0.8",
        "dependencies": {
            "forwarded": "0.2.0",
            "ipaddr.js": "1.9.1",
        },
    },
    "proxy-agent-negotiate": {
        "version": "1.1.0",
        "dependencies": {},
    },
    "proxy-from-env": {
        "version": "2.1.0",
        "dependencies": {},
    },
    "qified": {
        "version": "0.13.2",
        "dependencies": {
            "hookified": "^3.0.3",
        },
    },
    "qs": {
        "version": "6.17.1",
        "dependencies": {
            "side-channel": "^1.1.1",
            "es-define-property": "^1.0.1",
        },
    },
    "range-parser": {
        "version": "1.3.0",
        "dependencies": {},
    },
    "raw-body": {
        "version": "4.0.0",
        "dependencies": {
            "bytes": "^3.1.2",
            "http-errors": "^2.0.1",
        },
    },
    "require-from-string": {
        "version": "2.0.2",
        "dependencies": {},
    },
    "router": {
        "version": "2.2.0",
        "dependencies": {
            "depd": "^2.0.0",
            "debug": "^4.4.0",
            "parseurl": "^1.3.3",
            "is-promise": "^4.0.0",
            "path-to-regexp": "^8.0.0",
        },
    },
    "safer-buffer": {
        "version": "2.1.2",
        "dependencies": {},
    },
    "send": {
        "version": "1.2.1",
        "dependencies": {
            "ms": "^2.1.3",
            "etag": "^1.8.1",
            "debug": "^4.4.3",
            "fresh": "^2.0.0",
            "statuses": "^2.0.2",
            "encodeurl": "^2.0.0",
            "mime-types": "^3.0.2",
            "escape-html": "^1.0.3",
            "http-errors": "^2.0.1",
            "on-finished": "^2.4.1",
            "range-parser": "^1.2.1",
        },
    },
    "serve-static": {
        "version": "2.2.1",
        "dependencies": {
            "send": "^1.2.0",
            "parseurl": "^1.3.3",
            "encodeurl": "^2.0.0",
            "escape-html": "^1.0.3",
        },
    },
    "setprototypeof": {
        "version": "1.2.0",
        "dependencies": {},
    },
    "shebang-command": {
        "version": "2.0.0",
        "dependencies": {
            "shebang-regex": "^3.0.0",
        },
    },
    "shebang-regex": {
        "version": "4.0.0",
        "dependencies": {},
    },
    "side-channel": {
        "version": "1.1.1",
        "dependencies": {
            "es-errors": "^1.3.0",
            "object-inspect": "^1.13.4",
            "side-channel-map": "^1.0.1",
            "side-channel-list": "^1.0.1",
            "side-channel-weakmap": "^1.0.2",
        },
    },
    "side-channel-list": {
        "version": "1.0.1",
        "dependencies": {
            "es-errors": "^1.3.0",
            "object-inspect": "^1.13.4",
        },
    },
    "side-channel-map": {
        "version": "1.0.1",
        "dependencies": {
            "es-errors": "^1.3.0",
            "call-bound": "^1.0.2",
            "get-intrinsic": "^1.2.5",
            "object-inspect": "^1.13.3",
        },
    },
    "side-channel-weakmap": {
        "version": "1.0.2",
        "dependencies": {
            "es-errors": "^1.3.0",
            "call-bound": "^1.0.2",
            "get-intrinsic": "^1.2.5",
            "object-inspect": "^1.13.3",
            "side-channel-map": "^1.0.1",
        },
    },
    "statuses": {
        "version": "2.0.2",
        "dependencies": {},
    },
    "string-width": {
        "version": "8.3.0",
        "dependencies": {
            "strip-ansi": "^7.1.2",
            "get-east-asian-width": "^1.5.0",
        },
    },
    "strip-ansi": {
        "version": "7.2.0",
        "dependencies": {
            "ansi-regex": "^6.2.2",
        },
    },
    "toidentifier": {
        "version": "1.0.1",
        "dependencies": {},
    },
    "type-check": {
        "version": "0.4.0",
        "dependencies": {
            "prelude-ls": "^1.2.1",
        },
    },
    "type-is": {
        "version": "3.0.0",
        "dependencies": {
            "content-type": "^3.1.1",
        },
    },
    "unicorn-magic": {
        "version": "0.4.1",
        "dependencies": {},
    },
    "update-browserslist-db": {
        "version": "1.3.4",
        "dependencies": {
            "escalade": "^3.2.0",
            "picocolors": "^1.1.1",
        },
    },
    "vary": {
        "version": "1.1.2",
        "dependencies": {},
    },
    "verkit": {
        "version": "0.5.0",
        "dependencies": {},
    },
    "which": {
        "version": "7.0.0",
        "dependencies": {
            "isexe": "^4.0.0",
        },
    },
    "word-wrap": {
        "version": "1.2.5",
        "dependencies": {},
    },
    "wrap-ansi": {
        "version": "10.0.2",
        "dependencies": {
            "ansi-styles": "^6.2.3",
            "string-width": "^8.2.0",
        },
    },
    "wrappy": {
        "version": "1.0.2",
        "dependencies": {},
    },
    "y18n": {
        "version": "5.0.8",
        "dependencies": {},
    },
    "yargs": {
        "version": "18.2.0",
        "dependencies": {
            "y18n": "^5.0.5",
            "cliui": "^9.0.1",
            "escalade": "^3.1.1",
            "string-width": "^8.2.1",
            "yargs-parser": "^22.0.0",
            "get-caller-file": "^2.0.5",
        },
    },
    "yargs-parser": {
        "version": "22.0.0",
        "dependencies": {},
    },
    "yocto-queue": {
        "version": "1.2.2",
        "dependencies": {},
    },
}

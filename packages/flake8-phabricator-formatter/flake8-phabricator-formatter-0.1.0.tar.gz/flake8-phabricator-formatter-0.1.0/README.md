flake8-phabricator-formatter
============================

A simple formatter plugin for [flake8](http://flake8.pycqa.org) that generates
json formatted results suitable for Phabricator's Harbormaster integraton,
according to [this documentation](https://github.com/uber/phabricator-jenkins-plugin/blob/master/docs/advanced.md#custom-lint)

As such, it's mainly dedicated to being used in Jenkins with the
[Phabricator Jenkins Plugin](https://github.com/uber/phabricator-jenkins-plugin).

## Example

```bash

flake8 --format=phabricator
{"context": "def some_stuff(toto):\n", "char": 1, "code": "E302", "line": 3, "name": "flake8", "severity": "error", "path": "sandbox/__init__.py", "description": "expected 2 blank lines, found 1"}
{"context": "  print ('with flake8 errors')\n", "char": 3, "code": "E303", "line": 6, "name": "flake8", "severity": "error", "path": "sandbox/__init__.py", "description": "too many blank lines (2)"}
{"context": "  print ('with flake8 errors')\n", "char": 3, "code": "E111", "line": 6, "name": "flake8", "severity": "error", "path": "sandbox/__init__.py", "description": "indentation is not a multiple of four"}
{"context": "  print ('with flake8 errors')\n", "char": 8, "code": "E211", "line": 6, "name": "flake8", "severity": "error", "path": "sandbox/__init__.py", "description": "whitespace before '('"}
{"context": "  toto = 42\n", "char": 3, "code": "E111", "line": 7, "name": "flake8", "severity": "error", "path": "sandbox/__init__.py", "description": "indentation is not a multiple of four"}
{"context": "  toto = 42\n", "char": 3, "code": "F841", "line": 7, "name": "flake8", "severity": "advice", "path": "sandbox/__init__.py", "description": "local variable 'toto' is assigned to but never used"}
{"context": "  \n", "char": 1, "code": "W293", "line": 8, "name": "flake8", "severity": "warning", "path": "sandbox/__init__.py", "description": "blank line contains whitespace"}

```

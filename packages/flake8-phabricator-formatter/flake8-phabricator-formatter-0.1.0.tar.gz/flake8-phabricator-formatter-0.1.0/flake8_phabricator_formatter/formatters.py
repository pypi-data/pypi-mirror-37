import json
from flake8.formatting import base


class PhabricatorFormatter(base.BaseFormatter):
    """ok"""
    severity = {'E': 'error',
                'W': 'warning',
                }
    def format(self, error):
        filename = error.filename
        if filename.startswith("./"):
            filename = filename[2:]
        errdict = {
            "name": "flake8",
            "path": filename,
            "code": error.code,
            "description": error.text,
            "line": error.line_number,
            "char": error.column_number,
            "severity": self.severity.get(error.code[0], 'advice'),
            "context": error.physical_line,
        }
        return json.dumps(errdict)

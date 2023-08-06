import json
from pathlib import Path
import re


_dir = Path(__file__).parent

with (_dir / 'substitute.json').open() as _f:
    _substitute_table = {
        k: v['substitute'] for k, v in json.load(_f).items()
    }
with (_dir / 'code_skeleton.json').open() as _f:
    _code_skeleton = json.load(_f)

del _f


def substitute(src):
    raw_body = ''.join(
        _substitute_table[ch] for ch in src
        if ch in _substitute_table
    )

    head = '\n'.join(_code_skeleton['head'])
    body = '\n'.join(_code_skeleton['body']).format(code=raw_body)

    placeholder = '_'
    body = f'\n{placeholder} = {placeholder}'.join(
        filter(None, re.split(r'(.{,70}[])])', body))
    )

    return f'{head}\n\n{placeholder} = {body}\n'

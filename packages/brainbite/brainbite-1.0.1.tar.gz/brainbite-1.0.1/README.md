brainbite
===
A python bit my brain, so I sliced up the python into fine strips in retaliation.

## Description
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck) is widely known as an esoteric programming language.
This package enables to write brainfuck-like code in python **legal** grammar.

This package also provides transpilation function from bf code to python one.

## Demo
Though this code is strange, outputs *"Hello World!"* on stdout correctly. 

```python
from brainbite import Biter

_ = Biter()[::...][::...][::...][::...][::...][::...][::...][::...][:...]
_ = _[:...:...][::...][::...][::...][::...][:...][:...:...][::...][::...]
_ = _[:...:...][::...][::...][::...][:...:...][::...][::...][::...]
_ = _[:...:...][::...][...:...][...:...][...:...][...:...][...:][...::...]
_ = _[:...:...][::...][:...:...][::...][:...:...][...:][:...:...][:...:...]
_ = _[::...][:...][...:...][...::...][...:...][...:][...::...][:...:...]
_ = _[:...:...][:][:...:...][...:][...:][...:][:][::...][::...][::...]
_ = _[::...][::...][::...][::...][:][:][::...][::...][::...][:][:...:...]
_ = _[:...:...][:][...:...][...:][:][...:...][:][::...][::...][::...][:]
_ = _[...:][...:][...:][...:][...:][...:][:][...:][...:][...:][...:][...:]
_ = _[...:][...:][...:][:][:...:...][:...:...][::...][:][:...:...][::...]
_ = _[::...][:]()

```

To get this code, run below command.

```bash
$ python -m brainbite sample hello_world
```

**Transpile** \
This module also works as transpiler.
```bash
$ python -m brainbite trans fizzbuzz.bf
```

For more information, view `$ python -m brainbite --help`.

## Install
This module is registered at PyPI. [PyPI - brainbite](https://pypi.org/project/brainbite/)
```bash
$ pip install brainbite
```

## License
[MIT](https://github.com/LouiS0616/brainbite/blob/master/LICENSE)

## Author
[LouiS0616](https://github.com/LouiS0616)

import argparse
from logging import getLogger
from pathlib import Path
import sys

from brainbite.transpiler import transpiler


# References
#   Qiita - Pythonのargparseでサブコマンドを実現する
#   https://qiita.com/oohira/items/308bbd33a77200a35a3d

assert __name__ == '__main__'

_logger = getLogger(__name__)
_dir = Path(__file__).parent


def init_parser():
    parser = argparse.ArgumentParser()
    sub_parser = parser.add_subparsers()

    #
    # sample parser
    sample_parser = sub_parser.add_parser(
        'sample',
        help='you can get some prepared samples. to list up sample, specify -.'
    )
    sample_parser.add_argument(
        'name', help='sample you want to get.'
    )
    sample_parser.add_argument(
        'lang', help='specify lang whether python or brainfuck.',
        nargs='?', default='python',
        choices=['py', 'python', 'bf', 'brainfuck']
    )
    sample_parser.set_defaults(handler=command_sample)

    #
    # trans parser
    trans_parser = sub_parser.add_parser(
        'trans', help='transpile brainfuck code to python one.'
    )
    trans_parser.add_argument(
        'path', help='brainfuck code path what you want to translate. to input from stdin, specify -.'
    )
    trans_parser.set_defaults(handler=command_trans)

    return parser


def command_sample(args):
    if args.name == '-':
        for sample_bf in (_dir / 'sample').glob('*.bf'):
            print(
                sample_bf.stem
            )
        return

    #
    sample_bf = _dir / f'sample/{args.name}.bf'

    if not sample_bf.is_file():
        _logger.warning(
            f'Sample {args.name} is not prepared.'
        )
        return

    bf_code = sample_bf.open().read()

    #
    if args.lang in ('bf', 'brainfuck'):
        sys.stdout.write(bf_code)
    else:
        sys.stdout.write(
            transpiler.substitute(bf_code)
        )


def command_trans(args):
    if args.path == '-':
        src = sys.stdin.read()
    else:
        path = Path(args.path)

        if not path.is_file():
            _logger.warning(
                f'File {args.path} is not found.'
            )
            return

        src = path.open().read()

    sys.stdout.write(
        transpiler.substitute(src)
    )


def main():
    parser = init_parser()

    args = parser.parse_args()
    if hasattr(args, 'handler'):
        args.handler(args)
    else:
        parser.print_help()


main()

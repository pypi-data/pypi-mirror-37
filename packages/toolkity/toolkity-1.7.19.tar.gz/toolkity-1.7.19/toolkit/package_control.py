import re
import os

from functools import partial
from argparse import ArgumentParser


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    mth = re.search(r"__version__\s?=\s?['\"]([^'\"]+)['\"]", init_py)
    if mth:
        return mth.group(1)
    else:
        raise RuntimeError("Cannot find version!")


def install_requires():
    """
    Return requires in requirements.txt
    :return:
    """
    try:
        with open("requirements.txt") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    except OSError:
        return []


def change_version(index=None, dev=False):

    if not index:
        parser = ArgumentParser()
        parser.add_argument("-i", "--index", type=int, help="版本顺位", default=3)
        parser.add_argument("-d", "--dev", action="store_true", help="是否是开发模式")
        args = parser.parse_args()
        index = args.index
        dev = args.dev

    package = os.path.basename(os.path.abspath(os.getcwd())).replace("-", "_")
    with open(os.path.join(package, '__init__.py'), "r+", encoding="utf-8") as f:
        init_py = f.read()
        f.seek(0)
        buf = re.sub(
            r"(__version__\s?=\s?['\"])([^'\"]+)(['\"])",
            partial(_repl, index=int(index), dev=dev), init_py)
        f.write(buf)


def _repl(mth, index, dev):
    versions = mth.group(2).split(".")
    vs = versions[index-1]
    blank = ""
    if dev:
        if vs.isdigit():
            versions[index - 1] = str(int(vs) + 1) + "dev1"
        else:
            for i in range(len(vs)-1, -1, -1):
                if not vs[i].isdigit():
                    last = vs[i+1:]
                    break
            else:
                last = ""

            if last == "":
                raise RuntimeError("Invalid version")

            versions[index - 1] = vs[:i+1] + str(int(last) + 1)
    else:
        if vs.isdigit():
            versions[index - 1] = str(int(vs) + 1)
        else:
            for i in range(0, len(vs)):
                if not vs[i].isdigit():
                    first = vs[:i]
                    break
            else:
                 first = vs

            if first == "":
                raise RuntimeError("Invalid version")

            versions[index - 1] = first
            blank = (len(vs) - len(first)) * " "

    return mth.group(1) + ".".join(versions) + mth.group(3) + blank
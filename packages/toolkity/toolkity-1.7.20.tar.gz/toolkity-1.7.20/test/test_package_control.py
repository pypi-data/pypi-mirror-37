import pytest

from toolkit.package_control import change_version


def test_version1():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("___version__ = '0.1.1'\n\n# 测试")

    change_version(3)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "___version__ = '0.1.2'\n\n# 测试"


def test_version2():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(2)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.2.1'\n\n# 测试"


def test_version3():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(1)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '1.1.1'\n\n# 测试"


def test_version4():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d1'\n\n# 测试")

    change_version(3, True)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1d2'\n\n# 测试"


def test_version5():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d'\n\n# 测试")
    with pytest.raises(RuntimeError):
        change_version(3, True)


def test_version6():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1'\n\n# 测试")

    change_version(3, True)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.2dev1'\n\n# 测试"


def test_version7():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d2'\n\n# 测试")

    change_version(3)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1'  \n\n# 测试"


def test_version8():
    with open("test/__init__.py", "w", encoding="utf-8") as f:
        f.write("import abc\n___version__ = '0.1.1d19'\n\n# 测试")

    change_version(3, True)

    with open("test/__init__.py", encoding="utf-8") as f:
        assert f.read() == "import abc\n___version__ = '0.1.1d20'\n\n# 测试"



if __name__ == "__main__":
    pytest.main(["test_package_control.py"])

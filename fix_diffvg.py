import os
import re
import sys
from itertools import filterfalse


def disable_tensorflow_build():
    """Disable tensorflow build in diffvg's CMakeLists.txt"""
    with open('diffvg/CMakeLists.txt', 'r') as f:
        cmake_lists = f.read()
    with open('diffvg/CMakeLists.txt', 'w') as f:
        f.write(
            cmake_lists
            .replace("find_package(TensorFlow)", "# find_package(TensorFlow)")
            .replace("if(TensorFlow_FOUND)", "if(0)")
        )
    print("Done")


def fix_pydiffvg_import():
    """Fix pydiffvg import"""
    use_path = None
    found_diffvg = False
    for import_path in sys.path:
        if re.fullmatch(r"/usr/local/lib/python[\d\.]*/dist-packages", import_path):
            for p in filterfalse(
                lambda x: not x.startswith('d'), os.listdir(import_path)
            ):
                if p[:6] == "diffvg":
                    use_path = os.path.join(import_path, p)
                    found_diffvg = True
                    break
            else:
                continue
        if found_diffvg:
            break

    if not found_diffvg:
        raise Exception(
            "Could not find diffvg package. try re-build diffvg.\n\n"
            "If you add the path manually, "
            "you can add the path of the lines starting with \"Installed\" "
            "in the diffvg build log to `sys.path` to make it work."
        )

    if use_path not in sys.path:
        sys.path.append(use_path)
        print("Added path:", use_path)
    else:
        print("Path already exists:", use_path)


if __name__ == '__main__':
    disable_tensorflow_build()

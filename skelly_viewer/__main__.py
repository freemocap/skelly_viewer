# __main__.py
import sys
from pathlib import Path

from skelly_viewer.gui.qt.skellyview_main_window import main

base_package_path = Path(__file__).parent.parent
print(f"adding base_package_path: {base_package_path} : to sys.path")
sys.path.insert(0, str(base_package_path))  # add parent directory to sys.path


if __name__ == "__main__":
    main()

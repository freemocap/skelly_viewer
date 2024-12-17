# __main__.py

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="SkellyViewer")
    return parser.parse_args()

def run():
    parse_args()

    from skelly_viewer.gui.qt.skellyview_main_window import main
    main()

if __name__ == "__main__":
    run()

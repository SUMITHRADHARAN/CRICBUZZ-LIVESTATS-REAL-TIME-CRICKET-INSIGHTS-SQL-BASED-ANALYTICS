# utils/path_setup.py
import sys
import os

# Always add project root (parent of "pages" and "utils") to sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/.."
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

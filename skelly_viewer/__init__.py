"""Top-level package for basic_template_repo."""

__package_name__ = "skelly_viewer"
__version__ = "v2024.08.1025"

__author__ = """Skelly FreeMoCap"""
__email__ = "info@freemocap.org"
__repo_owner_github_user_name__ = "freemocap"
__repo_url__ = f"https://github.com/{__repo_owner_github_user_name__}/{__package_name__}/"
__repo_issues_url__ = f"{__repo_url__}issues"

print(f"Thank you for using {__package_name__}!")
print(f"This is printing from: {__file__}")
print(f"Source code for this package is available at: {__repo_url__}")

from skelly_viewer.config.default_paths import get_log_file_path
from skelly_viewer.config.logging_configuration import configure_logging
from skelly_viewer.gui.qt.skelly_viewer_widget import SkellyViewer

configure_logging(log_file_path=get_log_file_path())

"""Default Contacts settings."""

import os

PLUGIN_BASE_DIR = os.path.dirname(__file__)

CONTACTS_STATS_FILES = {
    "dev": os.path.join(
        PLUGIN_BASE_DIR, "../frontend/webpack-stats.json"),
    "prod": os.path.join(
        PLUGIN_BASE_DIR, "static/modoboa_contacts/webpack-stats.json")
}


def apply(settings):
    """Modify settings."""
    DEBUG = settings["DEBUG"]
    if "webpack_loader" not in settings["INSTALLED_APPS"]:
        settings["INSTALLED_APPS"] += ("webpack_loader", )
    wpl_config = {
        "CONTACTS": {
            "CACHE": not DEBUG,
            "BUNDLE_DIR_NAME": "modoboa_radicale/",
            "STATS_FILE": CONTACTS_STATS_FILES.get("dev" if DEBUG else "prod"),
            "IGNORE": [".+\.hot-update.js", ".+\.map"]
        }
    }
    if "WEBPACK_LOADER" in settings:
        settings["WEBPACK_LOADER"].update(wpl_config)
    else:
        settings["WEBPACK_LOADER"] = wpl_config

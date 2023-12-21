from PyInstaller.utils.hooks import collect_data_files

module_collection_mode = "py+pyz"
hiddenimports = [
    "branch.cli.init",
    "branch.cli.produce",
    "branch.cli.consume",
    "branch.cli.topics",
    "branch.cli.server",
    "branch.cli.server.start",
    "branch.cli.tui",
]
datas = collect_data_files("branch")

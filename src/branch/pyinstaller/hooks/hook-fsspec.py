from PyInstaller.utils.hooks import collect_data_files

module_collection_mode = "py+pyz"
hiddenimports = [
    "gcsfs",
]
datas = collect_data_files("fsspec")

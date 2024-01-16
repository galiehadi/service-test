import os
"""
Setting parameter untuk koneksi ke database.
"""
__version__ = 'v1.6'

_USER_ = os.environ.get("DB_USER", "toor")  # set username untuk akses DB
_PASS_ = os.environ.get("DB_PASSWORD", "P@ssw0rd")  # set password user untuk akses DB
_IP_ = os.environ.get("DB_HOST", "127.0.0.1")  # set koneksi ip database (default: 127.0.0.1)
_PORT_ = int(os.environ.get("DB_PORT", "3306"))  # set port database MySQL (default: 3306)
_DB_NAME_ = os.environ.get("DB_NAME", "menu")  # set nama database
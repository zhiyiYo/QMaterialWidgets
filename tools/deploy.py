import os

os.system('nuitka --standalone --windows-disable-console --enable-plugin=pyside6 --mingw64 --show-memory --show-progress --windows-icon-from-ico=docs/source/_static/logo.ico demo.py')

"""
Pyinstaller will not make an executable out of a package, so this is the workaround.
For more info see https://github.com/pyinstaller/pyinstaller/issues/2560
"""

from client.__main__ import main

main()

#!c:\users\tom\pycharmprojects\django_blog\blog_venv\scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'Pigments==1.6','console_scripts','pygmentize'
__requires__ = 'Pigments==1.6'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Pigments==1.6', 'console_scripts', 'pygmentize')()
    )

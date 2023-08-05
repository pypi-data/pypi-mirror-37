import os

import django
from django.conf import settings

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Manual setup is required for standalone Django usage
# NOTE: Since documentation is built using the built/installed package when
# using Tox, it can't use the 'test.settings' Django settings module.
settings.configure(
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.staticfiles',
        'rest_framework',
        'guardian',
        'mathfilters',
        'versionfield',
        'resolwe',
        'resolwe.permissions',
        'resolwe.flow',
        'resolwe.elastic',
    ),
)
django.setup()

# Get package metadata from 'resolwe/__about__.py' file
about = {}
with open(os.path.join(base_dir, 'resolwe', '__about__.py')) as f:
    exec(f.read(), about)

# -- General configuration ------------------------------------------------

# The extension modules to enable.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.intersphinx',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
]

# The suffix(es) of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Resolwe'
version = about['__version__']
release = version
author = about['__author__']
copyright = about['__copyright__']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# Warn about all references where the target cannot be found
nitpicky = True
# Except for the following:
nitpick_ignore = [
    # This is needed to prevent warnings for container types, e.g.:
    # :type foo: tuple(bool, str)
    ('py:obj', ''),
]

# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

# Output file base name for HTML help builder.
htmlhelp_basename = 'Resolwedoc'

# Configuration for intersphinx
_django_major_version = "{}.{}".format(*django.VERSION[:2])
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/{}/'.format(_django_major_version),
               'https://docs.djangoproject.com/en/{}/_objects/'.format(_django_major_version)),
}

# Configuration for extlinks
extlinks = {
    'drf': ('http://www.django-rest-framework.org/api-guide/%s', ''),
}

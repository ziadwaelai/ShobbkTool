from setuptools import setup
import os


# pip install py2app
# python setup.py py2app


APP = ['main.py']
DATA_FILES = [
    ('assets', ['assets/logo.png', 'assets/icon.png']),
]
OPTIONS = {
    'argv_emulation': True,
    'packages': [
        'skimage',
        'transformers.pipelines',
        'transformers.dynamic_module_utils',
        'transformers.image_utils',
        'transformers.utils',
    ],
    'excludes': [
        'matplotlib',
        'tkinter',
        'rembg',
    ],
    # 'iconfile': os.path.join(os.getcwd(), 'assets\icon.icns'),  # Specify your icon path in .icns format
    'optimize': 1,
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

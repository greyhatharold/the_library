from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['customtkinter'],
    'iconfile': 'path/to/your/icon.icns',  # Replace with the path to your app icon
    'plist': {
        'CFBundleName': 'The Library',
        'CFBundleDisplayName': 'The Library',
        'CFBundleGetInfoString': "The Library Application",
        'CFBundleIdentifier': "com.yourdomain.TheLibrary",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2023, Your Name, All Rights Reserved"
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
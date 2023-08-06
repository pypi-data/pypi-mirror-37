# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['vidl']

package_data = \
{'': ['*']}

install_requires = \
['colorama>=0.3.9,<0.4.0',
 'colorboy>=1.0.1,<2.0.0',
 'deep-filter>=1.0,<2.0',
 'mutagen>=1.41,<2.0',
 'youtube-dl>=2018.9,<2019.0']

entry_points = \
{'console_scripts': ['vidl = vidl.app:main']}

setup_kwargs = {
    'name': 'vidl',
    'version': '3.2.1',
    'description': 'Python script to download video/audio, built with youtube-dl',
    'long_description': '# vidl\nvidl is a script designed to easily download video/audio from anywere, using youtube-dl. It automatically embeds thumbnails to mp3/mp4/m4a files.\n\nvidl will add metadata to mp3 files if it\'s found. The `--no-md` option turns this off.\n`title`, `artist` and `year` metadata is added, but if the URL is a playlist, it also adds `album`, `album artist`, `track number`, `track count`.\nIf the title contains " - ", vidl often uses what comes before and after it as artist and title respectively. The `--dont-extract-md` option turns off this behaviour.\n\n# Installation\n1. Install Python (3.7 is recommended)\n2. Install [ffmpeg and ffprobe](https://www.ffmpeg.org/)\n3. Run `pip install vidl`\n4. If you\'re not on macOS or Windows, you need to specify where vidl will download files to by running `vidl config download_folder \'<path>\'`.\nIf you\'re on macOS, I strongly recommend [setting up shortcuts for vidl](#macos-shortcut-setup)\n\n# Usage\nExamples:\n`vidl https://www.youtube.com/watch?v=ta_ZVS7HkwI`\n- Downloads the video as mp3, and adds metadata it detects.\n\n`vidl mp3 https://www.youtube.com/watch?v=ta_ZVS7HkwI --no-md`\n- Downloads the video as mp3, without adding metadata.\n\n`vidl config download_folder "~/Downloads"`\n- Set the folder that vidl downloads to `~/Downloads`.\n\n`vidl`\n- Prints vidl\'s help menu, which looks like this:\n    ```\n    Usage:\n        vidl [format] [options] <URL>\n\n    Options:\n        format             mp3, mp4, wav or m4a. Default mp3.\n        --no-md            Don\'t add metadata to downloaded files.\n        --no-smart-md      Don\'t extract artist and song name from title.\n        --no-dl            Don\'t download anything.\n        -v, --verbose      Display all logs.\n        --version          Display vidl version. "vidl -v" also works.\n        -h, --help         Display this help message.\n\n    Configuration:\n        vidl config <key> [new_value]\n\n    Available Configs:\n        download_folder    The folder that vidl downloads to.\n        output_template    youtube-dl output template.\n    ```\n\n# <a name="#macos-shortcut-setup"></a>Set up shortcuts for vidl (macOS)\nYou\'ll be able to select any piece of text, press your chosen shortcut and the link(s) in your selected text will be downloaded! A little tedious to set up, but well worth it.\n\nFirst, we need to create a macOS Service:\n1. Open the Automator app.\n2. Choose File > New, and select Service.\n3. (TLDR; Add `Run Shell Script`) In the window that just popped up, there are two columns on the left (if not, click the `Library` button in the status bar). Select `Utilities` in the first column, and in the second column, drag `Run Shell Script` into the main part of the window.\n4. Make your settings match these:\n    \n    ![Service receives selected [URLs] in [any application]. Input is [only URLs]. In your Run Shell Script box; Shell: [/bin/bash]. Pass input: [as arguments]](https://raw.githubusercontent.com/SpectralKH/vidl/master/macos-service-screenshot.png)\n    \n    If you want the shortcut to only work in one app, select that app instead of `any application`.\n5. In the text box in the "Run Shell Script" box, paste in the following script:\n    ```bash\n    for f in "$@"\n    do\n        # AppleScript doesn\'t look for scripts in the same places as the terminal,\n        # so we need to make it look in the proper folders.\n        export PATH=<VIDL_DIR>:$PATH\n        export PATH=<FFMPEG_DIR>:$PATH\n        export PATH=<FFPROBE_DIR>:$PATH\n        vidl --quiet "$f"\n    done\n    ```\n    Replace `<VIDL_DIR>` with the path you get from running `dirname $(which vidl)` in the terminal.\n    Replace `<FFMPEG_DIR>` with the path you get from running `dirname $(which ffmpeg)` in the terminal.\n    Replace `<FFPROBE_DIR>` with the path you get from running `dirname $(which ffprobe)` in the terminal.\n6. Choose File > Save. Type in vidl.\n\nAlmost done, you just need to tie a shortcut to the macOS Service you just created:\n1. Open the System Preferences app.\n2. Go to Keyboard and select the Shortcuts tab.\n3. Select Services from the left column, and locate vidl (should be under Internet). Add your preferred shortcut.\n\n# Dev Instructions\n### Installation\n1. Install Python (3.7 is recommended)\n2. Install [ffmpeg and ffprobe](https://www.ffmpeg.org/)\n3. Install [Poetry](https://poetry.eustace.io)\n4. Run `poetry install` to install Python package dependencies.\n4. Make sure your `download_path` is set in `vidl/config.json`.\n\nI recommend running `poetry config settings.virtualenvs.in-project true`. This command makes Poetry create your Python virtual environment inside the project folder, so you\'ll be able to easily delete it. Additionally, it lets VSCode\'s Python extension detect the virtual environment if you set the `python.pythonPath` setting to `${workspaceFolder}/.venv/bin/python` in your workspace (or global) settings.\n\n### Running\nRun `poetry run python vidl`.\n\nTo test the package, you can run `poetry develop`. This adds the `vidl` package itself to the virtual environment, including the CLI executable. This means you can simply type `poetry run vidl`.\n\nAs an alternative to `poetry run <command>`, you can run `poetry shell` to enter the virtual environment\'s bash CLI, and then run your command on it\'s own.\n\n# ToDo\n- For future config possibilities, replace options like `--no-md` with `--md` and `--!md`. Maybe call it `defaults` instead of `config`?\n    - Add all configs as options, for instance add download_folder option.\n    - Add all options as configs, for instance add md option. \n    - Add config/option for individual metadata\n- Allow passing youtube-dl arguments directly\n',
    'author': 'KH',
    'author_email': 'kasperkh.kh@gmail.com',
    'url': 'https://vidl.kasp.io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.2,<4.0',
}


setup(**setup_kwargs)

import os


DOCUMENTS_DIR = os.path.expanduser('~/Documents')

MY_GAMES_DIR = os.path.join(DOCUMENTS_DIR, 'My Games')
FARMING_SM22_DIR = os.path.join(MY_GAMES_DIR, 'FarmingSimulator2022')

if all(map(os.path.isdir, [MY_GAMES_DIR, FARMING_SM22_DIR])):

    SAVE_GAMES = [file for file in os.listdir(FARMING_SM22_DIR) if file.startswith('savegame') and file != 'savegameBackup']
    print(SAVE_GAMES)
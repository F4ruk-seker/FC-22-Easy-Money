import xml.etree.ElementTree as ET
from pathlib import Path
import os


DOCUMENTS_DIR = os.path.expanduser('~/Documents')

MY_GAMES_DIR = os.path.join(DOCUMENTS_DIR, 'My Games')
FARMING_SM22_DIR = os.path.join(MY_GAMES_DIR, 'FarmingSimulator2022')

if all(map(os.path.isdir, [MY_GAMES_DIR, FARMING_SM22_DIR])):
    for file in os.listdir(FARMING_SM22_DIR):
        if file.startswith('savegame') and file != 'savegameBackup':

            tree = ET.parse(os.path.join(os.path.join(FARMING_SM22_DIR, file), 'farms.xml'))
            root = tree.getroot()

            for farm in root.findall('farm'):
                print(f'Para : {farm.get('money')} {farm.get('name')} {farm.get('farmId')}')

            tree = ET.parse(os.path.join(os.path.join(FARMING_SM22_DIR, file), 'careerSavegame.xml'))
            root = tree.getroot()

            # İlgili bilgileri almak için
            map_title = root.find('.//settings/mapTitle').text
            savegame_name = root.find('.//settings/savegameName').text
            save_date = root.find('.//settings/saveDate').text
            money = root.find('.//statistics/money').text

            # Bilgileri ekrana yazdır
            print("Map Title:", map_title)
            print("Savegame Name:", savegame_name)
            print("Save Date:", save_date)
            print("Money:", money)

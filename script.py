import xml.etree.ElementTree as ET
from pathlib import Path
import os


DOCUMENTS_DIR: Path = Path(os.path.expanduser('~/Documents')).resolve()

MY_GAMES_DIR: Path = DOCUMENTS_DIR / 'My Games'
FARMING_SM22_DIR: Path = MY_GAMES_DIR / 'FarmingSimulator2022'

career_file_name: str = 'careerSavegame.xml'
farm_file_name: str = 'farms.xml'


def get_farm_career_info(xml_dir: Path) -> dict | None:
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        return {
            'map_title': root.find('.//settings/mapTitle').text,
            'savegame_name': root.find('.//settings/savegameName').text,
            'save_date': root.find('.//settings/saveDate').text,
            'money': root.find('.//statistics/money').text,
        }
    return {
        'ERROR': f'dizinde kayıt dosyasına ulaşılamadı\n'
                 f'dizin: {xml_dir}\n'
                 f'aranan dosya: careerSavegame.xml\n'
    }


def update_farm_career_file_money(xml_dir: Path, new_money: int) -> None:
    ...


def update_farm_file_money(xml_dir: Path, new_money: str) -> None:
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        for farm in root.findall('farm'):
            farm.set('money', new_money)


if all(map(os.path.isdir, [MY_GAMES_DIR, FARMING_SM22_DIR])):
    farm_counter: int = 0
    for file in os.listdir(FARMING_SM22_DIR):
        if file.startswith('savegame') and file != 'savegameBackup':
            save_dir = FARMING_SM22_DIR / file
            farm_counter += 1

            print(f'Seçim id: ({file.replace('savegame', '')}) | Farm => ')
            for k, v in get_farm_career_info(save_dir / 'careerSavegame.xml').items():
                print(f'{k}: {v}')
            print(f'{farm_counter}.Farm => END {'*'*50}')

            # select = int(input('seçim id ile gösterilen parantez içersindeki sayıyı girin :'))

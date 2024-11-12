import xml.etree.ElementTree as ET
from pathlib import Path
from streamlit.logger import get_logger
import streamlit as st
import os
from model import FarmInfoModel

LOGGER = get_logger(__name__)


DOCUMENTS_DIR: Path = Path(os.path.expanduser('~/Documents')).resolve()

MY_GAMES_DIR: Path = DOCUMENTS_DIR / 'My Games'
FARMING_SM22_DIR: Path = MY_GAMES_DIR / 'FarmingSimulator2022'
print(FARMING_SM22_DIR)
career_file_name: str = 'careerSavegame.xml'
farm_file_name: str = 'farms.xml'


def get_farm_career_info(xml_dir: Path) -> dict | FarmInfoModel:
    tree = ET.parse(xml_dir)
    root = tree.getroot()

    return FarmInfoModel(
        map_title=root.find('.//settings/mapTitle').text,
        savegame_name=root.find('.//settings/savegameName').text,
        save_date=root.find('.//settings/saveDate').text,
        money=root.find('.//statistics/money').text
    )


def get_farms(save_dir):
    for file in os.listdir(save_dir):
        if file.startswith('savegame') and file != 'savegameBackup':
            save_dir = FARMING_SM22_DIR / file
            if os.path.isfile(save_dir / career_file_name):
                yield get_farm_career_info(save_dir / career_file_name)



def run():
    st.set_page_config(
        page_title="Farm Editör",
        page_icon="👋",
        initial_sidebar_state='collapsed'
    )

    selected_farming_sm22_dir: str = st.text_input(
        label='Select Save Dir',
        placeholder='Oyunun save Dosyaları nerede',
        value=FARMING_SM22_DIR
    )

    st.write("## Köy seçiniz! 👋")
    farms = list(get_farms(selected_farming_sm22_dir))
    sc = st.selectbox(
        label=' ',
        options=[f'{index + 1}. {farm.savegame_name}' for farm, index in zip(farms, range(len(farms)))],
        label_visibility='hidden'
    )

    selected_farm: FarmInfoModel = farms[int(sc.split('.')[0]) - 1]

    st.write(f'### Selcted Farm; {selected_farm.savegame_name} | {selected_farm.map_title} ')

    if selected_farm.map_title in ('Haut-Beyleron', 'Elmcreek', 'Erlengrat'):
        st.image(f'images/{selected_farm.map_title}.webp')
    print(selected_farm.save_date)
    new_farm_name = st.text_input(label='Farm Name : ', value=selected_farm.savegame_name)
    new_farm_money = st.number_input(label='Farm Money', value=int(selected_farm.money))
    st.text_input(label='Farm Last Update', value=selected_farm.save_date, disabled=True)

    st.button('Save')


if __name__ == "__main__":
    run()


"""
{'map_title': 'Haut-Beyleron', 'savegame_name': 'Kayıtlı Oyunlarım', 'save_date': '2024-10-29', 'money': '99999500'}
Para: 99999500
{'ERROR': 'dizinde kayıt dosyasına ulaşılamadı\ndizin: C:\\Users\\seker\\Documents\\My Games\\FarmingSimulator2022\\savegame2\\careerSavegame.xml\naranan dosya: careerSavegame.xml\n'}
{'map_title': 'Elmcreek', 'savegame_name': 'Kayıtlı Oyunlarım', 'save_date': '2024-11-12', 'money': '79070812'}
"""
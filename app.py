import xml.etree.ElementTree as ET
from pathlib import Path
from streamlit.logger import get_logger
import streamlit as st
import os
from model import FarmInfoModel
from langs.lang import Lang


LOGGER = get_logger(__name__)


DOCUMENTS_DIR: Path = Path(os.path.expanduser('~/Documents')).resolve()

MY_GAMES_DIR: Path = DOCUMENTS_DIR / 'My Games'
FARMING_SM22_DIR: Path = MY_GAMES_DIR / 'FarmingSimulator2022'
career_file_name: str = 'careerSavegame.xml'
farm_file_name: str = 'farms.xml'


def get_farm_career_info(xml_dir: Path) -> dict | FarmInfoModel:
    tree = ET.parse(xml_dir)
    root = tree.getroot()

    return FarmInfoModel(
        map_title=root.find('.//settings/mapTitle').text,
        savegame_name=root.find('.//settings/savegameName').text,
        save_date=root.find('.//settings/saveDate').text,
        money=root.find('.//statistics/money').text,
        save_dir=str(xml_dir).replace('careerSavegame.xml', '')
    )


def get_farms(save_dir):
    for file in os.listdir(save_dir):
        if file.startswith('savegame') and file != 'savegameBackup':
            save_dir = FARMING_SM22_DIR / file
            if os.path.isfile(save_dir / career_file_name):
                yield get_farm_career_info(save_dir / career_file_name)


def update_farm_career_file_money(xml_dir: Path, new_money: str) -> None:
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        money_element = root.find('./statistics/money')
        if money_element is not None:
            money_element.text = new_money
            tree.write(xml_dir)


def update_farm_file_money(xml_dir: Path, new_money: str) -> None:
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        for farm in root.findall('farm'):
            farm.set('money', new_money)
        tree.write(xml_dir)


def save(save_dir: Path | str, new_money: str):
    if type(save_dir) is not Path:
        save_dir = Path(save_dir).resolve()
    update_farm_file_money(save_dir / farm_file_name, new_money)
    update_farm_career_file_money(save_dir / career_file_name, new_money)

    st.dialog('Changed')


def get_langs() -> list[str]:
    # Lang.load(f'langs/{langs.replace('.json', '')}') for langs in os.listdir('langs') if langs.endswith('.json')
    return [lang.replace('.json', '') for lang in os.listdir('langs') if lang.endswith('.json')]


def load_lang(selected_language) -> Lang:
    return Lang.load(f'langs/{selected_language}')


def run():

    st.set_page_config(
        page_title="Farm Editör",
        page_icon="👋",
        initial_sidebar_state='collapsed',
        # layout="wide"
    )

    langs = get_langs()
    selected_language = st.selectbox(
        label='Select Language',
        options=[f'{lang.upper()}' for lang, index in zip(langs, range(len(langs)))],
    )

    lang = load_lang(selected_language.strip().lower())

    st.write(f'langis {lang.lang_name}')
    selected_farming_sm22_dir: str = st.text_input(
        label=lang.select_save_dir,
        placeholder=lang.select_save_placeholder,
        value=FARMING_SM22_DIR
    )

    st.write(f"## {lang.select_farm}")

    farms = list(get_farms(selected_farming_sm22_dir))
    sc = st.selectbox(
        label='select farm ',
        options=[f'{index + 1}. {farm.savegame_name}' for farm, index in zip(farms, range(len(farms)))],
        label_visibility='hidden'
    )

    selected_farm: FarmInfoModel = farms[int(sc.split('.')[0]) - 1]

    st.write(f'### {lang.selected_farm} :')
    st.write(f'{lang.save_name} : {selected_farm.savegame_name}')
    st.write(f'{lang.map} : {selected_farm.map_title}')

    map_img = selected_farm.map_title if selected_farm.map_title in ('Haut-Beyleron', 'Elmcreek', 'Erlengrat') else 'u'

    st.image(f'images/{map_img}.webp')

    new_farm_name = st.text_input(label=f'{lang.farm_name} : ', value=selected_farm.savegame_name)
    new_farm_money = st.number_input(label=f'{lang.farm_money} : ', value=int(selected_farm.money))

    st.text_input(label=lang.farm_last_save_date, value=selected_farm.save_date, disabled=True)

    st.button(lang.save, on_click=save(save_dir=selected_farm.save_dir, new_money=str(new_farm_money)))


if __name__ == "__main__":
    run()

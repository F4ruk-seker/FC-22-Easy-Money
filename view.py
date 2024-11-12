import os
from pathlib import Path
import streamlit as st
from streamlit.logger import get_logger
import xml.etree.ElementTree as ET


LOGGER = get_logger(__name__)


DOCUMENTS_DIR: Path = Path(os.path.expanduser('~/Documents')).resolve()

MY_GAMES_DIR: Path = DOCUMENTS_DIR / 'My Games'
FARMING_SM22_DIR: Path = MY_GAMES_DIR / 'FarmingSimulator2022'

career_file_name: str = 'careerSavegame.xml'
farm_file_name: str = 'farms.xml'


"""
{'map_title': 'Haut-Beyleron', 'savegame_name': 'Kayıtlı Oyunlarım', 'save_date': '2024-10-29', 'money': '99999500'}
Para: 99999500
{'ERROR': 'dizinde kayıt dosyasına ulaşılamadı\ndizin: C:\\Users\\seker\\Documents\\My Games\\FarmingSimulator2022\\savegame2\\careerSavegame.xml\naranan dosya: careerSavegame.xml\n'}
{'map_title': 'Elmcreek', 'savegame_name': 'Kayıtlı Oyunlarım', 'save_date': '2024-11-12', 'money': '79070812'}
"""

# st.write('hello bitchs')

def run():
    st.set_page_config(
        page_title="Hello",
        page_icon="👋",
    )
    st.text_input(
        placeholder='köy dizini',
        value=''
    )
    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()

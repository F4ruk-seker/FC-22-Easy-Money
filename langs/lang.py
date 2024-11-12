from dataclasses import dataclass
import json


@dataclass(frozen=True)
class Lang:
    lang_name: str
    lang_code: str
    page_title: str
    select_save_dir: str
    select_save_placeholder: str
    select_default_dir: str
    select_farm: str
    selected_farm: str
    farm_name: str
    farm_money: str
    farm_last_save_date: str
    save: str
    save_name: str
    map: str

    @classmethod
    def load(cls, lang: str = 'eng-us'):
        with open(f'{lang}.json', 'r', encoding='utf-8') as lang_file:
            data = json.loads(lang_file.read())
            return cls(**data)

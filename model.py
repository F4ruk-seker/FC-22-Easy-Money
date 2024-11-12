from dataclasses import dataclass


@dataclass
class FarmInfoModel:
    map_title: str | None = None
    savegame_name: str | None = None
    save_date: str | None = None
    money: int | None = None

import xml.etree.ElementTree as ET
from pathlib import Path
import os
import tkinter as tk
from tkinter import messagebox


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


def update_farm_career_file_money(xml_dir: Path, new_money: str) -> None:
    print(f'os.path.isfile: {os.path.isfile(xml_dir)}, p> {xml_dir}')
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        money_element = root.find('./statistics/money')
        if money_element is not None:
            money_element.text = new_money
            tree.write(xml_dir)
            print("Para başarıyla güncellendi!")
        else:
            print("Para bilgisi bulunamadı.")
    else:
        print(f"{xml_dir} dosyası bulunamadı.")


def update_farm_file_money(xml_dir: Path, new_money: str) -> None:
    if os.path.isfile(xml_dir):
        tree = ET.parse(xml_dir)
        root = tree.getroot()
        for farm in root.findall('farm'):
            farm.set('money', new_money)
        tree.write(xml_dir)
        messagebox.showinfo("Başarılı", "Para güncellendi!")

#
# if all(map(os.path.isdir, [MY_GAMES_DIR, FARMING_SM22_DIR])):
#     farm_counter: int = 0
#     for file in os.listdir(FARMING_SM22_DIR):
#         if file.startswith('savegame') and file != 'savegameBackup':
#             save_dir = FARMING_SM22_DIR / file
#             farm_counter += 1
#
#             print(f'Seçim id: ({file.replace('savegame', '')}) | Farm => ')
#             for k, v in get_farm_career_info(save_dir / 'careerSavegame.xml').items():
#                 print(f'{k}: {v}')
#             print(f'{farm_counter}.Farm => END {'*'*50}')
#
#             select = int(input('seçim id ile gösterilen parantez içersindeki sayıyı girin :'))

def show_farms():
    farm_counter = 0
    for file in os.listdir(FARMING_SM22_DIR):
        if file.startswith('savegame') and file != 'savegameBackup':
            save_dir = FARMING_SM22_DIR / file
            farm_info = get_farm_career_info(save_dir / career_file_name)
            if 'ERROR' not in farm_info:
                farm_counter += 1
                farm_frame = tk.Frame(window)
                farm_frame.pack(pady=10)
                print(f"Para: {farm_info['money']}")
                tk.Label(farm_frame, text=f"Çiftlik {farm_counter}").pack()
                tk.Label(farm_frame, text=f"Harita Başlığı: {farm_info['map_title']}").pack()
                tk.Label(farm_frame, text=f"Kayıt Adı: {farm_info['savegame_name']}").pack()
                tk.Label(farm_frame, text=f"Kayıt Tarihi: {farm_info['save_date']}").pack()
                tk.Label(farm_frame, text=f"Para: {farm_info['money']}").pack()

                money_entry = tk.Entry(farm_frame)
                money_entry.pack()
                tk.Button(farm_frame, text="Parayı Güncelle",
                          command=lambda entry=money_entry:
                          [
                            update_farm_file_money(save_dir / farm_file_name, entry.get()),
                            update_farm_career_file_money(save_dir / career_file_name, entry.get())
                          ]
                          ).pack()


window = tk.Tk()
window.title("Çiftlik Bilgileri ve Para Güncelleme")

if all(map(os.path.isdir, [MY_GAMES_DIR, FARMING_SM22_DIR])):
    show_farms()
else:
    tk.Label(window, text="Gerekli dizinler bulunamadı!").pack()

window.mainloop()

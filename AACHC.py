import os
import shutil

def clear_directory(directory_path):
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Удалён файл: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Удалена директория: {file_path}")

def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Директория '{directory_path}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")

def read_achievements_data():
    content = []
    with open('AACHC_in.txt', "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                
                if len(parts) != 4:  # Изменено с 5 на 4
                    print('Ошибка количества подаваемых данных в строке ' + str(parts))
                    os._exit(0)

                current_entry = []
                for part in parts:
                    if part != parts[0] and part != parts[3]:  # Обновлены индексы
                        part = part.replace("_", " ")
                    part = part.replace("name=", "").replace("descr=", "").replace("trigger=", "")  # Удален xp=
                    current_entry.append(part)
                
                content.append(current_entry)
    return content

def create_achievements_core_file():
    with open('output/core_parts_NAP/achievements_core.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это функция анализа достижений. Автозапуск каждые 20tcs (1 сек) функцией 20ticks.mcfunction\n\n')
        for inner_list in achievements_data:
            file.write(f'    # {inner_list[1]}\n')
            file.write(f'        scoreboard players add @a {inner_list[0]} 0\n')

            if inner_list[3].startswith('tag'):
                if ',' in inner_list[3]:
                    tags_list = inner_list[3].split(',')
                    tags_list[0] = tags_list[0][4:]
                    file.write('        scoreboard players add @a[')
                    for i, tag in enumerate(tags_list):
                        file.write(f'tag={tag}')
                        if i != len(tags_list) - 1:
                            file.write(', ')
                    file.write(', scores={' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')
                else:
                    file.write('        scoreboard players add @a[tag=' + inner_list[3][4:] + ', scores={' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[3].startswith('scores'):
                file.write('        scoreboard players add @a[scores={' + inner_list[3][7:] + ', ' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[3].startswith('item'):
                file.write('        scoreboard players add @a[hasitem={item=' + inner_list[3][5:] + '}, scores={' +inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[3].startswith('external'):
                file.write('        # External trigger\n')

            file.write('        tellraw @a[scores={' + inner_list[0] + '=1}] { "rawtext": [ { "text": "Ę §2§lВыполнено достижение: §r' + inner_list[1] + '" } ] }\n')
            file.write('        execute as @a[scores={' + inner_list[0] + '=1}] at @s run playsound get_achievement @s ~ ~ ~\n')
            file.write('        scoreboard players set @a[scores={' + inner_list[0] + '=1}] ' + inner_list[0] + ' 99\n\n')
    print('Создан файл core')

def create_achievements_info_file():
    with open('output/info/achievements.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это инфо о достижениях\n')
        file.write('tellraw @s { "rawtext": [ { "text": "§6=====§aДОСТИЖЕНИЯ§6=====" } ] }\n')
        file.write('    # Невыполненные достижения\n')
        for inner_list in achievements_data:
            file.write('        # ' + inner_list[1] + '\n')
            file.write('            tellraw @s[scores={' + inner_list[0] + '=0}] { "rawtext": [ { "text": "ę §f' + inner_list[1] + '§f: §o>>> §с' + inner_list[2] + '." } ] }\n\n')
        file.write('    # Выполненные достижения\n')
        for inner_list in achievements_data:
            file.write('        # ' + inner_list[1] + '\n')
            file.write('            tellraw @s[scores={' + inner_list[0] + '=99}] { "rawtext": [ { "text": "Ę ' + inner_list[1] + ' (' + inner_list[2] + ')" } ] }\n\n')
    print('Создан файл инфо')

def create_world_reg_file():
    with open('output/world_reg/achievements.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это регистрация переменный достижений\n')
        for inner_list in achievements_data:
            file.write(f'scoreboard objectives add {inner_list[0]} dummy {inner_list[0]}\n')
    print('Создан файл регистрации переменных')

def create_wipe_function():
    with open('output/knockout_system/data_wipe/wipe_achievements.mcfunction', "w", encoding='utf-8') as file:
        for inner_list in achievements_data:
            file.write(f'scoreboard players set @s {inner_list[0]} 0\n')
    print('Создан mcfunction для очистки данных о достижениях')

os.chdir(os.path.dirname(os.path.abspath(__file__)))
clear_directory('output')
create_directory('output')
create_directory('output/info')
create_directory('output/world_reg')
create_directory('output/core_parts_NAP')
create_directory('output/knockout_system/data_wipe')

print('=====')
achievements_data = read_achievements_data()
create_achievements_core_file()
create_achievements_info_file()
create_world_reg_file()
create_wipe_function()
print('=====')
print('AACHC успешно завершил работу')
import os
import shutil

def clear_directory(directory_path):
    # Проверяем, существует ли директория
    if os.path.exists(directory_path) and os.path.isdir(directory_path):
        # Проходим по всем файлам и подкаталогам в директории
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)

            # Если это файл, удаляем его
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Удалён файл: {file_path}")

            # Если это директория, удаляем её вместе с содержимым
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Удалена директория: {file_path}")

def create_directory(directory_path):
    try:
        # Создаем директорию, если она не существует
        os.makedirs(directory_path, exist_ok=True)
        print(f"Директория '{directory_path}' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании директории: {e}")

def read_achievements_data():  # Читаем данные об достижениях
    content = []
    with open('AACHC_in.txt', "r", encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split()
                
                if len(parts) != 5: # Если не то количество элементов в строке 
                    print('Ошибка количества подаваемых данных в строке ' + str(parts))
                    os._exit(0)

                # Создаем новый список для каждого ненулевого элемента
                current_entry = []

                for part in parts:
                    if part != parts[0] and part != parts[4]:
                        part = part.replace("_", " ")
                    part = part.replace("name=", "").replace("descr=", "").replace("xp=", "").replace("trigger=", "")

                    current_entry.append(part)  # Добавляем в текущую запись
                
                content.append(current_entry)  # Добавляем текущую запись в содержимое

    return content

def create_achievements_core_file(): # Создаем файлы с достижениями
    with open('output/core_parts_NAP/achievements_core.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это функция анализа достижений. Автозапуск каждые 20tcs (1 сек) функцией 20ticks.mcfunction\n\n')
        for inner_list in achievements_data: # Цикл для каждого достижения
            file.write(f'    # {inner_list[1]}\n') # Закомментированное описание достижения



            file.write(f'        scoreboard players add @a {inner_list[0]} 0\n') # Авторег



            if inner_list[4].startswith('tag'): # Если условие достижения - тег
                if ',' in inner_list[4]: # Если подано несколько тегов
                    tags_list = inner_list[4].split(',')
                    tags_list[0] = tags_list[0][4:]

                    file.write('        scoreboard players add @a[')
                    for i, tag in enumerate(tags_list):
                        file.write(f'tag={tag}')
                        if i != len(tags_list) - 1:
                            file.write(', ')
                    file.write(', scores={' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

                else: # Если подан 1 тег
                    file.write('        scoreboard players add @a[tag=' + inner_list[4][4:] + ', scores={' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[4].startswith('scores'): # Если условие достижения - score
                file.write('        scoreboard players add @a[scores={' + inner_list[4][7:] + ', ' + inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[4].startswith('item'): # Если условие достижения - предмет
                file.write('        scoreboard players add @a[hasitem={item=' + inner_list[4][5:] + '}, scores={' +inner_list[0] + '=0}] ' + inner_list[0] + ' 1\n')

            if inner_list[4].startswith('external'): # Если стороннее условие достижения
                file.write('        # External trigger\n')


            # Сообщение о выполненом достижении
            file.write('        tellraw @a[scores={' + inner_list[0] + '=1}] { "rawtext": [ { "text": "Ę §2§lВыполнено достижение: §r' + inner_list[1] + ' (' + inner_list[2] + ')!" } ] }\n')


            # Выдача ОП
            file.write('        scoreboard players add @a[scores={' + inner_list[0] + '=1}] xp_tray ' + inner_list[3] + '\n')


            # Проигрывание звука
            file.write('        execute as @a[scores={' + inner_list[0] + '=1}] at @s run playsound get_achievement @s ~ ~ ~\n')


            # Контроль переменной достижения
            file.write('        scoreboard players set @a[scores={' + inner_list[0] + '=1}] ' + inner_list[0] + ' 99\n')


            # Сноска в конце
            file.write('\n')
    print('Создан файл core')


def create_achievements_info_file():
    with open('output/info/achievements.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это инфо о достижениях\n')
        file.write('tellraw @s { "rawtext": [ { "text": "§6=====§aДОСТИЖЕНИЯ§6=====" } ] }\n')

        file.write('    # Невыполненные достижения\n')
        for inner_list in achievements_data: # Цикл для каждого достижения
            file.write('        # ' + inner_list[1] + '\n') # Название достижения

            file.write('            tellraw @s[scores={' + inner_list[0] + '=0}] { "rawtext": [ { "text": "ę §f' + inner_list[1] + ' §a[§f' + inner_list[3] + ' XP§a]§f: §o>>> §с' + inner_list[2] + '." } ] }\n')

            # Сноска в конце
            file.write('\n')

        file.write('    # Выполненные достижения\n')
        for inner_list in achievements_data: # Цикл для каждого достижения
            file.write('        # ' + inner_list[1] + '\n') # Название достижения

            file.write('            tellraw @s[scores={' + inner_list[0] + '=99}] { "rawtext": [ { "text": "Ę ' + inner_list[1] + ' (' + inner_list[2] + ')" } ] }\n')

            # Сноска в конце
            file.write('\n')
    print('Создан файл инфо')


def create_world_reg_file():
    with open('output/world_reg/achievements.mcfunction', "w", encoding='utf-8') as file:
        file.write('# Это регистрация переменный достижений\n')
        for inner_list in achievements_data: # Цикл для каждого достижения
            file.write(f'scoreboard objectives add {inner_list[0]} dummy {inner_list[0]}\n')
    print('Создан файл регистрации переменных')


os.chdir(os.path.dirname(os.path.abspath(__file__))) # Устанавливаем путь выполнения кода
clear_directory('output') # Очищаем старые данные
create_directory('output') # Создаем нужное древо директорий
create_directory('output/info')
create_directory('output/world_reg')
create_directory('output/core_parts_NAP')

print('=====')

achievements_data = read_achievements_data()
create_achievements_core_file()
create_achievements_info_file()
create_world_reg_file()

print('=====')

print('AACHC успешно завершил работу')
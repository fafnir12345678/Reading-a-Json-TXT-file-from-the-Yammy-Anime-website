import json
import os

def convert_anime_list(json_file_path, txt_file_path):
    try:
        # Проверяем существование файла
        if not os.path.exists(json_file_path):
            print(f"Ошибка: Файл {json_file_path} не найден")
            return
        
        # Читаем JSON файл
        with open(json_file_path, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            
        # Исправляем возможные проблемы с форматом JSON
        if not content.startswith('['):
            content = '[' + content
        if not content.endswith(']'):
            content = content + ']'
        
        # Заменяем некорректные последовательности
        content = content.replace('},,{', '},{').replace('},,', '},')
        
        anime_data = json.loads(content)
        
        # Словарь для отображения статусов
        status_display = {
            "completed": "Просмотрено",
            "watching": "Смотрю",
            "planned": "В планах",
            "null": "Отложено", 
            "dropped": "Брошено",
            "rewatching": "Пересматриваю"
        }
        
        # Группируем аниме по статусам
        grouped_anime = {}
        for anime in anime_data:
            if not isinstance(anime, dict):
                continue
                
            status = anime.get('status', '')
            title = anime.get('target_title', 'Неизвестное название')
            
            # Пропускаем записи с некорректным статусом
            if not status or status not in status_display:
                continue
                
            display_status = status_display[status]
            if display_status not in grouped_anime:
                grouped_anime[display_status] = []
            grouped_anime[display_status].append(title)
        
        # Порядок отображения разделов
        display_order = ["Смотрю", "Просмотрено", "В планах", "Отложено", "Брошено", "Пересматриваю"]
        
        # Создаем текстовый файл
        with open(txt_file_path, 'w', encoding='utf-8') as file:
            for section in display_order:
                if section in grouped_anime and grouped_anime[section]:
                    file.write(f"{section}\n")
                    for title in grouped_anime[section]:
                        file.write(f"· {title}\n")
                    file.write("\n")
        
        # Статистика
        total_anime = sum(len(v) for v in grouped_anime.values())
        print(f"Успешно! Создан файл: {txt_file_path}")
        print(f"Обработано аниме: {total_anime}")
        
        # Выводим статистику по статусам
        for status in display_order:
            if status in grouped_anime:
                count = len(grouped_anime[status])
                print(f"{status}: {count}")
                
    except json.JSONDecodeError as e:
        print(f"Ошибка декодирования JSON: {e}")
        print("Проверьте корректность JSON файла")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Использование
if __name__ == "__main__":
    input_file = "C:\\google disk\\важное\\Бэкапы\\Anime list [site.yummyani.me].json"
    output_file = "C:\\google disk\\важное\\Бэкапы\\аниме.txt"
    
    convert_anime_list(input_file, output_file)

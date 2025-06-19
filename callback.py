# Имя файла: callback.py

def change_commit_message(message):
  # Создаем обычную Unicode-строку с кириллицей
  target_string = "Удалены все комментарии из кода + обновлен логотип\n"
  
  # Сравниваем message (который является байтами) с нашей строкой, 
  # которую мы тоже кодируем в байты с помощью UTF-8
  if message == target_string.encode('utf-8'):
    
    # Возвращаем новое сообщение. Тут можно использовать b'', 
    # так как "New version" содержит только ASCII символы.
    return b"New version\n"
  
  # Если сообщение не совпало, возвращаем его без изменений
  return message
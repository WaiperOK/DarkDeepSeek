
def change_commit_message(message):
  target_string = "Удалены все комментарии of кода + обновлен логотип\n"
  
  if message == target_string.encode('utf-8'):
    
    return b"New version\n"
  
  return message
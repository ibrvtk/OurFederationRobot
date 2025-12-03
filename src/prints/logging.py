from datetime import datetime



async def print_error(message) -> None:
    '''Логгирование ошибки.'''    
    timestamp = datetime.now().strftime("%H:%M")
    print(f"[{timestamp}] (X) {message}")

async def print_other(message) -> None:
    '''Логгирование любой информации.'''
    timestamp = datetime.now().strftime("%H:%M")
    print(f"[{timestamp}] {message}")
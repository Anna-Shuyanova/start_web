def check_correct_data(time_str, heart_rate):
    if not isinstance(heart_rate, int) or heart_rate < 0:
        return False

    parts = time_str.split(':')
    
    if len(parts) != 3:
        return False

    for i in range(len(parts)):
        if not parts[i].isdigit():
            return False
        parts[i] = int(parts[i])

    hour, minute, second = parts

    if not (0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60):
        return False

    return True

def accept_package(storage_data, package):
    time, heart_rate = package
    if check_correct_data(time, heart_rate):
        storage_data[time] = heart_rate
        return storage_data
    else:
        return f"Некорректный пакет данных!"

def main():
    storage_data = {}
    
    while True:
        time_input = input("Введите текущее время (HH:MM:SS): ").strip()
        
        if not is_valid_time_format(time_input):
            print("Некорректный формат времени! Используйте формат HH:MM:SS.")
            
        heart_rate_str = input("Введите частоту сердечных сокращений (уд/мин): ").strip()
        
        if not heart_rate_str.isdigit():
            print("Частота сердечных сокращений должна быть положительным целым числом!")

        heart_rate = int(heart_rate_str)
        
        package = (time_input, heart_rate)
        storage_data = accept_package(storage_data, package)
        
        print(f"Время: {time_input}")
        print(f"Частота сердечных сокращений: {heart_rate} уд/мин")
        
        if heart_rate >= 100:
            print('Осторожно что-то не так! Обратитесь к врачу.')
        elif heart_rate >= 80:
            print('Осторожно успокойтесь!')
        elif heart_rate >= 60:
            print('Хороший результат, Вы двигаетесь в правильном направлении!')
        else:
            print('Главное — быть активным!')
        
        print("\n")

def is_valid_time_format(time_str):
    parts = time_str.split(':')
    if len(parts) != 3:
        return False
    for part in parts:
        if not part.isdigit():
            return False
    hour, minute, second = map(int, parts)
    return 0 <= hour < 24 and 0 <= minute < 60 and 0 <= second < 60

if __name__ == "__main__":
    main()




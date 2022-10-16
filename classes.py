from abc import abstractmethod, ABC


class Storage(ABC):  # Абстрактный класс
    @abstractmethod
    def add(self, name, count):
        pass

    @abstractmethod
    def remove(self, name, count):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):  # Склад

    def __init__(self, items: dict, capacity=100):  # capacity - максимальное количество товаров в позиции
        self.items = items
        self.capacity = capacity

    def add(self, name, count):  # Увеличение по ключу
        if name in self.items.keys():
            if self.get_free_space() >= count:
                self.items[name] += count
                return True
            else:
                if isinstance(self, Store):
                    return "Недостаточно места в магазине"
                elif isinstance(self, Store):
                    print("Недостаточно места на складе")
                return False
        else:
            if self.get_free_space() >= count:
                self.items[name] = count
                return True
            else:
                print("Недостаточно места на складе")
                return False

    def get_items(self):
        return self.items

    def remove(self, name, count):  # Уменьшение по ключу
        if self.items[name] >= count:
            print("Нужное количество есть на складе")
            self.items[name] -= count
            return True
        else:
            print("Недостаточно товара на складе!")
            return False

    def get_free_space(self):
        current_space = 0
        for item in self.items.values():
            current_space += item
        return self.capacity - current_space

    def get_unique_items_count(self):
        return len(self.items.keys())

    def __str__(self):
        st = ""
        for key, value in self.items.items():
            st += f"{key}: {value}\n"
        return st


class Shop(Store): # Магазин
    def __init__(self, items, capacity=20):  # capacity - максимальная вместимость
        super().__init__(items, capacity)

    def add(self, name, count):
        if self.get_unique_items_count() >= 5:  # Максимальное количество позиций товаров (по условию: 5)
            print("Слишком много уникальных товаров!")
            return False
        else:
            super().add(name, count)
            return True


class Request:
    def __init__(self, request_str):
        req_list = request_str.split()
        action = req_list[0]
        self.__count = int(req_list[1])
        self.__item = req_list[2]
        if action == "Доставить":  # Отнимает товары с одного места и прибавляет в другом
            self.__from = req_list[4]
            self.__to = req_list[6]
        elif action == "Забрать":  # Отнять в одном месте и нигде не прибавать
            self.__from = req_list[4]
            self.__to = None
        elif action == "Привезти":  # Прибавить в одном месте и нигде не убавить
            self.__from = None
            self.__to = req_list[4]

    def move(self):
        if self.__to and self.__from:
            if eval(self.__to).add(self.__item, self.__count):
                eval(self.__from).remove(self.__item, self.__count)
        elif self.__to:
            eval(self.__to).add(self.__item, self.__count)
        elif self.__from:
            eval(self.__from).remove(self.__item, self.__count)


"""Программа"""
print('Здравствуйте! Это программа Склад.\n')

storage_1 = Store(items={"Телефон": 10, "Компьютер": 10, "Телевизор": 10})  # Не больше 5 позиций
storage_2 = Store(items={"Телефон": 10, "Компьютер": 10, "холодильник": 10})
shop_1 = Shop(items={"Телефон": 3, "Компьютер": 3, "Телевизор": 3})

while True:
    print("Заполненность площадей:\n")
    print(f"storage_1:\n{storage_1}")
    print(f"storage_2:\n{storage_2}")
    print(f"shop_1:\n{shop_1}")
    user_text = input("Введите команду:\n")  # примеры ввода пользователя ниже
    if user_text == "стоп":  # по слову стоп цикл завершается
        break
    else:
        req = Request(user_text)
        req.move()

""" Компанды для тестирования:

Доставить 3 Компьютер из storage_1 в shop_1
Забрать 3 Телефон из storage_1
Привезти 10 Компьютер из storage_2

"""
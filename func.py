class Manager:
    def __init__(self):
        self.warehouse = []
        self.history = []
        self.balance = self.balance_his()
        self.komunikat = "Tutaj zobaczysz komunikaty."
        self.warehouse_actual()
        self.history_file()

    def is_or_not(self, item):
        if len(self.warehouse) > 0:
            for i in self.warehouse:
                if i[0] == item:
                    return True

            return False
        else:
            return False

    def warehouse_actual(self):
        try:
            if len(self.warehouse) < 1:
                with open('warehouse.txt') as warehous:
                    for line in warehous:
                        self.warehouse.append(eval(line))
        except:
            pass

    def history_write(self):
        if len(self.history) > 0:
            with open("history.txt", "w") as file:
                for item in self.history:
                    file.write(str(item) + '\n')

    def item_in(self, item):
        for i in self.warehouse:
            if i[0] == item:
                ilosc = i[1]['ilosc']
                return ilosc

    def balance_his(self):
        try:
            with open('balance.txt') as balan:
                self.balance = float(balan.read())
        except:
            self.balance = 0
        return self.balance

    def wareh_write(self):
        with open("warehouse.txt", "w") as file:
            for item in self.warehouse:
                file.write(str(item) + "\n")

    def history_file(self):
        try:
            if len(self.history) == 0:
                with open('history.txt') as file:
                    for line in file:
                        x = line.strip()
                        self.history.append(x)
        except:
            pass

    def balancee(self, add):
        add = float(add)
        if manager.balance + add < 0:
            self.komunikat = 'Nieprawidlowe dane. Saldo Twojego konta nie może być ujemne.'
        else:
            self.balance += add
            self.history.append(f'Zmiana kwoty o {add}')
            self.komunikat = f"Zmieniono saldo o {add}"
        with open("balance.txt", "w") as text:
            text.write(str(self.balance))

    def sell(self, item, quantity, cost):
        item = item.upper()
        quantity = int(quantity)
        cost = float(cost)
        if self.is_or_not(item):
            if quantity > self.item_in(item):
                self.komunikat = f'Podano liczbę większą niz stan magazynu. Nie możesz sprzedać więcej niż {self.item_in(item)}'
            else:
                self.balance = self.balance + cost * quantity
                for a in self.warehouse:
                    if item == a[0]:
                        a[1]['ilosc'] -= quantity
                        if a[1]['ilosc'] <= 0:
                            self.history.append(f'Sprzedano {quantity} sztuk przedmiotu {item}')
                            self.warehouse.remove(a)
                            self.wareh_write()
                            break

                        else:
                            self.history.append(f'Sprzedano {quantity} sztuk przedmiotu {item}')
                            self.wareh_write()
                            break
        else:
            self.komunikat = f'Brak produktu {item} na stanie magazynu.'

    def purchase(self, item, quantity, cost):
        item = item.upper()
        quantity = int(quantity)
        cost = float(cost)
        if self.is_or_not(item):
            for i in self.warehouse:
                if self.balance - quantity * cost < 0:
                    self.komunikat = 'Zakup nie jest możliwy. Brak środków.'
                    break
                if i[0] == item and self.balance - quantity * cost >= 0:
                    if i[1]['koszt'] != cost:
                        self.komunikat = 'Niestety. Podaleś różne ceny dla tego samego produktu.'
                        break

                    self.komunikat = 'Produkt już znajduje się w magazynie. Ilość poprawnie zmieniona.'
                    i[1]['ilosc'] += quantity
                    self.history.append(f'Zaaktualizowano ilosc produktu {item} o {quantity}')
                    self.balance = self.balance - quantity * cost
                    self.wareh_write()
                    break
        if not self.is_or_not(item):
            if self.balance - quantity * cost >= 0:
                self.warehouse.append([item, {'ilosc': quantity, 'koszt': cost}])
                self.history.append(f'Dodano produkt {item} w cenie {cost} w ilości {quantity}')
                self.balance = self.balance - quantity * cost
                self.wareh_write()
                self.komunikat = f'Dodano produkt {item} w cenie {cost} w ilości {quantity}'
            else:
                self.komunikat = 'Brak środków na pokrycie zakupu.'
        with open("balance.txt", "w") as text:
            text.write(str(self.balance))


manager = Manager()


def history(manager):
    if len(manager.history) > 0:
        print(f'Wykonano łącznie {len(manager.history)} operacji.')
        print('Możesz wybrać zakres operacji. ')
        print(f'Możliwy przedział to: 1 do {len(manager.history)}')
        od = input("Wprowadź numer operacji od której pragniesz zaczać.")
        if od.isnumeric() is False or int(od) < 1 or int(od) > len(manager.history):
            print(f'Błędna wartość. Możliwy przedział to: 1 do {len(manager.history)}')
            print('Wyświetlam wyniki od operacji pierwszej.')
            od = 1
        do = input("Wprowadź numer operacji na której pragniesz zakończyć.")
        if do.isnumeric() is False or int(do) > len(manager.history) or int(od) > int(do):
            print(f'Błędna wartość. Możliwy przedział to: 1 do {len(manager.history)}')
            print('Wyświetlam wyniki do samego końca.')
            do = int(len(manager.history))
        manager.execute("history_number", od, do)
    else:
        print("Historia wykonanych operacji jest pusta.")


def history_number(manager, od, do, a=0):
    od = int(od)
    do = int(do)
    if od > 0:
        for i in manager.history:
            a = a + 1
            if a < od or a > do:
                continue
            print(f'Opercja numer: {a} to  {i}')
            print('***************************************************')


def warehouse_per_item(manager):
    item = input('Podaj nazwę produktu: ').upper()
    if manager.is_or_not(item):
        for i in manager.warehouse:
            if i[0] == item:
                ilosc = i[1]['ilosc']
                cena = i[1]['koszt']
                print('Stan magazynu:')
                print(f'Dla produktu {item}, to {ilosc}. Cena jednej sztuki: {cena}.')

## Задание 5; Рябинин Владислав Денисович; Solo;
## Затраченные ресурсы: бутылка водки и бессонная ночь
from math import *
from collections import deque
from random import *

class Espresso:
    ingredients = {"coffee": 1, "hot_water": 1}
    prices = {"coffee": 0.35, "hot_water": 0.08, "milk": 0.22,
              "steamed_milk": 0.25, "milk_foam": 0.15, "chocolate": 0.22}

    def __init__(self, volume):
        self.volume = volume

    def time(self):
        return round(60 + (self.volume/300)*30) # 60 секунд подготовить стакан (+ остальные ингредиенты) + время залить кипятком (зависит от V)

    def self_cost(self):
        final_cost = 0
        for key in self.ingredients.keys():
            final_cost += self.ingredients[key] * self.prices[key] * self.volume
        return final_cost

    def cost(self):
        final_cost = 0
        return self.self_cost() * 1.10


class Cappuccino(Espresso):
    ingredients = Espresso.ingredients.copy()
    ingredients.setdefault('milk_foam', 1)
    ingredients.setdefault('steamed_milk', 1)

    def __init__(self, volume):
        super().__init__(volume)

    def time(self):
        return round(super().time() + 15 + (self.volume/300)*30) # 15 секунд сверху нанести пенку + от объёма зависит, сколько наливать молоко

class Flat_White(Espresso):
    ingredients = Espresso.ingredients.copy()
    ingredients.setdefault('steamed_milk', 2)

    def __init__(self, volume):
        super().__init__(volume)

    def time(self):
        return round(super().time() + (self.volume/300)*50) # доп. время на то, чтобы добавить молоко


class Mocha(Espresso):
    ingredients = Espresso.ingredients.copy()
    ingredients.setdefault('chocolate', 1)
    ingredients.setdefault('steamed_milk', 0.5)

    def __init__(self, volume):
        super().__init__(volume)

    def time(self):
        return round(super().time() + 10 + (self.volume/300)*20) # 10 секунд насыпать шоколад + налить молоко


class Americano(Espresso):
    ingredients = Espresso.ingredients.copy()
    ingredients['hot_water'] = 2.5

    def __init__(self, volume):
        super().__init__(volume)

    def time(self):
        return round(super().time() + (self.volume/300)*20) # время на то, чтобы долить горячей воды


class Cortado(Espresso):
    ingredients = Espresso.ingredients.copy()
    ingredients.setdefault('milk_foam', 0.5)

    def __init__(self, volume):
        super().__init__(volume)

    def time(self):
        return round(super().time() + 15) # 15 секунд на пенку

def Client(hour): # функция определения прихода клиента
    f_t = [10, 25, 50, 70, 80, 75, 60, 55, 40, 45, 60, 85, 45, 15]
    p = (f_t[hour] / 3600)
    return uniform(0, 1) < p

def Coffee(): # функция определения вида кофе и V
    volume = choice([60, 100, 150, 250, 300, 400, 500]) # кофейня предлагает на выбор разные V в стакане
    kinds_of_coffee = [Espresso, Cappuccino, Flat_White, Mocha, Americano, Cortado]
    type_coffee = choice(kinds_of_coffee)
    return type_coffee(volume)

def FIRE(): # это грустная статистика, но в России раз в день происходит пожар (примерно) в общепите
    return uniform(0, 1) < (10**(-5) / 14)

def Time_Of_Choice(): # сколько времени будет выбирать заказ
    usually_time = [10, 60, 120]
    return choice(usually_time)

def Time_Of_Getting(): # сколько времени будет получать заказ
    p = uniform(0, 1)
    if p < 0.004:
        return randint(180, 900) # в среднем на 250 клиентов есть какой-то скандал, в среднем они длятся от 3 до 15 минут
    else: # считаем, что во время конфликта кофейня не предлагает переделать заказ, поскольку наши баристы идеально его готовят
        return 20 # стандартная выдача заказа секунд 20

def Time_Of_Mistake(time, hour): # все люди иногда совершают ошибки..
    p = [1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 5] # на 100 заказов в разные часы в среднем столько убитых заказов
    total_time, curr_time = 0, 0 # всего время на приготовление, текущая готовность
    while curr_time != time:
        p_mistake = uniform(0, 1)
        if p_mistake < (p[hour] / (100*time)): # если ошибся, то начинает сначала + сколько-то времени на устранение своей ошибки
            curr_time = 0
            total_time += 1 + randint(10, 60)
        else:
            curr_time += 1
            total_time += 1
    return total_time

n = int(input('Введите число n, количество бариста в вашей кофейне: '))
queue = [deque() for _ in range(n)]
time_work = [0 for _ in range(n)]
all_orders, clients_without_coffee, average_size_of_queue, average_time_in_queue = [], 0, [0, 0], [0, 0]
for hour in range(8, 22):
    if FIRE():
        print('Ваша кофейня сгорела, Милорд!')
        exit()
    for time in range(0, 3600):
         if Client(hour-8) == 1: # если пришёл клиент
             min_queue = min([len(queue[i]) for i in range(n)])  # человек анализирует количество людей в очереди
             average_size_of_queue[0], average_size_of_queue[1] = average_size_of_queue[0] + min_queue, average_size_of_queue[1] + (min_queue != 0) # если очередь есть, то запоминаем значение для среднего
             if min_queue >= 5: # если в очередях минимум 5 человек, то клиент разворачивается и уходит
                 clients_without_coffee += 1
             for i in range(n*(min_queue < 5)): # он смотрит все очереди, однако только в случае, если минимальная очередь меньше пяти
                 if len(queue[i]) == min_queue: # идёт в первую очередь, где меньшее количество людей
                     order = Coffee() # случайным образом выбирает кофе
                     all_time = Time_Of_Getting()+Time_Of_Choice()
                     all_time = all_time + Time_Of_Mistake(order.time(), hour-8)
                     if hour == 21:
                         flag = sum(queue[i])+time_work[i] < (3600 - time) # в последний час работы важно проверять факт того, что бариста успеет завершить последний заказ
                         if flag == 1:
                             average_time_in_queue[0] += time_work[i] + sum(queue[i])  # человеку в очереди нужно прождать остальных + время на нынешний заказ
                             average_time_in_queue[1] += (time_work[i] + sum(queue[i]) != 0) # если очереди нет, то это этот клиент не учитывается, т.к. считаем среднее среди тех людей, которые стояли в очереди
                             all_orders.append(order)
                             queue[i].append(all_time)
                         else: # клиенту вежливо сообщают, что его заказ не успеют приготовить
                             clients_without_coffee += 1
                     else:
                         average_time_in_queue[0] += time_work[i] + sum(queue[i])
                         average_time_in_queue[1] += (time_work[i] + sum(queue[i]) != 0)
                         all_orders.append(order) # в общий список добавляем готовый заказ
                         queue[i].append(all_time) # в очередь добавляем время
                     break # клиент встал в очередь, дальше смотреть не нужно

         time_work = [time - (time != 0) for time in time_work] # если время 0 то ничего не делаем, иначе уменьшаем на 1
         for i in range(n):
             if (len(queue[i]) != 0) and time_work[i] == 0: # заказ начинает готовиться со следующей секунды
                 time_work[i] = queue[i][0] # бариста берёт первый заказ из своей очереди
                 queue[i].popleft() # заказ уходит

income, self_cost, average_time = 0, 0, 0
for order in all_orders:
    income += order.cost()
    self_cost += order.self_cost()
    average_time += order.time()
print(f'Общая выручка за этот прекрасный день равна {int(income)} золотых, Господин!')
print(f'Общая себестоимость проданных снадобий за этот изумительный день равна {int(self_cost)} золотых, Милорд!')
print(f'Среднее время, которое потратили наши рабы на приготовление кофе составляет {int(average_time / n)} секунд, Создатель!')
print(f'Количество гоблинов, которые не смогли насладиться нашей сывороткой равняется {clients_without_coffee}')
print(f'Среднее количество гоблинов в очереди за сегодняшний день равно {average_size_of_queue[0] / average_size_of_queue[1]:.3f}')
print(f'Среднее количество секунд, которое гоблины простояли в очередях за нашей прелестью сегодня равно {average_time_in_queue[0] / average_time_in_queue[1]:.3f}')










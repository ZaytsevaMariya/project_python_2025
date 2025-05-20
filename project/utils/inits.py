import flet as ft
import math
import numpy as np
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

all_style: dict = {
    "main": {
        "expand": True,
        "bgcolor": '#17181d',
        "border_radius": 10,
        "width": 50,
        "height": 1000,
    }
}

'Класс Graph1: содержит координаты двух точек, через которые задаются геодезические: coordinate1, coordinate2; коэффициенты преобразования: transformation1, transformation2, transformation3, transformation4; функции, которые рисуют графики, преднозначен для модели верхней полуплоскости'
class Graph1(ft.Container):
    def __init__(self) -> None:
        super().__init__(**all_style.get("main"))

        self.size = 100

        self.coordinate1 = complex(0, 0)
        self.coordinate2 = complex(0, 0)
        self.trans_coordinate1 = complex(0, 0)
        self.trans_coordinate1 = complex(0, 0)
    
        self.transformation1 = 0
        self.transformation2 = 0
        self.transformation3 = 0
        self.transformation4 = 0

        self.key_circle = True
                           
    '''
    функция circle: параметрически задаёт дугу радиуса radius, диапазон дуги задаётся углом angle, центр задаётся вектором с координатами vector1, vector2
    '''    
    def circle(self, angle, radius, vector1 = 0, vector2 = 0):
        self.radius_array = np.array([radius for _ in range(self.size)])
        vector1_array = np.array([vector1 for _ in range(self.size)])
        vector2_array = np.array([vector2 for _ in range(self.size)])

        return (self.radius_array * np.cos(angle) + vector1_array), (self.radius_array * np.sin(angle) + vector2_array)
    
    '''
    функция line: параметрически задаёт вертикальную линию
    '''
    def line(self, parameter, coordinate):
        self.x_array = np.array([coordinate for _ in range(self.size)])

        return self.x_array, parameter
    
    '''
    функция graph: содержит информацию о внешнем виде графика
    '''
    def graph(self):
        self.fig = plt.figure(facecolor="#17181d")        

        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_facecolor("#17181d")
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')

        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')

        if self.key_circle:
            self.draw_circle(self.ax)

        else:
            self.draw_line(self.ax)
        
        return self.fig
    
    '''
    функция draw_circle: рисует дугу до преобразования(зелёный) и после(красный)
    '''
    def draw_circle(self, ax):
        self.ax.set_aspect('equal')
        self.angle = np.linspace(0, np.pi, self.size)
        self.x, self.y = self.circle(self.angle, self.radius, self.center)
        self.trans_x, self.trans_y = self.circle(self.angle, self.trans_radius, self.trans_center)

        ax.plot(self.x, self.y, color = "green")
        ax.plot(self.trans_x, self.trans_y, color = "red")

        ax.scatter(self.coordinate1.real, self.coordinate1.imag, color='blue')
        ax.scatter(self.coordinate2.real, self.coordinate2.imag, color='blue')

    '''
    функция draw_line: рисует вертикальные линии до преобразования(зелёный) и после(красный), содержит две вспомогательные линии (x1_for_scale, y1_for_scale), (x2_for_scale, y2_for_scale), которые помещают рассматриваемые линии в центр графика
    '''
    def draw_line(self, ax):
        self.parameter = np.linspace(self.coordinate1.imag + 4*(self.coordinate1.imag - self.coordinate2.imag), self.coordinate2.imag + 4*(-self.coordinate1.imag + self.coordinate2.imag), self.size)
        self.x, self.y = self.line(self.parameter, self.coordinate1.real)        
        self.trans_x, self.trans_y = self.line(self.parameter, self.trans_coordinate1.real)
        self.x1_for_scale, self.y1_for_scale = self.line(self.parameter, self.coordinate1.real + 4*(self.coordinate1.real - self.trans_coordinate1.real))
        self.x2_for_scale, self.y2_for_scale = self.line(self.parameter, self.trans_coordinate1.real + 4*(-self.coordinate1.real + self.trans_coordinate1.real))

        ax.plot(self.x, self.y, color = "green")
        ax.plot(self.trans_x, self.trans_y, color = "red")
        ax.plot(self.x1_for_scale, self.y1_for_scale, color = "#17181d")
        ax.plot(self.x2_for_scale, self.y2_for_scale, color = "#17181d")

        ax.scatter(self.coordinate1.real, self.coordinate1.imag, color='blue')
        ax.scatter(self.coordinate2.real, self.coordinate2.imag, color='blue')
    
    '''
    функция compute_center: вычисляет центр полуокружности, которая является геодезической в верхней полуплоскости
    '''
    def compute_center(self, coordinate1, coordinate2):
        return ((coordinate1.imag)**2 - (coordinate2.imag)**2 + (coordinate1.real)**2 - (coordinate2.real)**2)/(2 * (coordinate1.real - coordinate2.real))
    
    '''
    функция compute_radius: вычисляет радус полуокружности, которая является геодезической в верхней полуплоскости
    '''
    def compute_radius(self, coordinate1, center):
        return math.sqrt((coordinate1.imag)**2 + (coordinate1.real - center)**2)
    
    '''
    функция examine: выбирает какой тип геодезической (прямую или полуокружность) задал пользователь и запускает отрисовку соответствующего графика в левом окне
    '''
    def examine(self) -> None:

        if (self.coordinate1.real - self.coordinate2.real) != 0:
            self.key_circle = True
            self.center = self.compute_center(self.coordinate1, self.coordinate2)
            self.radius = self.compute_radius(self.coordinate1, self.center)
            self.trans_coordinate1 = (self.transformation1 + self.transformation2 * self.coordinate1) / (self.transformation3 + self.transformation4 * self.coordinate1)
            self.trans_coordinate2 = (self.transformation1 + self.transformation2 * self.coordinate2) / (self.transformation3 + self.transformation4 * self.coordinate2)
            self.trans_center = self.compute_center(self.trans_coordinate1, self.trans_coordinate2)
            self.trans_radius = self.compute_radius(self.trans_coordinate1, self.trans_center)

        else:
            self.key_circle = False
            self.trans_coordinate1 = (self.transformation1 + self.transformation2 * self.coordinate1) / (self.transformation3 + self.transformation4 * self.coordinate1)
            self.trans_coordinate2 = (self.transformation1 + self.transformation2 * self.coordinate2) / (self.transformation3 + self.transformation4 * self.coordinate2)
            
        self.content = MatplotlibChart(self.graph(), expand=True)
        self.update()

        
'''
Класс Graph2: наследует Graph1 с целью упрощения отрисовки графика, отвечающего модели диска, переписаны функции draw_circle и draw_line для случая диска
'''
class Graph2(Graph1):
    def __init__(self) -> None:
        super().__init__()

    '''
    функция disk_transformation: переводит точки с верхней полуплоскости в единичный диск преобразованием (z+i)/(z-i)
    '''
    def disk_transformation(self, x, y):
        return ((x)**2 + (y)**2 - 1) / ((x)**2 + (y + 1)**2), ((-2 * x) / ((x)**2 + (y + 1)**2))

    '''
    функция draw_circle: рисует дуги в диске посредством применения преобразования (z+i)/(z-i) к точкам соответствующих дуг н верхней полуплоскости
    '''
    def draw_circle(self, ax):
        self.ax.set_aspect('equal')
        self.angle = np.linspace(0, np.pi, self.size)
        self.angle_main = np.linspace(0, 2 * np.pi, self.size)
        self.x, self.y = self.circle(self.angle, self.radius, self.center)
        self.trans_x, self.trans_y = self.circle(self.angle, self.trans_radius, self.trans_center)
        self.main_x, self.main_y = self.circle(self.angle_main, 1, 0)

        self.x_for_disk, self.y_for_disk = self.disk_transformation(self.x, self.y)
        self.trans_x_for_disk, self.trans_y_for_disk = self.disk_transformation(self.trans_x, self.trans_y)

        ax.plot(self.main_x, self.main_y, color = "white")
        ax.plot(self.x_for_disk, self.y_for_disk, color = "green")
        ax.plot(self.trans_x_for_disk, self.trans_y_for_disk, color = "red")
        self.point1_for_disk_x, self.point1_for_disk_y = self.disk_transformation(self.coordinate1.real, self.coordinate1.imag)
        self.point2_for_disk_x, self.point2_for_disk_y = self.disk_transformation(self.coordinate2.real, self.coordinate2.imag)
        ax.scatter(self.point1_for_disk_x, self.point1_for_disk_y, color='blue')
        ax.scatter(self.point2_for_disk_x, self.point2_for_disk_y, color='blue')

    '''
    функция compute_parameters_for_line_case: вычесляет параметры для дуги в диске, соответсвующей вертикальной прямой на верхней полуплоскости 
    '''  
    def compute_parameters_for_line_case(self, coord1, coord2):
        half_chord = (((1-coord1)**2 + coord2**2)**(1/2)) / 2
        alpha1 = math.asin(half_chord)
        alpha2 = math.acos(half_chord)
        radius = half_chord / math.cos(alpha1)

        return radius, alpha2

    '''    
    функция draw_line: рисует геодезические в диске, соответсвующие вертикальным прямым на верхней полуплоскости
    '''
    def draw_line(self, ax):
        self.ax.set_aspect('equal')
        self.angle_main = np.linspace(0, 2 * np.pi, self.size)
        self.main_x, self.main_y = self.circle(self.angle_main, 1, 0)

        second_coord_real, second_coord_imag = self.disk_transformation(self.coordinate1.real, 0)
        self.radius, alpha2 = self.compute_parameters_for_line_case(second_coord_real, second_coord_imag)

        self.angle = np.linspace(np.pi/2, np.pi/2 + 2*alpha2, self.size)
        self.x, self.y = self.circle(self.angle, self.radius, 0, 1, -self.radius)

        second_trans_coord_real, second_trans_coord_imag = self.disk_transformation(self.trans_coordinate1.real, 0)
        self.trans_radius, trans_alpha2 = self.compute_parameters_for_line_case(second_trans_coord_real, second_trans_coord_imag)

        self.trans_angle = np.linspace(np.pi/2, np.pi/2 + 2*trans_alpha2, self.size)
        self.trans_x, self.trans_y = self.circle(self.trans_angle, self.trans_radius, 0, 1, -self.trans_radius)

        ax.plot(self.main_x, self.main_y, color = "white")
        ax.plot(self.x, self.y, color = "green")
        ax.plot(self.trans_x, self.trans_y, color = "red")
        self.point1_for_disk_x, self.point1_for_disk_y = self.disk_transformation(self.coordinate1.real, self.coordinate1.imag)
        self.point2_for_disk_x, self.point2_for_disk_y = self.disk_transformation(self.coordinate2.real, self.coordinate2.imag)
        ax.scatter(self.point1_for_disk_x, self.point1_for_disk_y, color='blue')
        ax.scatter(self.point2_for_disk_x, self.point2_for_disk_y, color='blue')

import flet as ft
from flet.matplotlib_chart import MatplotlibChart

from utils import *

'''
Функция main: задаёт основные параметры окна приложения
'''
def main(page: ft.Page):
    page.title = "Transform Geodesic"
    page.theme_mode = 'light'
    graph1: ft.Container = Graph1()
    graph2: ft.Container = Graph2()
    geodesic_interface: ft.Container = Geodesic_interface(_graph1=graph1, _graph2=graph2)

    page.add(
        ft.Column(
            expand = True,
            controls = [ft.Row(expand = True, controls=[graph1, graph2]), geodesic_interface]
        )
    )
       

ft.app(main)
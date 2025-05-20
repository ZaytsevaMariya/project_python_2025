import flet as ft

'''
словарь со стилями для графических элементов окна
'''
geodesic_interface_style: dict = {
    "main": {
        "expand": True,
        "bgcolor": '#17181d',
        "border_radius": 10,
    },

    "style_for_button": {
        "icon": ft.icons.ADD,
        "bgcolor": "1f2128",
        "icon_size": 18,
        "icon_color": "teal600",
        "scale": ft.transform.Scale(0.8),
    },

    "style_for_coordinate1": {
        "label": "1st point",
        "width": 100,
        "color": "white",
    },

     "style_for_coordinate2": {
        "label": "2nd point",
        "width": 100,
        "color": "white",
    },

    "style_for_transformation1": {
        "label": "a",
        "width": 100,
        "color": "white",
    },

    "style_for_transformation2": {
        "label": "b",
        "width": 100,
        "color": "white",
    },

    "style_for_transformation3": {
        "label": "c",
        "width": 100,
        "color": "white",
    },

    "style_for_transformation4": {
        "label": "d",
        "width": 100,
        "color": "white",
    },
}


'''
Класс Geodesic_interface - наследуется от ft.Container, содержит информацию о графических элементах нижней части окна, обрабатывает действия пользователя и запускает отрисовку графиков
'''
class Geodesic_interface(ft.Container):
    def __init__(self, _graph1: object, _graph2: object) -> None:
        super().__init__(**geodesic_interface_style.get("main"))

        self._graph1: object = _graph1
        self._graph2: object = _graph2

        self.coordinate_field1 = ft.TextField(**geodesic_interface_style.get("style_for_coordinate1"))
        self.coordinate_field2 = ft.TextField(**geodesic_interface_style.get("style_for_coordinate2"))
        self.transformation_field1 = ft.TextField(**geodesic_interface_style.get("style_for_transformation1"))
        self.transformation_field2 = ft.TextField(**geodesic_interface_style.get("style_for_transformation2"))
        self.transformation_field3 = ft.TextField(**geodesic_interface_style.get("style_for_transformation3"))
        self.transformation_field4 = ft.TextField(**geodesic_interface_style.get("style_for_transformation4"))

        self.data_for_geodesic = ft.Row(alignment = "center", spacing = 100, controls = [ft.Row(alignment = 'center', controls = [self.coordinate_field1, self.coordinate_field2]), ft.Row(alignment = 'center', controls = [ft.Text("(a+bz)/(c+dz):", size=17, weight="w500", color = "white"), self.transformation_field1, self.transformation_field2, self.transformation_field3, self.transformation_field4])])
       
        '''
        функция update_coordinate: записывает координаты точек, введённых пользователям, в соответсвующие поля классов Graph1 и Graph2, проверяет корректность вводимых типов данных и запускает отрисовку графиков функией examine()
        '''    
        def update_coordinate(self, e) -> None:
            if self.is_complex(self.coordinate_field1.value) & self.is_complex(self.coordinate_field1.value) & self.is_float(self.transformation_field1.value) & self.is_float(self.transformation_field2.value) & self.is_float(self.transformation_field3.value) & self.is_float(self.transformation_field4.value):
                if self.det(float(self.transformation_field1.value), float(self.transformation_field2.value), float(self.transformation_field3.value), float(self.transformation_field4.value)):

                    self._graph1.coordinate1, self._graph2.coordinate1 = complex(self.coordinate_field1.value), complex(self.coordinate_field1.value)
                    self._graph1.coordinate2, self._graph2.coordinate2 = complex(self.coordinate_field2.value), complex(self.coordinate_field2.value)
                    self._graph1.transformation1, self._graph2.transformation1 = float(self.transformation_field1.value), float(self.transformation_field1.value)
                    self._graph1.transformation2, self._graph2.transformation2 = float(self.transformation_field2.value), float(self.transformation_field2.value)
                    self._graph1.transformation3, self._graph2.transformation3 = float(self.transformation_field3.value), float(self.transformation_field3.value)
                    self._graph1.transformation4, self._graph2.transformation4 = float(self.transformation_field4.value), float(self.transformation_field4.value)

                    self._graph1.examine()
                    self._graph2.examine()

                else: pass

            else: pass



        self.add_button = ft.IconButton(
            **geodesic_interface_style.get("style_for_button"),
            on_click= lambda e: update_coordinate(self, e),
        )

        
        '''
        self.content содержит все графические элементы нижней части окна
        '''
        self.content = ft.Column(
            horizontal_alignment="center",
            controls = [
                ft.Divider(height=1, color="#17181d"),
                ft.Text("Geodesic", size=17, weight="w500", color = "white"),
                self.data_for_geodesic, self.add_button,
                ft.Text("Enter two points on geodesic as x+yj and coefficients for transformation, such that ad-bc≠0, then push the green plus button. Otherwise, the program will do nothing.", size=17, weight="w500", color = "white")
            ]
        )

    '''
    функции is_complex и is_float: проверяют являются ли элементы типами complex и float, соответственно 
    '''
    def is_complex(self, word):
            try:
                complex(word)
                return True
            except ValueError:
                return False
            
    def is_float(self, word):
            try:
                float(word)
                return True
            except ValueError:
                return False
    '''
    функция det: проверяет корректность введённого преобразования
    '''        
    def det(self, a, b, c, d):
        return (a * d - b * c != 0)
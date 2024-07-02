import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._min = None
        self._max = None
        self._soglia = None

    def handle_graph(self, e):
        numNodi, numArchi = self._model.creaGrafo()
        self._view.txt_result.clean()
        self._view.txt_result.controls.append(ft.Text(f"nodi : {numNodi}   archi: {numArchi}"))
        self._min, self._max = self._model.getPesi()
        self._view.txt_result.controls.append(ft.Text(f"min: {self._min}, max: {self._max}"))
        self._view.update_page()

    def handle_countedges(self, e):
        self._soglia = self._view.txt_name.value
        if self._soglia.isdigit():
            if int(self._soglia) > self._min or int(self._soglia) < self._max:
                minori, maggiori = self._model.getSoglie(int(self._soglia))
            else:
                self._view.txt_result2.clean()
                self._view.txt_result2.controls.append(
                    ft.Text("Inserire un numero compreso tra il massimo e il minimo del grafo"))
                self._view.update_page()
        else:
            self._view.txt_result2.clean()
            self._view.txt_result2.controls.append(ft.Text("Inserire un numero nel campo soglia (anche negativo)"))
            self._view.update_page()
            return

        self._view.txt_result2.clean()
        self._view.txt_result2.controls.append(
            ft.Text(f"gli archi con peso minore alla soglia sono: {minori}, e quelli maggiori: {maggiori}"))
        self._view.update_page()

    def handle_search(self, e):
        path = self._model.inizializzazione(self._soglia)
        self._view.txt_result3.clean()
        # calcolo peso max
        pesoMax = 0
        for tappa in path:
            pesoMax += tappa.get_peso() ###########
        self._view.txt_result3.controls.append(ft.Text(f"Il peso massimo e': {pesoMax}"))
        for tappa in path:
            self._view.txt_result3.controls.append(ft.Text(""))
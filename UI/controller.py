import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_create_graph(self, e):
        n_alb = self._view.txtNumAlbumMin.value
        if n_alb.isnumeric():
            if int(n_alb) > 0:
                self._model.artists = self._model.load_artists(n_alb)
                self._model.build_graph()
            else:
                self._view.show_alert("No numero album minimo: poni intero maggiore di 0")
        else:
            self._view.show_alert("No numero: poni numero intero")

    def handle_connected_artists(self, e):
        pass



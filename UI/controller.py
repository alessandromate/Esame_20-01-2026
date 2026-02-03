import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def alarm_not_digit(self):
        self._view.show_alert("Metti un numero positivo")

    def alarm_not_correct_1(self):
        self._view.show_alert("Metti un numero positivo (anche decimale) in 'Durata minima' e un numero positivo intero in 'Numero massimo artisti (tra 1 e il numero di artisti nell'output precedente''")

    def handle_create_graph(self, e):
        n_alb = self._view.txtNumAlbumMin.value

        if not n_alb.isdigit():
            self.alarm_not_digit()
        else:
            n_nodes, n_edges, id_name = self._model.build_graph(n_alb)

            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {n_nodes} nodi, {n_edges} archi"))

            for a in id_name:
                name = a[1]
                self._view.ddArtist.options.append(ft.dropdown.Option(key=name , text=name))
            self._view.update_page()


    def handle_connected_artists(self, e):
        self._view.txt_result.controls.clear()

        n_alb = self._view.txtNumAlbumMin.value
        n_nodes, n_edges, id_name = self._model.build_graph(n_alb)
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {n_nodes} nodi, {n_edges} archi"))

        input = self._view.ddArtist.value
        triples= self._model.neigh_art(input)       #output: id, name, weight
        triples.sort(key=lambda x: x[0], reverse=False)
        for e in triples:
            self._view.txt_result.controls.append(ft.Text(f" {e[0]}, {e[1]} - Numero di generi comuni: {e[2]}"))
        self._view.update_page()

    def handle_ricerca(self, e):
        MaxArtists =self._view.txtMaxArtists.value
        MinDuration = self._view.txtMinDuration.value
        n_alb_min = self._view.txtNumAlbumMin.value

        if (MaxArtists.isdigit() and int(MaxArtists) in range(1, len(self._model.triples2)+1)):
            try:
                MinDuration =  float(MinDuration)
                if MinDuration >= 0:
                    peso_ott, sol_ott_list = self._model.build_ricerca(MaxArtists, MinDuration, n_alb_min)
                    self._view.txt_result.controls.clear()

                    self._view.txt_result.controls.append(
                        ft.Text(f"Cammino di peso massimo dell artista {sol_ott_list[0][0]}"))
                    self._view.txt_result.controls.append(ft.Text(f"Lunghezza {len(sol_ott_list)}"))
                    for e in sol_ott_list:
                        self._view.txt_result.controls.append(ft.Text(f"{e[0]}, {e[2]}"))
                    self._view.txt_result.controls.append(ft.Text(f"Peso massimo {peso_ott}"))

                    self._view.update_page()

            except ValueError:
                self.alarm_not_correct_1()

        else:
            self.alarm_not_correct_1()





    '''                                                                True                 False
        .isdigit()	    numeri interi 0-9                            "123"	                "12.3", "-5", "abc"
        .isnumeric()	Numeri, frazioni, numeri romani         	"½", "123"	            "12.3", "-5"
        .isdecimal()	Solo cifre,decimali pure	                "123"	                "²" (esponente), "-5"'''


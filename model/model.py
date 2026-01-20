import networkx as nx
from database.dao import DAO

class Model:
    def __init__(self):
        self._G = nx.Graph()



    def load_artists(self, n_alb):
        self.artists = DAO.get_artists(n_alb)           #id , name
        #print(self.artists)
        return self.artists

    def load_artists_genre(self):
        self.tuple_artists = {}
        self.artists_genre = DAO.get_tuple_artists()
        for r in self.artists_genre:
            self.tuple_artists[(r['id_1'], r['id_2'])] =  r['tot_generi']
        #print(self.tuple_artists)
        return self.tuple_artists

    def get_nodes(self):
        self.nodes= []
        for a in self.artists:
            self.nodes.append(a['id'])
        self._G.add_nodes_from(self.nodes)
        return self.nodes

    def get_edges(self):
        self.edges = []
        self.load_artists_genre()


        tuple_art_filtered =  []        #possibili tuple con artisti filtrati
        for e in self.artists:
            for f in self.artists:
                if e['id'] != f['id']:
                    tuple_art_filtered.append((e['id'], f['id']))
                else:
                    print('')

        self.tuple_id_result =[]

        for i in tuple_art_filtered:    #i: tupla
            try:
                 #weigth dell arco
                w= self.tuple_artists[i]
                self.tuple_id_result.append((i, w))
            except KeyError:
                print('')
        for a,b in self.tuple_id_result:
            print(a, b)


        #prof mi può dire che cosa ho sbagliato qua sotto (commentato in verde), perche mi ha fatto perdere una quantità di tempo incredibile,
        #quindi sono giunto a scrivere alternativamente lo script qua sopra
        '''
        for a,b in self.tuple_artists.items():      #a: key b : value
            first = ''
            second = ''



            if a[0] ==(e['id'] for e in self.artists):
                print('ok')
                first = a[0]

                print(f'----{first}')
                
            if (a[1] ==(e['id'] for e in self.artists)):
                second = a[1]

            w = self.tuple_artists[(first, second)].value

            self.tuple_id_result.append((first, second, w)'''




    def load_artists_with_min_albums(self, min_albums):
        pass

    def build_graph(self):
        self.get_nodes()
        self.get_edges()


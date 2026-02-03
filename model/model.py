import networkx as nx
from database.dao import DAO


class Model:
    def __init__(self):
        self.artists = []           #list of ids
        self.id_gen = {}

        self.tuples = []    # (id, genere)
        self.id_name = []   # (id, name)
        self.triples1 = []       # ( n,n, w) to build graph
        self.G = nx.Graph()
        self.triples2 = []          #( id, name , w) to output punto 2
        self.id_art = None


    def load_artists(self, n_alb):            #output : {'id': 73}
        output = DAO.get_artists_gen(n_alb)
        for e in output:
            if e['id'] not in self.artists:
                self.artists.append(e['id'])                    #solo id artisti
        '''self.id_gen = {a['id']: a['genere'] for a in output}'''
        for e in output:
            self.tuples.append((e['id'], e['genere'] ))    #dict con key = tupla (id artista , genere)'''

        for e in output:
            if (e['id'], e['name']) not in self.id_name: self.id_name.append((e['id'], e['name'] ))

        return self.artists, self.tuples

    def build_graph(self,n_alb):
        self.load_artists(n_alb)

        art_map = {}            # art : [gen, gen, gen]
        for art, gen in self.tuples:
            if art not in art_map:
                art_map[art] = set()
            art_map[art].add(gen)
        print(art_map)
        for i  in range(len(self.artists)):         # i : 0 ,1 ,2
            for j in range(i+1,len(self.artists)):          # j : 1 ,2 ,3
                art1 = self.artists[i]
                art2 = self.artists[j]
                comuni = art_map[art1] & art_map[art2]

                if len(comuni) > 0:
                    print(f' w : {len(comuni)}')
                    self.triples1.append((art1, art2, len(comuni)))

        self.G.add_nodes_from(self.artists)
        self.G.add_weighted_edges_from(self.triples1)


        return len(list(self.G.nodes)), len(list(self.G.edges)), self.id_name

    def neigh_art(self, input):     #input = name art
        for a in self.id_name:
            if input == a[1]:
                self.id_art = a[0]
                                   #n0 = nodo partenza = id_art
        #for n,w in self.G[id_art].items():      #n = neigh di n0, w dict attr  (n0-n_neigh) = e
        id_neigh_weight=[]
        for n in list(self.G.neighbors(self.id_art)):
            print(self.G[self.id_art][n]['weight'])
            id_neigh_weight.append(( n ,self.G[self.id_art][n]['weight'] ))

            '''if isinstance(w, (set, list, tuple)):       #(v 3.6 networkx) w = {1, 3} oppure {1}
                peso = max(w)
            else:
                peso = w
            id_neigh_weight.append((n, peso))'''


        for n1 in id_neigh_weight:
            for n2 in self.id_name:
                if n1[0] == n2[0]:
                    self.triples2.append((n1[0], n2[1], n1[1]))
        return self.triples2

    def load_artist_track(self,n_alb_min, MinDuration):
        output = DAO.get_artist_track(int(n_alb_min), float(MinDuration))       #id artisti, con vincolo durata min soddisfatto
        output_list = []
        for e in output:
            output_list.append(e['id'])
        return output_list

    def build_ricerca(self, MaxArtists, MinDuration, n_alb_min):
        '''cammino peso massimo con lunghezza = n_art , n0 = art1, artisti  con almeno una canzone durata
        minima quella in input, (conversione), in cammini artisto solo una volta presente,
        '''

        output_list = self.load_artist_track(n_alb_min, MinDuration)
        print(output_list)
        self.nodes = list(self.G.nodes)
        self.edges = list(self.G.edges)

        n0=self.id_art
        self.peso_ott = 0
        self.sol_ott_list = []

        self.ricorsione(n0, [n0], [], output_list, MaxArtists)

        print(f' soluzione ottima {self.sol_ott_list}')
        return self.peso_ott, self.sol_ott_list

    def ricorsione(self, node, partial_nodes, partial_edges, output_list, MaxArtists):
        # update
        list_w =[e[2] for e in partial_edges]

        peso_cur = sum (w for w in list_w)
        if peso_cur > self.peso_ott:
            self.peso_ott = peso_cur
            self.sol_ott_list = list(partial_edges)  # list di edges  con d (lista triplette)

        if len(partial_edges) >= int(MaxArtists):
            return

        for n in list(self.G.neighbors(node)):
            if n in output_list:            #vincolo durata min track
                if n not in partial_nodes:
                    if not partial_edges:        # prima condition per 1' round
                        w = self.G[node][n]['weight']
                        partial_edges.append((node, n, w))
                        partial_nodes.append(n)
                        self.ricorsione(n, partial_nodes, partial_edges, output_list, MaxArtists)
                    else:       #da 2' round in poi
                        w = self.G[node][n]['weight']
                        if w :
                            partial_edges.append((node, n, w))
                            partial_nodes.append(n)

                            self.ricorsione(n, partial_nodes, partial_edges, output_list, MaxArtists)

                            partial_edges.pop()
                            partial_nodes.pop()


    #versione networkx 3.5






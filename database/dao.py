from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_artists(n_alb):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT alb.artist_id as id, name
FROM album alb, artist a
where alb.artist_id = a.id 
group by alb.artist_id having count(alb.id) >= %s"""
        cursor.execute(query, (n_alb,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result


    #salvo tupla artisti con stesso genere
    @staticmethod
    def get_tuple_artists():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """SELECT  al.artist_id as id_1, tab.artista2 as id_2, COUNT(*) as tot_generi
FROM track t, album al, (select t2.genre_id as genere2, al2.artist_id as artista2
							from  track t2, album al2
							where t2.album_id = al2.id ) as tab
where  t.album_id = al.id and t.genre_id = tab.genere2 
group by al.artist_id, tab.artista2 having al.artist_id <> tab.artista2 

"""

        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result



    '''
    @staticmethod
    def get_album(durata):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.id as id
                    from album a
                        where a.id IN (select t.album_id
                                   from track t
                                   group by t.album_id \
                                   having sum(milliseconds) > %s * 60000) \
                """
        cursor.execute(query, (durata,))
        for row in cursor:
            # result[row['id']] = row['titolo']
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_playlist():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select distinct t1.album_id as a1, a.album_id as a2
                   from playlist_track p1
                            join track t1 on p1.track_id = t1.id
                            join (select p2.playlist_id, t2.album_id
                                  from playlist_track p2
                                           join track t2 on p2.track_id = t2.id) a on p1.playlist_id = a.playlist_id
                   where t1.album_id <> a.album_id"""
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_album_info():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select t.album_id as id, a.title as title, sum(milliseconds) / 60000 as durata
                   from album a, \
                        track t
                   where t.album_id = a.id
                   group by t.album_id \
                """
        cursor.execute(query)
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result'''
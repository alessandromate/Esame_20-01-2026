from database.DB_connect import DBConnect
from model.artist import Artist

class DAO:

    @staticmethod
    def get_artists_gen(n_alb):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select ar.id as id, ar.name as name, t.genre_id as genere
                    from (select a.id as id
                    from artist a, album al 
                    where al.artist_id = a.id 
                    group by a.id having count(*) >= %s) as sub, track t, album alb, artist ar
                    where t.album_id = alb.id and alb.artist_id  = ar.id and sub.id = ar.id
                    group by ar.id, t.genre_id 
                        """
        cursor.execute(query, (n_alb,))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_artist_track( n_alb_min, MinDuration):
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """select ar.id as id
                    from (select a.id as id
                    from artist a, album al 
                    where al.artist_id = a.id 
                    group by a.id having count(*) >= %s) as sub, track t, album alb, artist ar
                    where t.album_id = alb.id and alb.artist_id  = ar.id and sub.id = ar.id and t.milliseconds /60000 >= %s
                    group by ar.id
                                """
        cursor.execute(query, (n_alb_min, MinDuration, ))
        for row in cursor:
            result.append(row)
        cursor.close()
        conn.close()
        return result







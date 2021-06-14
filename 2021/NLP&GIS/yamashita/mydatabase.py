import psycopg2

def connect():
    con = psycopg2.connect("host=" + "localhost" +
                           " port=" + "5432" +
                           " dbname=" + "touristspot" +
                           " user=" + "postgres" +
                           " password=" + "yamashita")
    return con

def select_execute(con, sql):
    with con.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()

    return rows

if __name__ == '__main__':

    # print('input spot title:',end='')
    title=input()
    print(title)

    con = connect()
    cur = con.cursor()
    cur.execute("SELECT title,lead,overview,latitude,longitude,spotaddress FROM wikidata WHERE title='" +title+ "';")
    results = cur.fetchall()

    #output result
    print(results)

    cur.close()
    con.close()
#!/usr/bin/env python

import psycopg2

DBNAME = 'news'


def query(sql, db_conn, the_tail):
    """
    query function returns the results of an SQL query.

    query function takes the following parameters.
    args:
    sql - an SQL query statement to be executed.
    db_conn - a DB connection session.
    the_tail - a string passed in for printing.

    returns:
    A list of tuples containing the results of the query.
    """
    try:
        cursor = db_conn.cursor()
        cursor.execute(sql)
        sql_result = cursor.fetchall()

        for row in sql_result:
            print row[0] + ' - ' + str(row[1]) + the_tail

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection
        if (db_conn):
            cursor.close()


def main():
    conn = psycopg2.connect(database=DBNAME)
    sql1 = """SELECT b.title, COUNT(b.title) num
              FROM articles b, log c
              WHERE b.slug = substr(c.path, 10, length(c.path))
              GROUP BY b.title
              ORDER BY num desc
              LIMIT 3"""
    sql2 = """SELECT a.name, COUNT(b.title) num
              FROM authors a, articles b, log c
              WHERE a.id = b.author AND
              b.slug = substr(c.path, 10)
              GROUP BY a.name
              ORDER BY num desc"""

    print("""\nQuestion #1:
    What are the most popular three articles of all time?""")
    query(sql1, conn, " views")

    print("""\nQuestion #2:
    Who are the most popular article authors of all time?""")
    query(sql2, conn, " views")

    print("""\nQuestion #3:
    On which days did more than 1% of requests lead to errors?""")
    with open('query3.sql', 'r') as file:
        sql3 = file.read().strip()
        file.close()
    query(sql3, conn, " errors")
    conn.close()


if __name__ == "__main__":
    main()

import psycopg2

def create_data_base(name_postgres_base, user_postgres, password_postgres, name_DB):
    conn = psycopg2.connect(database=f'{name_postgres_base}', user=f'{user_postgres}', password=f'{password_postgres}')
    cur = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {name_DB}"
    cur.execute(sql)
    print(f'Ваша база данных {name_DB} создана')
    cur.close()
    conn.close()

def create_table_bd(name_db, user_postgres, password_postgres):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE  client(id_client SERIAL PRIMARY KEY,
                     name VARCHAR(30) NOT NULL,
                     lastname VARCHAR(50) NOT NULL);
                    """)
        cur.execute("""
        CREATE TABLE phone(id_phone SERIAL PRIMARY KEY,
                     phone_number VARCHAR(23),
                     id_client INT REFERENCES client(id_client));
                    """)
        cur.execute("""
        CREATE TABLE  email(id_mail SERIAL PRIMARY KEY,
                     email VARCHAR(50),
                     id_client INT REFERENCES client(id_client));
        """)
    print(f'Ваши таблицы созданы')
    conn.commit()
    conn.close()

def insert_new_client(name_db, user_postgres, password_postgres, name_client, lastname_client, number_phone = 'Отсутствует', client_mail = 'Отсутствует'):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, lastname)
        VALUES(%s, %s);
                """, (name_client, lastname_client))
        cur.execute("""SELECT id_client
        FROM client           
        """)
        temp_var = cur.fetchone()[0]
        cur.execute("""
                INSERT INTO phone(phone_number, id_client)
                VALUES(%s,%s);
                """, (number_phone,temp_var ))
        cur.execute("""
                        INSERT INTO email(email)
                        VALUES(%s);
                        """, (client_mail, ))

        conn.commit()
        conn.close()

def insert_new_phone(name_db, user_postgres, password_postgres, lastname_client, number_phone):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute("""
                        SELECT id_client
                        FROM client
                        WHERE lastname = %s
                        """, (lastname_client, ))
        select_id = cur.fetchone()[0]
        cur.execute(f"""INSERT INTO phone(phone_number, id_client)
                        VALUES (%s,%s)""",(number_phone,select_id))
        conn.commit()
        conn.close()

def update_info_client(name_db, user_postgres, password_postgres, lastname_client, number_phone, email,):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute("""
                        SELECT id_client
                        FROM client
                        WHERE lastname = %s
                        """, (lastname_client, ))
        select_id = cur.fetchone()[0]
        cur.execute(f"""UPDATE phone SET (phone_number, id_client)
                        VALUES (%s,%s)""",(number_phone,select_id))
        conn.commit()
        conn.close()
#create_data_base('postgres', 'postgres', 'root', 'test_db')
#create_table_bd('test_db','postgres','root')
#insert_new_client('test_db','postgres','root','Гоша', 'Пупкин', '8-050-443-31-22','jdукdj@asd.vy')
#insert_new_phone('test_db','postgres','root', 'Пупкин','75554-645')

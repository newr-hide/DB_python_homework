import psycopg2
# Задание выполненное в виде функций
#Функция создающая саму базу
def create_data_base(name_postgres_base, user_postgres, password_postgres, name_DB):
    conn = psycopg2.connect(database=f'{name_postgres_base}', user=f'{user_postgres}', password=f'{password_postgres}')
    cur = conn.cursor()
    conn.autocommit = True
    sql = f"CREATE DATABASE {name_DB}"
    cur.execute(sql)
    print(f'Ваша база данных {name_DB} создана')
    cur.close()
    conn.close()

# Функция, создающая структуру БД (таблицы).
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

# Функция, позволяющая добавить нового клиента.
def insert_new_client(name_db, user_postgres, password_postgres, name_client, lastname_client, number_phone = 'Отсутствует', client_mail = 'Отсутствует'):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(name, lastname)
        VALUES(%s, %s);
                """, (name_client, lastname_client))
        cur.execute("""SELECT id_client
        FROM client
        WHERE lastname =  %s         
        """, (lastname_client,))
        temp_var = cur.fetchone()[0]
        cur.execute("""
                INSERT INTO phone(phone_number, id_client)
                VALUES(%s,%s);
                """, (number_phone,temp_var ))
        cur.execute("""
                        INSERT INTO email(email, id_client)
                        VALUES(%s,%s);
                        """, (client_mail,temp_var ))

        conn.commit()
        conn.close()

# Функция, позволяющая добавить телефон для существующего клиента.
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
        print('Телефон успешно добавлен')
        conn.commit()
        conn.close()
# Функция, позволяющая изменить данные о клиенте.
def update_info_client(name_db, user_postgres, password_postgres, id_client,name_client=None, lastname_client=None, number_phone=None, email=None,):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:

        if name_client != None:
            cur.execute(""" UPDATE client SET name=%s WHERE id_client=%s """, (name_client,id_client))
            print('Имя клиента успешно заменено')
        elif lastname_client != None:
            cur.execute(""" UPDATE client SET lastname=%s WHERE id_client=%s """, (lastname_client,id_client))
            print('Фамилия клиента успешно заменена')
        elif email != None:
            cur.execute(""" UPDATE email SET email=%s WHERE id_client=%s""", (email, id_client))
            print('Емайл успешно заменен')
        elif number_phone != None:
            cur.execute(f"""UPDATE phone SET phone_number=%s WHERE id_client=%s """, (number_phone,id_client ))
            print('Номер успешно изменен')
        else:
            print('Нечего менять! Задайте параметр замены')

        conn.commit()
        conn.close()
# Функция, позволяющая удалить телефон для существующего клиента.
def remove_phone_client(name_db, user_postgres, password_postgres, id_client, number_phone):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute(""" 
        DELETE FROM phone WHERE id_client=%s AND phone_number = %s """, (id_client, number_phone ))
        print('Телефон успешно удален')
    conn.commit()
    conn.close()
#Функция, позволяющая удалить существующего клиента.

def remove_client(name_db, user_postgres, password_postgres, id_client):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        cur.execute(""" 
                    DELETE FROM email WHERE id_client=%s """, (id_client,))
        cur.execute(""" 
                    DELETE FROM phone WHERE id_client=%s """, (id_client,))
        cur.execute(""" 
            DELETE FROM client WHERE id_client=%s """, (id_client, ))
        print('Клиент успешно удален')
    conn.commit()
    conn.close()

# Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def search_client(name_db, user_postgres, password_postgres, name_client=None, lastname_client=None, number_phone=None, email=None):
    conn = psycopg2.connect(database=f'{name_db}', user=f'{user_postgres}', password=f'{password_postgres}')
    with conn.cursor() as cur:
        if name_client != None:
            cur.execute(""" 
            SELECT * FROM client 
            JOIN phone ON client.id_client = phone.id_client 
            JOIN email ON client.id_client = email.id_client 
            WHERE name=%s;
            """, (name_client,))
            temp_var = cur.fetchall()
            print(temp_var)
            print(f'Имя клиента: {temp_var[0][1]}\nФамилия Клиента: {temp_var[0][2]}\nНомер телефона:{temp_var[0][4]}\nEmail:{temp_var[0][7]}')

        elif lastname_client != None:
            cur.execute(""" 
                        SELECT * FROM client
                        JOIN phone ON client.id_client = phone.id_client 
                        JOIN email ON client.id_client = email.id_client 
                        WHERE lastname=%s;""", (lastname_client,))
            temp_var = cur.fetchall()

            print(f'Имя клиента: {temp_var[0][1]}\nФамилия Клиента: {temp_var[0][2]}\nНомер телефона:{temp_var[0][4]}\nEmail:{temp_var[0][7]}')


        elif number_phone != None:
            cur.execute(""" 
                        SELECT * FROM phone
                        JOIN client ON phone.id_client = client.id_client
                        JOIN email ON phone.id_client = email.id_client
                        WHERE phone_number=%s;""", (number_phone,))
            temp_var = cur.fetchall()
            print(f'Имя клиента: {temp_var[0][4]}\nФамилия Клиента: {temp_var[0][5]}\nНомер телефона:{temp_var[0][1]}\nEmail: {temp_var[0][7]}')

        elif email != None:
            cur.execute("""
            SELECT * FROM email 
            JOIN client ON email.id_client = client.id_client
            JOIN phone ON email.id_client = phone.id_client
            WHERE email=%s;
                        """, (email,))
            temp_var = cur.fetchall()
            print(f'Имя клиента: {temp_var[0][4]}\nФамилия Клиента: {temp_var[0][5]}\nНомер телефона:{temp_var[0][7]}\nEmail: {temp_var[0][1]}')
        else:
            print('Вы не ввели параметр поиска')


#create_data_base('postgres', 'postgres', 'root', 'test_db')
#create_table_bd('test_db','postgres','root')
#insert_new_client('test_db','postgres','root','Андрей', 'Кирх', '8-64548-22')
#insert_new_phone('test_db','postgres','root', 'Кирх','7445')
#update_info_client('test_db','postgres','root',1, number_phone=8923555455)
#update_info_client('test_db','postgres','root',2,email='kfjgfdkf@s;dl')
#update_info_client('test_db','postgres','root',2,lastname_client='Дерюгина')
#update_info_client('test_db','postgres','root',2,name_client='Маруся')
#update_info_client('test_db','postgres','root',2)
#remove_phone_client('test_db','postgres','root',5,'7445')
#remove_client('test_db','postgres','root',1)
#search_client('test_db','postgres','root','Андрей')
#search_client('test_db','postgres','root',lastname_client='Веселина')
#search_client('test_db','postgres','root',number_phone='86453')
#search_client('test_db','postgres','root',email='kfjgfdkf@s;dl')


class Working_with_a_DB:
    def __init__(self):
        self.conn = None
    def create_data_base(self, name_postgres_base, user_postgres, password_postgres, name_DB):
        self.conn = psycopg2.connect(database=f'{name_postgres_base}', user=f'{user_postgres}', password=f'{password_postgres}')
        cur = self.conn.cursor()
        self.conn.autocommit = True
        sql = f"CREATE DATABASE {name_DB}"
        cur.execute(sql)
        print(f'Ваша база данных {name_DB} создана')
        cur.close()
        self.conn.close()

    def connect(self,name_db, user, password):
        try:
            self.conn = psycopg2.connect(database=name_db, user=user, password=password)
        except Exception as e:
            print("Ошибка подключения к базе данных:", e)
            return False
        print('Подкючение к Базе Данных удачно')
        return True
    def create_table_bd(self):
        with self.conn.cursor() as cur:
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
        self.conn.commit()
        self.conn.close()

    def insert_new_client(self, name_client, lastname_client, number_phone='Отсутствует', client_mail='Отсутствует'):

        with self.conn.cursor() as cur:
            cur.execute("""
            INSERT INTO client(name, lastname)
            VALUES(%s, %s);
                    """, (name_client, lastname_client))
            cur.execute("""SELECT id_client
            FROM client
            WHERE lastname =  %s         
            """, (lastname_client,))
            temp_var = cur.fetchone()[0]
            cur.execute("""
                    INSERT INTO phone(phone_number, id_client)
                    VALUES(%s,%s);
                    """, (number_phone, temp_var))
            cur.execute("""
                            INSERT INTO email(email, id_client)
                            VALUES(%s,%s);
                            """, (client_mail, temp_var))
            print('Данные клиента успешно занесены в базу данных')
            self.conn.commit()
            self.conn.close()

    def insert_new_phone(self, lastname_client, number_phone):
        with self.conn.cursor() as cur:
            cur.execute("""
                            SELECT id_client
                            FROM client
                            WHERE lastname = %s
                            """, (lastname_client,))
            select_id = cur.fetchone()[0]
            cur.execute(f"""INSERT INTO phone(phone_number, id_client)
                            VALUES (%s,%s)""", (number_phone, select_id))
            print('Телефон успешно добавлен')
            self.conn.commit()
            self.conn.close()

    def update_info_client(self, id_client, name_client=None, lastname_client=None,
                           number_phone=None, email=None, ):
        with self.conn.cursor() as cur:

            if name_client != None:
                cur.execute(""" UPDATE client SET name=%s WHERE id_client=%s """, (name_client, id_client))
                print('Имя клиента успешно заменено')
            elif lastname_client != None:
                cur.execute(""" UPDATE client SET lastname=%s WHERE id_client=%s """, (lastname_client, id_client))
                print('Фамилия клиента успешно заменена')
            elif email != None:
                cur.execute(""" UPDATE email SET email=%s WHERE id_client=%s""", (email, id_client))
                print('Емайл успешно заменен')
            elif number_phone != None:
                cur.execute(f"""UPDATE phone SET phone_number=%s WHERE id_client=%s """, (number_phone, id_client))
                print('Номер успешно изменен')
            else:
                print('Нечего менять! Задайте параметр замены')

            self.conn.commit()
            self.conn.close()

    def remove_phone_client(self, id_client, number_phone):

        with self.conn.cursor() as cur:
            cur.execute(""" 
            DELETE FROM phone WHERE id_client=%s AND phone_number = %s """, (id_client, number_phone))
            print('Телефон успешно удален')
        self.conn.commit()
        self.conn.close()

    def remove_client(self, id_client):
        with self.conn.cursor() as cur:
            cur.execute(""" 
                        DELETE FROM email WHERE id_client=%s """, (id_client,))
            cur.execute(""" 
                        DELETE FROM phone WHERE id_client=%s """, (id_client,))
            cur.execute(""" 
                DELETE FROM client WHERE id_client=%s """, (id_client,))
            print('Клиент успешно удален')
        self.conn.commit()
        self.conn.close()

    def search_client(self, name_client=None, lastname_client=None, number_phone=None, email=None):

        with self.conn.cursor() as cur:
            if name_client != None:
                cur.execute(""" 
                SELECT * FROM client 
                JOIN phone ON client.id_client = phone.id_client 
                JOIN email ON client.id_client = email.id_client 
                WHERE name=%s;
                """, (name_client,))
                temp_var = cur.fetchall()

                print(
                    f'Имя клиента: {temp_var[0][1]}\nФамилия Клиента: {temp_var[0][2]}\nНомер телефона:{temp_var[0][4]}\nEmail:{temp_var[0][7]}')

            elif lastname_client != None:
                cur.execute(""" 
                            SELECT * FROM client
                            JOIN phone ON client.id_client = phone.id_client 
                            JOIN email ON client.id_client = email.id_client 
                            WHERE lastname=%s;""", (lastname_client,))
                temp_var = cur.fetchall()

                print(
                    f'Имя клиента: {temp_var[0][1]}\nФамилия Клиента: {temp_var[0][2]}\nНомер телефона:{temp_var[0][4]}\nEmail:{temp_var[0][7]}')


            elif number_phone != None:
                cur.execute(""" 
                            SELECT * FROM phone
                            JOIN client ON phone.id_client = client.id_client
                            JOIN email ON phone.id_client = email.id_client
                            WHERE phone_number=%s;""", (number_phone,))
                temp_var = cur.fetchall()
                print(
                    f'Имя клиента: {temp_var[0][4]}\nФамилия Клиента: {temp_var[0][5]}\nНомер телефона:{temp_var[0][1]}\nEmail: {temp_var[0][7]}')

            elif email != None:
                cur.execute("""
                SELECT * FROM email 
                JOIN client ON email.id_client = client.id_client
                JOIN phone ON email.id_client = phone.id_client
                WHERE email=%s;
                            """, (email,))
                temp_var = cur.fetchall()
                print(
                    f'Имя клиента: {temp_var[0][4]}\nФамилия Клиента: {temp_var[0][5]}\nНомер телефона:{temp_var[0][7]}\nEmail: {temp_var[0][1]}')
            else:
                print('Вы не ввели параметр поиска')
        self.conn.commit()
        self.conn.close()

#createDB = Working_with_a_DB()
#create_base = createDB.create_data_base('postgres','postgres','root','wowdb')
#createDB.connect('wowdb','postgres','root')
#createDB.create_table_bd()
#createDB.insert_new_client('Андрей', 'Кирх', '8-64548-22')
#createDB.insert_new_phone('Кирх','744354-645')
#createDB.update_info_client(1,number_phone=9874566)
#createDB.remove_phone_client(1,'987466')
#createDB.remove_client(1)
#createDB.search_client(name_client='Андрей')
import psycopg2


conn = psycopg2.connect(database="Homework_pysql", user="postgres", password="1693107")

#Функция, создающая структуру БД (таблицы).
def create_db():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients(
            id SERIAL PRIMARY KEY,
            name text,
            surname text,
            email text
            );
            """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Phone_number(
            Phone_number_id SERIAL PRIMARY KEY,
            Client_id integer not null references clients(id),
            Phone_number text UNIQUE not null
            );
            """)
    conn.commit()


#Функция, позволяющая добавить нового клиента.
def add(first_name, last_name, email, phone_number=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(name,surname,email) VALUES(%s, %s, %s) RETURNING id;
            """, (first_name, last_name, email,))
        id = cur.fetchone()
        print(id)
        if phone_number != None:
            cur.execute("""
                INSERT INTO Phone_number(Client_id,Phone_number) VALUES(%s, %s);
                """, (id, phone_number,))
    conn.commit()
        

#Функция, позволяющая добавить телефон для существующего клиента.
def add_phone(id,phone_number):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO Phone_number(Client_id, Phone_number) VALUES(%s, %s);
            """, (id, phone_number,))
        conn.commit()


#Функция, позволяющая изменить данные о клиенте.
def change_client(id, name=None, surname=None, email=None, Phone_number=None, old_phone=None):
    if name !=None:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clients SET name=%s where id=%s;
                """, (name, id,))
            conn.commit()
    if surname !=None:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clients SET surname=%s where id=%s;
                """, (surname, id,))
            conn.commit()
    if email !=None:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE clients SET email=%s where id=%s;
                """, (email, id,))
            conn.commit()
    if Phone_number != None and old_phone != None:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE Phone_number SET Phone_number=%s where id=%s and Phone_number=%s;
                """, (Phone_number, id, old_phone,))
            conn.commit()
    

#Функция, позволяющая удалить телефон для существующего клиента.
def delete_phone(client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Phone_number WHERE Client_id=%s and phone_number=%s;
        """, (client_id,phone,))
        conn.commit()


#Функция, позволяющая удалить существующего клиента.
def delete_client(client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM Phone_number WHERE Client_id=%s;
        """, (client_id,))
        conn.commit()
        cur.execute("""
        DELETE FROM clients WHERE id=%s;
        """, (client_id,))
        conn.commit()


#Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.
def find_client(name=None, surname=None, email=None, phone=None):
    with conn.cursor() as cur:
        if phone != None:
            cur.execute("""
            SELECT a.id, a.name, a.surname, a.email, b.phone_number
            from clients a
            left join Phone_number b on a.id = b.Client_id
            WHERE b.phone_number=%s;
            """, (phone,))
            print(cur.fetchall())
        else:
            params = {'name':name,
                    'surname':surname,
                    'email':email}
            querry = "SELECT id, name, surname, email from clients where 1=1"
            for key, value in params.items():
                if value != None:
                    querry += f" and {key}='{value}'"
            cur.execute(querry)
            print(cur.fetchall())
        


create_db()
add('Андрей', 'Иванов', 'mail1@yandex.ru', '+1234567890')
add('Роман', 'Ерашов', 'mail7@yandex.ru', '+4562349871')
add('Илья', 'Петров', 'mail2@yandex.ru', '+63454859457')
add('Александр', 'Пятков', 'mail3@yandex.ru', '+9876453287')
add('Никита', 'Адрианов', 'mail4@yandex.ru', '+9876543210')
add('Руслан', 'Замоскворецкий', 'mail5@yandex.ru')
add_phone(4,'+111111111111')
add_phone(5,'+111111111112')
add_phone(3,'+111111111113')
add_phone(3,'+111111111114')
add_phone(3,'+111111111115')
change_client(id=5, name='Имя', surname='Фамилия')
find_client(phone='+1234567890')
delete_phone(3, '+1234567890')
delete_client(5)
conn.close()
import csv
import datetime
import MySQLdb


def db_connector(func):
    def wrapper(*args, **kwargs):
        conn = MySQLdb.connect('localhost', 'root', 'root', 'vivid_seats')
        cursor = conn.cursor()
        try:
            res = func(cursor, *args, **kwargs)
            conn.commit()
            return res
        except Exception as ex:
            print ex
            conn.rollback()
        finally:
            conn.close()

    return wrapper

@db_connector
def populate_table_seller(cursor):
    stmt = 'INSERT INTO seller (seller_name) VALUES (%s)'
    data = [['seller 1'], ['seller 2'], ['seller 3'], ['seller 4'], 
            ['seller 5'], ['seller 6'], ['seller 7']]

    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

def get_ticket_records():
    '''Since the provided data is not big, so I directly have all data in a
       list, rather than have a nenerator.
    '''
    with open('sampleTickets1.csv') as csvfile:
        next(csvfile, None)
        csv_reader = csv.reader(csvfile, deleimiter=',')
        keys = set()
        res = []
        i = 1

        for r in csv_reader:
            k = '-'.join([r[0], str[i], r[1], r[4], r[3]])
            if k not in keys:
                res.append([int(r[0], i, int(r[1]), r[4], int(r[2]), 
                            round(float(r[3]), 2))])
                keys.add(k)
            i = i % 7 + 1

        return res

def get_event_ids(tickets):
    return list(set([i[0] for i in tickets]))

@db_connector
def populate_table_event(cursor, event_ids):
    stmt = '''INSERT INTO event (event_id, event_name, event_street,
                event_city, event_state, event_country, event_zip, event_time)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
           '''
    data = []
    for i in range(len(event_ids)):
        data.append([event_ids[i],
                     'event %s' % event_ids[i],
                     'event %s' % event_ids[i],
                     'event %s' % event_ids[i],
                     'event %s' % event_ids[i],
                     'US',
                     '60601',
                     datetime.datetime.strptime('12/07/2018 18:00:00',
                        '%m%d%Y %H:%M:%S') + datetime.timedelta(days=i)
                    ])

    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

@db_connector
def populate_table_ticket(cursor, data):
    stmt = '''INSERT INTO ticket (event_id, seller_id, ticket_section,
                ticket_row, ticket_quantity, ticket_price)
              VALUES (%s, %s, %s, %s, %s, %s)'''
    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

@db_connector
def populate_table_referal(cursor):
    stmt = 'INSERT INTO referal (referal_name) VALUES (%s)'
    data = [['direct'], ['google'], ['espn']]
    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

@db_connector
def populate_table_customer(cursor):
    stmt = '''INSERT INTO customer (customer_name, customer_street,
                customer_city, customer_state, customer_country,
                customer_zip, customer_phone, customer_email,
                referal_id)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

    data = []
    for i in range(5):
        data.append(['customer %s' % str(i+1),
                     'customer street %s' % str(i+1),
                     'customer city %s' % str(i+1),
                     'customer state %s' % str(i+1),
                     'customer phone %s' % str(i+1),
                     'customer email %s' % str(i+1),
                     'US',
                     '60601',
                     i % 3 + 1
                    ])
    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

@db_connector
def populate_table_order_status(cursor):
    stmt = 'INSERT INTO order_status (status_name) VALUES (%s)'
    data = [['SUCCESS'], ['REFUND']]
    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

@db_connector
def get_ticket_count(cursor):
    stmt = 'SELECT count(0) FROM ticket'
    try:
        cursor.execute(stmt)
        res = cursor.fetchone()
        return res
    except Exception as ex:
        raise ex

@db_connector
def get_ticket_price(cursor, ticket_id):
    stmt = 'SELECT ticket_price FROM ticket WHERE ticket_id = %s' % ticket_id
    try:
        cursor.execute(stmt)
        res = cursor.fetchone()
        return res
    except Exception as ex:
        raise ex

@db_connector
def populate_table_order(cursor):
    stmt = '''INSERT INTO `order` (customer_id, referal_id, 
                ticket_id, order_quantity, order_total_price, order_status)
              VALUES (%s, %s, %s, %s, %s, %s)'''
    data = []
    ticket_count = get_ticket_count()
    if ticket_count:
        for i in range(10):
            data.append([i%5 + 1,  
                         i%3 + 1,
                         i%ticket_count[0] + 1,
                         1,
                         get_ticket_price(i%ticket_count[0] + 1),
                         1
                        ])

    try:
        cursor.executemany(stmt, data)
    except Exception as ex:
        raise ex

def main():
    populate_table_seller()
    ticket = get_ticket_records()

    if ticket:
        event_ids = get_event_ids(tickets)
        populate_table_event(event_ids)
        populate_table_ticket(tickets)

        populate_table_referal()
        populate_table_customer()
        populate_table_order_status()
        populate_table_order()


if __name__ == '__main__':
    main()

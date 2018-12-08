__author__ = 'carson.qin'

from Challenge import db
from sqlalchemy import create_engine


class Event(db.Model):
    __tablename__ = 'event'
    __bind_key__ = 'vivid_seats'

    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String)
    event_street = db.Column(db.String)
    event_city = db.Column(db.String)
    event_state = db.Column(db.String)
    event_country = db.Column(db.String)
    event_zip = db.Column(db.String)
    event_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime)

    def __init__(self, event_info):
        self.event_id = event_info.get('event_id')
        self.event_name = event_info.get('event_name')
        self.event_street = event_info.get('event_street')
        self.event_city = event_info.get('event_city')
        self.event_state = event_info.get('event_state')
        self.event_country = event_info.get('event_country')
        self.event_zip = event_info.get('event_zip')
        self.event_time = event_info.get('event_time')
        self.create_time = event_info.get('create_time')
        self.event_id = event_info.get('event_id')


class Ticket(db.Model):
    __tablename__ = 'ticket'
    __bind_key__ = 'vivid_seats'

    ticket_id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer)
    seller_id = db.Column(db.Integer)
    ticket_section = db.Column(db.Integer)
    ticket_row = db.Column(db.String)
    ticket_quantity = db.Column(db.Integer)
    ticket_price = db.Column(db.Float)

    def __init__(self, ticket_info):
        self.ticket_id = ticket_info.get('ticket_id')
        self.event_id = ticket_info.get('event_id')
        self.seller_id = ticket_info.get('seller_id')
        self.ticket_section = ticket_info.get('ticket_section')
        self.ticket_row = ticket_info.get('ticket_row')
        self.ticket_quantity = ticket_info.get('ticket_quantity')
        self.ticket_price = ticket_info.get('ticket_price')

    def insert_on_duplicate(self):
        try:
            db_connect = create_engine('mysql://root:root@localhost/vivid_seats')
            db_connect.connect().execute(
                         '''INSERT INTO %s (event_id, seller_id, ticket_section, 
                            ticket_row, ticket_quantity, ticket_price)
                            VALUES (%s, %s, "%s", "%s", %s, %s)
                            ON DUPLICATE KEY UPDATE ticket_quantity=ticket_quantity+%s;
                         ''' % (self.__tablename__, self.event_id, self.seller_id, 
                                self.ticket_section, self.ticket_row,
                                self.ticket_quantity, self.ticket_price, self.ticket_quantity)
                         )
        except:
            raise

class Seller(db.Model):
    __tablename__ = 'seller'
    __bind_key__ = 'vivid_seats'

    seller_id = db.Column(db.Integer, primary_key=True)
    seller_name = db.Column(db.String)
    create_time = db.Column(db.DateTime)

    def __init__(self, seller_info):
        self.seller_id = seller_info.get('seller_id')
        self.seller_name = seller_info.get('seller_name')
        self.create_time = seller_info.get('create_time')

class Referal(db.Model):
    __tablename__ = 'referal'
    __bind_key__ = 'vivid_seats'

    referal_id = db.Column(db.Integer, primary_key=True)
    referal_name = db.Column(db.String)

    def __init__(self, referal_info):
        self.referal_id = referal_info.get('referal_id')
        self.referal_name = referal_info.get('referal_name')

class Customer(db.Model):
    __tablename__ = 'customer'
    __bind_key__ = 'vivid_seats'

    customer_id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    customer_street = db.Column(db.String)
    customer_city = db.Column(db.String)
    customer_state = db.Column(db.String)
    customer_country = db.Column(db.String)
    customer_zip = db.Column(db.String)
    customer_phone = db.Column(db.String)
    customer_email = db.Column(db.String)
    referal_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, customer_info):
        self.customer_id = customer_info.get('customer_id')
        self.customer_name = customer_info.get('customer_name')
        self.customer_street = customer_info.get('customer_street')
        self.customer_city = customer_info.get('customer_city')
        self.customer_state = customer_info.get('customer_state')
        self.customer_country = customer_info.get('customer_country')
        self.customer_zip = customer_info.get('customer_zip')
        self.referal_id = customer_info.get('referal_id')
        self.create_time = customer_info.get('create_time')

class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    __bind_key__ = 'vivid_seats'

    status_id = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String)

    def __init__(self, status_info):
        self.status_id = status_info.get('status_id')
        self.status_name = status_info.get('status_name')

class Order(db.Model):
    __tablename__ = 'order'
    __bind_key__ = 'vivid_seats'

    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    referal_id = db.Column(db.Integer)
    ticket_id = db.Column(db.Integer)
    order_quantity = db.Column(db.Integer)
    order_total_price = db.Column(db.Integer)
    order_status = db.Column(db.Integer)

    def __init__(self, order_info):
        self.order_id = order_info.get('order_id')
        self.customer_id = order_info.get('customer_id')
        self.referal_id = order_info.get('referal_id')
        self.ticket_id = order_info.get('ticket_id')
        self.order_quantity = order_info.get('order_quantity')
        self.order_total_price = order_info.get('order_total_price')
        self.order_status = order_info.get('order_status')

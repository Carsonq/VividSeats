__author__ = 'carson.qin'

import json

from flask import Blueprint, render_template, request, url_for, redirect
from sqlalchemy import and_
from Challenge import db
from sqlalchemy.exc import OperationalError, IntegrityError, ProgrammingError
from flask_jsonpify import jsonify

from .models import Event, Ticket, Seller, Referal, Customer, OrderStatus, Order
from .utils import error_json, data_json, success_json

tickets = Blueprint('tickets', __name__)


@tickets.route('/events/<int:event_id>/tickets', methods=['GET'])
def get_tickets(event_id):
    '''Get available tickets or the best ticket of an event
    '''
    if request.args.get('search') == 'best':
        return _get_best_ticket(event_id)

    return _get_available_tickets(event_id)

def _get_available_tickets(event_id):
    '''Get available tickets for an event
       The cheapest ticket(price) with closest section(section)
       should have a seat(row, not GA etc if applicable)
    '''
    res = {}
    fetch_res = Ticket.query.filter(and_(Ticket.event_id==event_id, Ticket.ticket_quantity>0)).all()
    for t in fetch_res:
        res[t.ticket_id] = {'quantity': t.ticket_quantity, 'price': t.ticket_price,
                            'section': t.ticket_section, 'row': t.ticket_row, 'seller': t.seller_id}
    return data_json(res)

def _get_best_ticket(event_id):
    '''Get the best ticket of an event
    '''
    res = {}
    ticket = Ticket.query.filter(and_(Ticket.event_id==event_id, Ticket.ticket_quantity>0,
        Ticket.ticket_row.op('regexp')(r'^[0-9]+$'))).order_by(Ticket.ticket_price, Ticket.ticket_section).first()
    if not ticket:
        ticket = Ticket.query.filter(and_(Ticket.event_id==event_id, 
            Ticket.ticket_quantity>0)).order_by(Ticket.ticket_price, Ticket.ticket_section).first()

    if ticket:
        res['section'] = ticket.ticket_section
        res['row'] = ticket.ticket_row
        res['price'] = ticket.ticket_price
        res['seller'] = ticket.seller_id

    return data_json(res)

@tickets.route('/sellers/<int:seller_id>/tickets', methods=['POST'])
def add_tickets(seller_id):
    '''Post a new ticket from a seller
    '''
    ticket_info = {}
    try:
        if request.data:
            data = json.loads(request.data)
        else:
            data = request.form
        ticket_info['seller_id'] = seller_id
        ticket_info['event_id'] = data.get('event_id')
        ticket_info['ticket_section'] = data.get('ticket_section')
        ticket_info['ticket_row'] = data.get('ticket_row')
        ticket_info['ticket_quantity'] = data.get('ticket_quantity')
        ticket_info['ticket_price'] = data.get('ticket_price')

        Ticket(ticket_info).insert_on_duplicate()

    except ValueError as ex:
        return error_json('Invalid Json')
    except (OperationalError, IntegrityError, ProgrammingError) as ex:
        return error_json('lack of necessary info or incorrect info')
    except Exception as ex:
        return error_json('unsuccess')
    
    return success_json('success')

@tickets.route('/ticket/<int:ticket_id>', methods=['PUT'])
def buy_one_ticket(ticket_id):
    '''Update a ticket to sold
    '''
    try:
        if request.data:
            data = json.loads(request.data)
        else:
            data = request.form
        referal_id = data.get('referal_id')
        customer_id = data.get('customer_id')

        ticket = Ticket.query.filter(Ticket.ticket_id==ticket_id).first()
        if ticket and ticket.ticket_quantity > 0:
            ticket.ticket_quantity -= 1

            db.session.add(Order({'customer_id': customer_id, 'referal_id': referal_id,
                                  'ticket_id': ticket_id, 'order_quantity': 1, 
                                  'order_total_price': ticket.ticket_price, 'order_status':1}))

            db.session.commit()
        elif not ticket:
            return error_json('No such ticket')
        else:
            return error_json('Out of stock')
    except ValueError as ex:
        return error_json('Invalid Json')
    except (OperationalError, IntegrityError, ProgrammingError) as ex:
        db.session.rollback()
        return error_json('lack of necessary info or incorrect info')
    except Exception as ex:
        db.session.rollback()
        return error_json("unsuccess")
    
    return success_json("success")

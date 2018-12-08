import requests
import sys
import json


def test_get_available_tickets(event_id):
    '''available case 162, 164, 107
    '''
    r = requests.get('http://127.0.0.1:5000/v1/events/%s/tickets' % str(event_id))
    print r.json()

def test_add_tickets(seller_id):
    '''available seller id 1 ~ 7
    '''
    data = {
        "event_id": 107,
        "ticket_section": 222,
        "ticket_row": "111", 
        "ticket_quantity": 20,
        "ticket_price": 50
    }
    r = requests.post('http://127.0.0.1:5000/v1/sellers/%s/tickets' % str(seller_id), data = json.dumps(data))
    print r.json()

def test_buy_tickets(ticket_id):
    '''available ticket id 1 ~ 1533 if there is no more tickets added.
    '''
    data = {
        "referal_id": 2,
        "customer_id": 3
    }
    r = requests.put('http://127.0.0.1:5000/v1/ticket/%s' % str(ticket_id), data = data)
    print r.json()

def test_get_best_ticket(event_id):
    '''available case 162, 164, 107
    '''
    r = requests.get('http://127.0.0.1:5000/v1/events/%s/tickets?search=best' % str(event_id))
    print r.json()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '1':
            test_get_available_tickets(162)
        if sys.argv[1] == '2':
            test_add_tickets(1)
        if sys.argv[1] == '3':
            test_buy_tickets(1)
        if sys.argv[1] == '4':
            test_get_best_ticket(162)

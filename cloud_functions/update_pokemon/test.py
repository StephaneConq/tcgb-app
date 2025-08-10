from pokemontcgsdk import RestClient
from pokemontcgsdk import Card, Set


RestClient.configure('9addaede-720a-4e1f-a08b-411776f7221a')

cards = Card.where(page=1, pageSize=250)

sets = Set.all()
for set in sets:
    print(set.id)
    cards = Card.where(q=f'set.name:{set.name.lower()}', page=5, pageSize=250)
    pass

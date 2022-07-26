doodad = {
    "title": str, # the bold words at the top of the card
    "description": str, # exactly what is on the card telling you what to do
    "cash": int, # currently going to spend
    "cashflow": int, # what you spend monthly for it
    "category": str # One of the categories in expenses, typically 'other'
}

market = {
    "title": str, # The bold words at the top of the card
    "description": str, # exactly what is on the card telling you what to do
    "type": str, # eg. realestate, stock, land, business, dividend, insurance, child marries, (CONTINUED.)
    # pollution, natural disaster, CHARITY, mentor
    "name": str, # eg. MYT4U, OK4U, 4-PLEX, STARTERHOUSE, APARTMENTCOMPLEX, ALL. What card affects
    "highest": bool, # when realestate, affects the highest value of property
    "price": int or str, # eg. the stock price, what you are selling realestate for per unit, land. (CONTINUED.)
    # when child marries pay amount.
    "bankrupt": bool, # eg. stock fails, lose all shares
    "size": int, # in land, selling 5 acres or 10 acres
    "value": int, # in spare time co, you get a $7000 value, foreign trade and recession will have this too
    "property": object, # exchange deals, your starter house changes to 4-PLEX, record these new numbers.
    "forcedSale": bool, # You have no choice but to sell.
    "target": str, # eg. Player, player your right, everyone, right all, starts with you and moves to the right.
}

capitalGain = {
    "title": str, # the bold words at the top of the card
    "description": str, # the words on the card
    "type": str, # stock, realestate, land, business (D2Y)
    "option": str, # in the stock category, is it a CALL, PUT, REGULAR, or SHORT
    "name": str, # MYT4U, OK4U, DUPLEX, STARTERHOUSE, LAND, CARD 1
    "card": object, # in the stock case, there is the current price, option, strikePrice, and name,
    # in the realestate case there is name, cost, (CONTINUED.)
    # mortgage, downpay and cashflow, in the land case, the same as realestate, in the business case, cost and cashflow.

}

cashFlow = {
    "title": str, # the bold words at the top of the card
    "description": str, # the words on the card
    "type": str, # realestate, business (D2Y, Royalty), dividend, OPTION
    "name": str, # DUPLEX, STARTERHOUSE, CARD 1, Partner with a Pro, ROYALTY
    "card": object,
    # in the realestate case there is name, cost, (CONTINUED.)
    # mortgage, downpay and cashflow, in the business case, name, cost and cashflow, (CONTINUED.)
    # in the dividend case name, cost, downpay, cashflow, in the option case: cost.
}

beginning = {
    "title": str, # the bold words at the top of the card
    "description": str, # what the card says
    "cash": int, # the amount of extra starting money you have
    "stock": object, # the amount of stock you start with
    "realestate": object # if there is a real estate object what you have at start
}

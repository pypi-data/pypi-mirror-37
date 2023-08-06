# -*- coding: utf-8 -*-
from flask import session
from shop.signals import sale_created, sale_transferred
from shop.globals import current_cart


def copy_flipgive_id(sender, sale=None):
    "Copy flipgive_campaign to created party"
    cart = current_cart
    flipgive_campaign_id = session.get('flipgive_campaign_id') or \
        (cart.flipgive_campaign and cart.flipgive_campaign.id)

    sale = sale or cart.sale

    # Save FlipGive Campaign to sale and party if available in Cart
    if flipgive_campaign_id and sale:
        sale.flipgive_campaign = flipgive_campaign_id
        sale.flipgive_token = session.get('flipgive_token')
        sale.save()

        party = sale.party
        party.flipgive_campaign = flipgive_campaign_id
        party.save()


def register_signals(app):
    "Registers signals with app"
    sale_created.connect(copy_flipgive_id, app)
    sale_transferred.connect(copy_flipgive_id, app)

# -*- coding: utf-8 -*-
"""Product views."""
from flask import Blueprint, flash, request, redirect, url_for, session
from flask_babel import gettext as _

from fulfil_client import ClientError
from fulfil_shop_flipgive.models import FlipGiveCampaign
from shop.cart.models import Cart

blueprint = Blueprint(
    'flipgive', __name__,
    url_prefix='/flipgive', static_folder='../static'
)


@blueprint.route('/campaign-landing')
def flipgive_campaign():
    flipgive_token = request.args.get('token')
    redirect_url = request.args.get('redirect')

    if flipgive_token:
        try:
            flipgive_campaign_id = FlipGiveCampaign.rpc.get_from(flipgive_token)
        except ClientError:
            flash(_('Error in identifying campaign.'), 'error')
            # Flipgive token is wrong
            return redirect(url_for('public.home'))

        flipgive_campaign = FlipGiveCampaign.get_by_id(flipgive_campaign_id)

        session['flipgive_token'] = flipgive_token
        session['flipgive_campaign_id'] = flipgive_campaign_id

        flash(_('Congratulations! Your purchase will sponsor %s' %
                flipgive_campaign.name))

        # save the flipgive_campaign_id in current cart
        cart = Cart.get_active()
        cart.flipgive_campaign = flipgive_campaign_id
        cart.save()

        if cart.sale:
            sale = cart.sale
            sale.flipgive_campaign = cart.flipgive_campaign.id
            sale.flipgive_token = flipgive_token
            sale.save()
        if cart.sale and cart.sale.party:
            party = cart.sale.party
            party.flipgive_campaign = cart.flipgive_campaign.id
            party.save()

    return redirect(redirect_url or url_for('public.home'))

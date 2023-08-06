# -*- coding: utf-8 -*-
"""Flipgive models"""
from fulfil_client.model import (ModelType, StringType)

import shop.cart.models
import shop.user.models
from shop.fulfilio import Model


class Sale(shop.cart.models.Sale):
    flipgive_campaign = ModelType("flipgive.campaign", cache=True)
    flipgive_token = StringType()


shop.cart.models.Sale = Sale


class Cart(shop.cart.models.Cart):
    flipgive_campaign = ModelType("flipgive.campaign", cache=True)


shop.cart.models.Cart = Cart


class Party(shop.user.models.Party):
    # XXX: FlipGive Campaign is saved on Party because it can be used for
    # shopping multiple times (especially phone order). In case, the
    # user comes from different FlipGive Campaign, this should be updated.
    flipgive_campaign = ModelType("flipgive.campaign", cache=True)


shop.user.models.Party = Party


class FlipGiveCampaign(Model):
    __model_name__ = 'flipgive.campaign'

    name = StringType()
    campaign_id = StringType()

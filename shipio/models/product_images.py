from odoo import models, fields, api

import logging

_log = logging.getLogger(__name__)


class ProductImages(models.Model):
    _name = "product.images"

    product_id = fields.Many2one('product.template')
    image = fields.Image("image", max_width=128, max_height=128)

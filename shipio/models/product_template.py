from odoo import models, fields, api

import logging

_log = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_id = fields.Many2one('res.partner', required=True)
    image_ids = fields.One2many(comodel_name='product.images', inverse_name='product_id')
    height = fields.Float()
    width = fields.Float()
    length = fields.Float()
    volume = fields.Float(string='Volume', compute='_compute_volume', store=True, readonly=True)
    shipping_method = fields.Selection([
        ('air', 'Air'),
        ('sea', 'Sea'),
        ('land', 'Land')
    ])
    storage_location = fields.Many2one('stock.location')
    destination_location = fields.Many2one('stock.location')
    delivery_address = fields.Many2one('res.partner')
    delivery_country = fields.Many2one('res.country', related='delivery_address.country_id', store=True)

    @api.depends('height', 'width', 'length')
    def _compute_volume(self):
        for record in self:
            record.volume = (record.height*record.width*record.length) / 10**6

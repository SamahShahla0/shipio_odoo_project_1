from odoo import models, fields, api

import random
import string

import logging

_log = logging.getLogger(__name__)


class Shipments(models.Model):
    _name = "shipments"

    name = fields.Char()
    products_count = fields.Integer(compute='_compute_count_products', store=True)
    delivery_country = fields.Many2one('res.country', store=True)
    lines = fields.One2many('shipment.line', inverse_name='shipment_id')

    @api.depends('lines')
    def _compute_count_products(self):
        for record in self:
            record.products_count = len(record.lines)

    def action_open_label_type(self):
        action = self.env['ir.actions.act_window']._for_xml_id('product.action_open_label_layout')
        action['context'] = {'default_product_ids': self.lines.product_id.ids}
        return action


class ShipmentLine(models.Model):
    _name = "shipment.line"

    shipment_id = fields.Many2one('shipments', ondelete='cascade')
    product_id = fields.Many2one('product.template', required=True)
    customer_id = fields.Many2one('res.partner', related='product_id.customer_id')
    storage_location = fields.Many2one('stock.location', related='product_id.storage_location')
    destination_location = fields.Many2one('stock.location', related='product_id.destination_location')
    delivery_country = fields.Many2one('res.country', related='product_id.delivery_address.country_id')
    delivery_address = fields.Many2one('res.partner', related='product_id.delivery_address')
    ship_barcode = fields.Char(string='Barcode', readonly=True, stored=True)

    @api.model
    def create(self, vals):
        if 'ship_barcode' not in vals or not vals['ship_barcode']:
            vals['ship_barcode'] = self._generate_barcode()
        record = super(ShipmentLine, self).create(vals)
        record.product_id['barcode'] = record.ship_barcode
        return record

    def _generate_barcode(self):
        # Generate a random barcode (e.g., 13 characters long)
        return ''.join(random.choices(string.digits, k=13))

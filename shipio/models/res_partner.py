from odoo import models, fields, api

import logging

_log = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    product_ids = fields.One2many(comodel_name='product.template', inverse_name='customer_id')
    country_code = fields.Char(related='country_id.code', store=True)
    base_name = fields.Char(string='Base Name')
    location = fields.Char(string='Location', compute='_compute_location', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['base_name'] = vals['name']
            if vals.get('country_id'):
                country_id = vals.get('country_id')
                country = self.env['res.country'].search([('id', '=', country_id)])
                vals['name'] = '%s - %s' % (country.code, vals['name'])
        records = super().create(vals_list)
        return records

    def write(self, vals_list):
        if vals_list.get('country_id'):
            for record in self:
                country_id = vals_list.get('country_id')
                country = self.env['res.country'].search([('id', '=', country_id)])
                vals_list['name'] = '%s - %s' % (country.code, record.base_name)
        res = super().write(vals_list)
        return res

    @api.depends('street', 'city', 'state_id', 'country_id')
    def _compute_location(self):
        for record in self:
            parts = [record.street, record.city, record.state_id.name if record.state_id else '',
                     record.country_id.name if record.country_id else '']
            record.location = ', '.join(part for part in parts if part)

    def open_location_in_google_maps(self):
        for record in self:
            if record.location:
                return {
                    'type': 'ir.actions.act_url',
                    'url': f"https://www.google.com/maps/search/?api=1&query={record.location}",
                    'target': 'new',
                }


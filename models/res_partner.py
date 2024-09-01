from odoo import models, fields, api
#from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging

_logger = logging.getLogger(__name__)

class ResCountryMunicipality(models.Model):
    _name = 'res.country.municipality'
    _description = 'Municipality'

    name = fields.Char(string='Municipio', required=True)
    state_id = fields.Many2one('res.country.state', string='Provincia', required=True)
    postal_code = fields.Char(string='Código Postal')

    @api.model
    def action_save(self):
        self.ensure_one()  #
        return True 

class ResPartner(models.Model):
    _inherit = 'res.partner'

    cuban_country_id = fields.Many2one(
        'res.country', 
        string='País', 
        default=lambda self: self.env['res.country'].search([('name', '=', 'Cuba')], limit=1).id
    )
    province_id = fields.Many2one(
        'res.country.state', 
        string='Provincia',
        domain="[('country_id', '=', cuban_country_id)]",  # Filtrar las provincias que pertenecen a Cuba
    )
    municipality_id = fields.Many2one(
        'res.country.municipality', 
        string='Municipio',
        domain="[('state_id', '=', province_id)]",  # Filtrar los municipios que pertenecen a la provincia seleccionada
    )
    
    postal_code = fields.Char(string='Código Postal', compute='_compute_postal_code')

    @api.depends('municipality_id')
    def _compute_postal_code(self):
        for partner in self:
            partner.postal_code = partner.municipality_id.postal_code

    @api.model
    def default_get(self, fields):
        res = super(ResPartner, self).default_get(fields)
        res['cuban_country_id'] = self.env['res.country'].search([('name', '=', 'Cuba')], limit=1).id
        return res

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    delivery_municipality_ids = fields.Many2many(
        'res.country.municipality',
        string='Municipios de Entrega'
    )

    delivery_municipality_display = fields.Char(
        string='Municipios de Entrega (Provincia/Municipio)',
        compute='_compute_delivery_municipality_display'
    )

    @api.depends('delivery_municipality_ids')
    def _compute_delivery_municipality_display(self):
        for product in self:
            names = []
            for municipality in product.delivery_municipality_ids:
                if municipality.state_id:
                    names.append(f"{municipality.state_id.name} / {municipality.name}")
                else:
                    names.append(municipality.name)
            product.delivery_municipality_display = ', '.join(names)


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    municipality_ids = fields.Many2many('res.country.municipality', string='Municipio')

    @api.onchange('municipality_ids')
    def _onchange_municipality_ids(self):
        if self.municipality_ids:
            provinces = self.municipality_ids.mapped('state_id')
            self.state_ids = provinces
            #self.country_id = self.env.ref('base.cu').id
            # Mantén Cuba como el único país en el campo country_ids
            self.country_ids = [(6, 0, [self.env.ref('base.cu').id])]

    # Predefinir los campos y hacerlos de solo lectura
    state_ids = fields.Many2many('res.country.state', string='Provincias', readonly=True)
    country_ids = fields.Many2many(
        ....
    )

    def _match_address(self, partner):
        _logger.info("Método '_match_address' extendido...")        
        # Obtenemos el municipality_id desde el partner o desde el contexto/sesión
        ......
        
        return True
        


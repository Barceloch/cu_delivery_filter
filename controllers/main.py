# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import logging

_logger = logging.getLogger(__name__)

class DeliveryFilter(http.Controller):
    #@http.route('/api/user_status', type='http', auth='public', website=True)
    @http.route('/api/user_status', type='http', auth='public', methods=['GET'], website=True)
    def user_status(self):
        user = request.env.user
        is_logged_in = user.id != request.env.ref('base.public_user').id
        resp = {'logged_in': is_logged_in}
        
        _logger.info("Is Logged in: %s", resp)
        
        return request.make_response(
            json.dumps(resp), 
            headers=[('Content-Type', 'application/json')]
        )
    
    @http.route('/api/partner_delivery_info', type='http', auth='public', methods=['GET'], website=True)
    def partner_delivery_info(self):
        user = request.env.user
        partner = user.partner_id

        # Obtener el municipio según el nombre de la ciudad del partner
        #municipality = request.env['res.country.municipality'].search([('name', '=', partner.city)], limit=1)

        # Preparar la respuesta
        response_data = {
            'partner_city': partner.city,  # Ciudad del partner
            'partner_state': partner.state_id.code if partner.state_id else None  # Estado/Provincia del partner
        }

        # Crear la respuesta JSON
        return request.make_response(
            json.dumps(response_data), 
            headers=[('Content-Type', 'application/json')]
        )



    @http.route('/set_delivery_address', type='http', auth='public', methods=['POST'], website=True, csrf=False)     
    def set_delivery_address(self, province_id, municipality_id):
        _logger.info("EXECUTING /set_delivery_address ...")

        province = request.env['res.country.state'].sudo().browse(int(province_id))
        municipality = request.env['res.country.municipality'].sudo().browse(int(municipality_id))
        
        if not province.exists() or not municipality.exists() or municipality.state_id.id != province.id:
            return {'error': 'Provincia o municipio no válido'}

        # Guardar en la sesión
        request.session['province_id'] = province.id
        request.session['municipality_id'] = municipality.id

        # Verificar si el usuario está autenticado
        if request.env.user and not request.env.user._is_public():
            _logger.info("UPDATE USER ADDRESS...")
            # Actualizar la información de contacto del usuario
            partner = request.env['res.partner'].sudo().browse(request.env.user.partner_id.id)
            partner.write({
                'country_id': 51,  # ID del país (Cuba)
                'state_id': province.id,
                'city': municipality.name,
                #'street': '_'
            })

            # Vaciar el carrito si se cambia la dirección
            request.website.sale_get_order().sudo().unlink()

        return request.redirect('/shop')

    @http.route('/shop/cart/items_count', type='http', auth='public', website=True)
    def get_cart_items_count(self):
        _logger.info("Getting cart items count...")
        order = request.website.sale_get_order()
        if order:
            _logger.info("Order found, counting items.")
            return request.make_response(
                f'{{"items_count": {len(order.order_line)}}}',
                headers=[('Content-Type', 'application/json')]
            )
        _logger.info("No order found, returning 0 items.")
        return request.make_response('{"items_count": 0}', headers=[('Content-Type', 'application/json')])

   
    @http.route('/get_municipalities', type='json', auth='public', methods=['POST'], website=True)
    def get_municipalities(self, province_id):
        #_logger.info("Province ID received: %s", province_id)
        municipalities = request.env['res.country.municipality'].search([('state_id', '=', int(province_id))])
        municipalities_list = [{'id': m.id, 'name': m.name} for m in municipalities]
        #_logger.info("Municipalities found: %s", municipalities_list)
        return municipalities_list

class CustomWebsiteSale(WebsiteSale):

    def _get_mandatory_fields_billing(self, country_id=False):
        ...
        return req

    def _check_shipping_partner_mandatory_fields(self, partner_id):
        ...
        return all(partner_id.read(shipping_fields_required)[0].values())

    def _get_mandatory_fields_shipping(self, country_id=False):
        ...
        return req



   


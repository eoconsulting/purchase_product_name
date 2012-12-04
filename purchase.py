# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2012 Tiny SPRL (<http://tiny.be>)
#                            Sistemas ADHOC
#                            Mariano Ruiz (Enterprise Objects Consulting)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import osv
from osv import fields
from tools.translate import _

class purchase_order_line(osv.osv):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'
    
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, notes=False, context=None):
        
        if context is None:
            context = {}
        
        res = super(purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
                    partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned,
                    name=name, price_unit=price_unit, notes=notes, context=context)
        
        if not product_id:
            return res
        
        product_product = self.pool.get('product.product')
        res_partner = self.pool.get('res.partner')
        
        lang = res_partner.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}
        
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        if not product:
            return res
        if isinstance(product, list):
            product = product[0]
        
        supplierinfo = False
        for supplierinfo_it in product.product_tmpl_id.seller_ids:
            if supplierinfo_it.name.id == partner_id:
                supplierinfo = supplierinfo_it
                break
        
        if supplierinfo and supplierinfo.product_name:
            new_name = supplierinfo.product_name
            if supplierinfo.product_code:
                new_name = '[' + supplierinfo.product_code + '] ' + new_name
            if 'value' in res:
                if product.default_code:
                    new_name += ' (Ref ' + product.default_code + ')'
                else:
                    new_name += ' (' + product.name + ')'
                res['value']['name'] = new_name
        return res
        
purchase_order_line()

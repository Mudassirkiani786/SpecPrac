from odoo import models

class MrpBom(models.Model):
    _inherit = "mrp.bom"

    def action_open_merged_materials(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Merged Materials',
            'res_model': 'merged.materials.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_bom_id': self.id},
        }

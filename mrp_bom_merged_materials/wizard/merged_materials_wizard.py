from odoo import models, fields
from collections import defaultdict

class MergedMaterialsWizard(models.TransientModel):
    _name = "merged.materials.wizard"

    bom_id = fields.Many2one("mrp.bom")
    line_ids = fields.One2many("merged.materials.line", "wizard_id")

    def action_compute(self):
        merged = defaultdict(float)

        def explode(bom, qty=1):
            for line in bom.bom_line_ids:
                total_qty = line.product_qty * qty

                if line.child_bom_id:
                    explode(line.child_bom_id, total_qty)
                else:
                    merged[line.product_id] += total_qty

        explode(self.bom_id)

        self.line_ids = [(0, 0, {
            "product_id": p.id,
            "quantity": q
        }) for p, q in merged.items()]

        return True


class MergedMaterialsLine(models.TransientModel):
    _name = "merged.materials.line"

    wizard_id = fields.Many2one("merged.materials.wizard")
    product_id = fields.Many2one("product.product")
    quantity = fields.Float()

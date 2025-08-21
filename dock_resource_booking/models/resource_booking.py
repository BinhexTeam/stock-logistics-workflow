from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    picking_ids = fields.One2many(
        "stock.picking",
        "booking_id",
        string="Associated Pickings",
        domain="[('state', 'not in', ['done', 'cancel']), \
              ('booking_id', '=', False), ('scheduled_date', '>=', start)]",
    )

    @api.constrains("start")
    def _check_start(self):
        for record in self.filtered("picking_ids"):
            if record.start:
                min_scheduled_date = min(record.picking_ids.mapped("scheduled_date"))
                if min_scheduled_date < record.start:
                    raise ValidationError(
                        _("Pickings should be scheduled after booking start!")
                    )

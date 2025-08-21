from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    booking_id = fields.Many2one(
        "resource.booking", string="Dock Reservation", ondelete="set null"
    )
    transporter_id = fields.Many2one("res.partner", string="Transport Company")
    transport_type = fields.Char(help="e.g., trailer, van, truck")

    @api.constrains("booking_id", "scheduled_date")
    def _check_booking_id(self):
        for record in self:
            if record.booking_id and record.booking_id.start and record.scheduled_date:
                if record.scheduled_date < record.booking_id.start:
                    raise ValidationError(
                        _("All pickings should be scheduled after booking start!")
                    )

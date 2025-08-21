from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResourceBooking(models.Model):
    _inherit = "resource.booking"

    picking_ids = fields.One2many(
        "stock.picking", "booking_id", string="Associated Pickings"
    )

    @api.onchange("date_start")
    def _onchange_date_start(self):
        for booking in self:
            for picking in booking.picking_ids:
                picking.scheduled_date = booking.date_start

    @api.constrains("resource_id", "date_start", "date_end")
    def _check_booking_collision(self):
        for booking in self:
            domain = [
                ("id", "!=", booking.id),
                ("resource_id", "=", booking.resource_id.id),
                ("date_start", "<", booking.date_end),
                ("date_end", ">", booking.date_start),
            ]
            overlapping = self.search(domain)
            if overlapping:
                raise ValidationError(_("Dock is already reserved for this time slot."))

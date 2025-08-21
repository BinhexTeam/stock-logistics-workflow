from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    booking_id = fields.Many2one(
        "resource.booking", string="Dock Reservation", ondelete="set null"
    )
    transporter_id = fields.Many2one("res.partner", string="Transport Company")
    transport_type = fields.Char(help="e.g., trailer, van, truck")

    @api.onchange("booking_id")
    def _onchange_booking_id(self):
        if self.booking_id:
            self.scheduled_date = self.booking_id.start

    @api.onchange("scheduled_date")
    def _onchange_scheduled_date(self):
        if self.booking_id and self.scheduled_date:
            self.booking_id.start = self.scheduled_date

    @api.model
    def create(self, vals):
        picking = super().create(vals)
        picking._auto_create_booking_on_confirm()
        return picking

    def write(self, vals):
        res = super().write(vals)
        self._auto_create_booking_on_confirm()
        return res

    def _auto_create_booking_on_confirm(self):
        for picking in self:
            if picking.state == "confirmed" and not picking.booking_id:
                # Only create if not already linked
                booking = self.env["resource.booking"].create(
                    {
                        "name": _("Dock Reservation for %s") % picking.name,
                        "start": picking.scheduled_date,
                        "date_end": picking.scheduled_date,
                        "resource_id": (
                            picking.dropoff_site_id.resource_id.id
                            if picking.dropoff_site_id
                            else False
                        ),
                        "picking_ids": [(4, picking.id)],
                    }
                )
                picking.booking_id = booking.id

    @api.constrains("booking_id")
    def _check_booking_collision(self):
        for picking in self:
            if picking.booking_id:
                overlapping = self.search(
                    [
                        ("id", "!=", picking.id),
                        ("booking_id", "=", picking.booking_id.id),
                        ("scheduled_date", "=", picking.scheduled_date),
                    ]
                )
                if overlapping:
                    raise ValidationError(
                        _(
                            "Another picking is already reserved for this dock and time slot."
                        )
                    )

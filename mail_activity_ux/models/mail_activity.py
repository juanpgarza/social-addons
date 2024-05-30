from odoo import fields, models


class MailActivity(models.Model):

    _inherit = "mail.activity"

    priority = fields.Selection([("1", "Alta"),("2", "Media"), ("3", "Baja")], string="Prioridad")
    
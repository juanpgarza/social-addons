from odoo import fields, models, api
from datetime import datetime

class MailActivity(models.Model):
    _name = 'mail.activity'
    _inherit = ['mail.activity', 'mail.thread']

    priority = fields.Selection([("1", "Alta"),("2", "Media"), ("3", "Baja")], string="Prioridad", tracking=True,)

    activity_group = fields.Integer("Grupo de actividades")

    approve_state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirm', 'Para aprobar'),
        ('refuse', 'Rechazada'),
        # ('validate1', 'Segunda aprobación'),
        ('validate', 'Aprobada')
        ], string='Estado de aprobación', 
        default='draft',
        tracking=True,
        )
        # compute='_compute_approve_state', store=True, tracking=True, copy=False, readonly=False,
        # help="The status is set to 'To Submit', when a time off request is created." +
        # "\nThe status is 'To Approve', when time off request is confirmed by user." +
        # "\nThe status is 'Refused', when time off request is refused by manager." +
        # "\nThe status is 'Approved', when time off request is approved by manager.")
    
    # approval_required = fields.Boolean(related='activity_type_id.approval_required')
    approval_required = fields.Boolean(compute="_compute_approval_required", string="Requiere aprobación", store=True)

    dias_atraso = fields.Integer(compute="_dias_atraso",string="Días de atraso")

    def _dias_atraso(self):
        for rec in self:
            fecha_vencimiento = rec.date_deadline
            fecha_hecho = rec.date_done
            if rec.done:            
                delta = fecha_hecho - fecha_vencimiento
                if delta.days < 0:
                    rec.dias_atraso = False
                else:
                    rec.dias_atraso = delta.days
            else:
                delta = datetime.now().date() - fecha_vencimiento
                if delta.days < 0:
                    rec.dias_atraso = False
                else:
                    # esta vencida
                    rec.dias_atraso = delta.days                    
    
    @api.model
    def create(self,values):
        res = super(MailActivity,self).create(values)
        res.approve_state = 'draft'
        return res

    # def action_done(self):
    #     res = super().action_done()
    #     for rec in self:
    #         if rec.approval_required:
    #             rec.approve_state = 'confirm'
    #             rec.active = True
    
    def _action_done(self, feedback=False, attachment_ids=None):
        # import pdb; pdb.set_trace()       
        res = super()._action_done(feedback,attachment_ids)
        for rec in self:
            if rec.approval_required:
                rec.approve_state = 'confirm'
                rec.active = True
            else:
                rec.approve_state = 'validate'
        return res

    def action_approve(self):        
        for rec in self:
            rec.approve_state = 'validate'
            rec.active = False

    def action_refuse(self):        
        for rec in self:
            rec.approve_state = 'refuse'
            rec.date_done = False
            rec.done = False
            # No funciona!
            # rec.state = 'today'

    @api.depends('activity_type_id')
    def _compute_approval_required(self):
        for activity in self:
            # leave.state = 'confirm' if leave.validation_type != 'no_validation' else 'draft'
            activity.approval_required = activity.activity_type_id.approval_required
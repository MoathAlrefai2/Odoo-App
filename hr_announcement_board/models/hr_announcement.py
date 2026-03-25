# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import date

HR_ANNOUNCEMENT = 'hr.announcement'


class HrAnnouncement(models.Model):
    _name = HR_ANNOUNCEMENT
    _description = 'HR Announcement'
    _rec_name = 'title'
    _order = 'is_pinned desc, publish_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # ─── Fields ──────────────────────────────────────────────────────────────

    title = fields.Char(
        string='Title',
        required=True,
        tracking=True,
    )
    body = fields.Html(
        string='Content',
        required=True,
        sanitize=True,
    )
    priority = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        string='Priority',
        default='0',
        required=True,
        tracking=True,
    )
    publish_date = fields.Date(
        string='Publish Date',
        default=fields.Date.today,
        required=True,
        tracking=True,
    )
    expiry_date = fields.Date(
        string='Expiry Date',
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('expired', 'Expired'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        copy=False,
    )
    author_id = fields.Many2one(
        comodel_name='res.users',
        string='Author',
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    is_pinned = fields.Boolean(
        string='Pinned',
        default=False,
        help='Pinned announcements always appear at the top of the board.',
        tracking=True,
    )

    # ─── Computed / helpers ───────────────────────────────────────────────────

    @api.constrains('publish_date', 'expiry_date')
    def _check_dates(self):
        for rec in self:
            if rec.expiry_date and rec.expiry_date < rec.publish_date:
                raise UserError(
                    _('Expiry Date must be equal to or after the Publish Date.')
                )

    # ─── Actions / workflow ──────────────────────────────────────────────────

    def action_publish(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_('Only draft announcements can be published.'))
            rec.state = 'published'

    def action_set_draft(self):
        for rec in self:
            if rec.state == 'expired':
                raise UserError(_('Expired announcements cannot be reset to draft.'))
            rec.state = 'draft'

    def action_expire(self):
        for rec in self:
            rec.state = 'expired'

    # ─── Scheduled action ────────────────────────────────────────────────────

    @api.model
    def _cron_auto_expire(self):
        """Called by a scheduled action to auto-expire past announcements."""
        today = fields.Date.today()
        expired = self.search([
            ('state', '=', 'published'),
            ('expiry_date', '<', today),
            ('expiry_date', '!=', False),
        ])
        if expired:
            expired.write({'state': 'expired'})

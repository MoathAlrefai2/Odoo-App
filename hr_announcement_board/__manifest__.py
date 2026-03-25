# -*- coding: utf-8 -*-
{
    'name': "HR Announcement Board",
    'summary': "Internal notice board where HR posts announcements visible to all employees",
    'description': "HR posts announcements with title, body, priority, and expiry date. Employees see active announcements on their dashboard. Announcements auto-hide after expiry.",
    'author': "Leading Point",
    'maintainer': "Leading Point",
    'website': "https://www.leading-point.com/",
    'category': 'Human Resources',
    'version': '18.0.0.0',
    'application': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'LGPL-3',
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml',
        'data/ir_cron.xml',
        'views/hr_announcement_form_list.xml',
        'views/hr_announcement_kanban.xml',
        'views/menu_items.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_announcement_board/static/src/scss/hr_announcement.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
}

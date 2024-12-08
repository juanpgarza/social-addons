# Copyright 2024 juanpgarza - Juan Pablo Garza <juanp@juanpgarza.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "mail_activity_ux",
    "summary": "",
    "version": "17.0.1.0.0",
    "category": "Social",
    "website": "https://github.com/juanpgarza/social-addons",
    "author": "juanpgarza",
    "license": "AGPL-3",
    "depends": [
                "base",
                "mail",
                "mail_activity_done", # OCA
                "mail_activity_board" # OCA
            ],
    "data": [
        'security/activity_security.xml',
        'views/mail_activity_views.xml',
        'views/mail_activity_type_views.xml',
        ],
    "installable": True,
}
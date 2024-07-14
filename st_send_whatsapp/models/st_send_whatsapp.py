# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api
import requests

class STSendWhatsApp(models.AbstractModel):
    _name = 'st.send.whatsapp'
    _description = 'Envia mensajes de whatsapp a contactos y grupos'

    @api.model
    def send_whapi(self,url="https://gate.whapi.cloud/messages/text",to="",message="",token="i2dyifThuwjRO4LYY9nnBefqichNzktU"):

        payload = {
            "typing_time": 0,
            "to": to,
            "body": message
        }
    
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": "Bearer {}".format(token)
        }

        response = requests.post(url, json=payload, headers=headers)

        return response

        # esto: 
        #       self.env['st.send.whatsapp'].send_whapi(to='120363246572441398@g.us',message='desde odoo')
        #       self.env['st.send.whatsapp'].send_whapi(to='120363246572441398@g.us',message='desde odoo 2',token='i2dyifThuwjRO4LYY9nnBefqichNzktU')
        # funciona OK desde el shell

        # print(response.text)

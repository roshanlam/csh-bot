import asyncio
import discord, secrets
from discord.ext import commands

class TextInput:
    """for storing our text input data"""
    def __init__(self, payload):
        self.type = payload['type']
        self.custom_id = payload['custom_id']
        self.style = payload['style']
        self.label = payload['label']
        self.min_length = payload.get('min_length')
        self.max_length = payload.get('max_length')
        self.required = payload.get('required')
        self.value = payload.get('value')
        self.placeholder = payload.get('placeholder')

class Modal:
    def __init__(self, bot: commands.Bot, title):
        self.bot = bot
        self.title = title
        self.custom_id = secrets.token_urlsafe(16)
        self.payload = {
          'title': title,
          'custom_id': self.custom_id,
          'components': []
        }
        self.adapter = discord.webhook.async_.async_context.get()
        self.fields = []

    def add_field(self, style, label, min_length=None, max_length=None, required=False, value=None, placeholder=None):
        """method to add new text input field
        styles:
            1 : single-line input
            2 : multi-line input
        """
        component = {
            'type': 4,
            'custom_id': secrets.token_urlsafe(16),
            'style': style,
            'label': label,
            'required': str(required),
        }
        if min_length:
            component['min_length'] = min_length
        if max_length:
            component['max_length'] = max_length
        if value:
            component['value'] = value
        if placeholder:
            component['placeholder'] = placeholder

        self.payload['components'].append({
            'type': 1,
            'components': [component]
        })

        self.fields.append(TextInput(component))

    async def send_modal(self, interaction: discord.Interaction):
        interaction.response._responded = True

        await self.adapter.create_interaction_response(
            interaction_id = interaction.id,
            token = interaction.token,
            session = interaction._session,
            data = self.payload,
            type = 9
        )

    async def wait(self, timeout=180):
        def interaction_check(interaction: discord.Interaction):
            return interaction.data.get('custom_id') == self.custom_id

        # this is probably a bad implementation but its working
        try:
            # wait for interaction with that match this modal instance custom_id
            interaction = await self.bot.wait_for('interaction', check=interaction_check, timeout=timeout)
        except asyncio.TimeoutError:
            # return None if user didn't respond to the modal
            return None, []

        components = interaction.data['components']

        # match each result field with corresponding TextInput field
        # because interaction data doesn't hold all of text input data
        result = []
        for component in components:
            for field in self.fields:
                if component['components'][0]['custom_id'] == field.custom_id:
                    field.value = component['components'][0]['value']
                    result.append(field)

        # returns modal interactions and list of TextInput filled.
        return interaction, result
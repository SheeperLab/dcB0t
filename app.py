import discord
from discord.ext import commands
import requests
import os
def notify_send(msg):
    url = 'https://notify-api.line.me/api/notify'
    token = os.environ['LINE_NOTIFY_TOKEN']
    headers = {
        'Authorization': 'Bearer ' + token
    }
    data = {
        'message': msg
    }
    response = requests.post(url, headers=headers, data=data)
    if response.status_code != 200:
        print('LINE 通知發送失敗')

intents = discord.Intents.default()
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        try:
            notify_send(f'{member.name} 進入了語音頻道 {after.channel.name}')
        except Exception as e:
            print(f'LINE 通知發送失敗: {e}')
    elif before.channel is not None and after.channel is not None and before.channel != after.channel:
        try:
            notify_send(f'{member.name} 從 {before.channel.name} 移動到了 {after.channel.name}')
        except Exception as e:
            print(f'LINE 通知發送失敗: {e}')

bot.run(os.environ['BOT_TOKEN'])

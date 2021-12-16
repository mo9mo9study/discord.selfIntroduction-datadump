import discord
from discord.ext import commands
import json
from collections import OrderedDict


class WriteJson(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.OTHERS_SERVER_ID = ""  # 不要なデータを移動する先のdiscordギルドID
        self.DB_SERVER_ID = ""  # 自己紹介データを保存していたDBギルドID

    @commands.Cog.listener()
    async def on_ready(self):
        self.OTHERS_SERVER = self.bot.get_guild(self.OTHERS_SERVER_ID)
        self.DB_SERVER = self.bot.get_guild(self.DB_SERVER_ID)
        print(self.DB_SERVER)

    @commands.command()
    async def jsons(self, ctx):
        number = 0
        with open("src/introduction.json", "r", encoding="utf-8") as f:
            # update_json = json.load(f, object_pairs_hook=OrderedDict)
            update_json = json.load(f)
        update_json["data"] = []
        for channel in self.DB_SERVER.text_channels:
            messages = await channel.history(limit=None).flatten()
            messages.reverse()
            messages = list(map(lambda m: m.content, messages))
            if len(messages) == 7:  # 自己紹介が登録されているchannel(json)
                print(messages[0])
                update_json["data"].append({})
                update_json["data"][number]["name"]        = messages[0]
                update_json["data"][number]["id"]          = int(channel.name)
                update_json["data"][number]["gender"]      = messages[1]
                update_json["data"][number]["twitterID"]   = messages[2]
                update_json["data"][number]["specialty"]   = messages[3]
                update_json["data"][number]["learned"]     = messages[4]
                update_json["data"][number]["studyingnow"] = messages[5]
                update_json["data"][number]["msgID"]       = messages[6]
                number += 1
            # else:  # 自己紹介が不完全なchannel(別サーバー)
            #     tp_channel = await self.OTHERS_SERVER.create_text_channel(name=messages[0], topic=channel.name)
            #     try:
            #         await tp_channel.send(messages[0])
            #         await tp_channel.send(messages[1])
            #         await tp_channel.send(messages[2])
            #         await tp_channel.send(messages[3])
            #         await tp_channel.send(messages[4])
            #         await tp_channel.send(messages[5])
            #     except IndexError:
            #         pass
        else:
            with open("src/after-introduction.json", "w", encoding="utf-8") as f:
                json.dump(update_json, f, indent=4, ensure_ascii=False)
                print("[INFO] Script end. Saved json data ")

    # バグで作成されたチャンネルを一括削除
    @commands.command()
    async def delch(self, ctx):
        for channel in self.DB_SERVER.text_channels:
            messages = await channel.history(limit=None).flatten()
            if len(messages) == 0:
                print(f"{channel.name}.delete")
                await channel.delete()


def setup(bot):
    bot.add_cog(WriteJson(bot))

import os
import logging
from dotenv import load_dotenv
from groq import Groq
import discord
from discord.ext import commands

# .envファイルを読み込む
load_dotenv()

# 環境変数からトークンを取得
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ログ設定
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='chat_log.txt', filemode='a', encoding="utf-8")

# Groqクライアントを作成
client_groq = Groq(api_key=GROQ_API_KEY)

# Discord Botの設定
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    logging.info(f'Bot logged in as {bot.user}')

@bot.command()
async def ask(ctx, *, question: str):
    """ユーザーの質問をLLMに送信し、応答を取得"""
    system_prompt = {"role": "system", "content": "あなたの名前は観音林かおるです。女の子らしく、質問には日本語で完結に答えて"}
    user_prompt = {"role": "user", "content": question}
    chat_history = [system_prompt, user_prompt]

    try:
        response = client_groq.chat.completions.create(
            model="llama3-70b-8192",
            messages=chat_history,
            max_tokens=500,
            temperature=1.2
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = f"エラーが発生しました: {str(e)}"

    # 会話ログを保存
    logging.info(f'User: {question}\nBot: {reply}')
    
    # Discordチャンネルに返信
    await ctx.send(reply)

# Botの起動
bot.run(DISCORD_TOKEN)

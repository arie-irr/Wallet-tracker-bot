import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils.evm import get_evm_balance
from utils.solana import get_solana_balance

load_dotenv()

BOT_TOKEN = os.getenv("7699374290:AAEnNCRbM9yjU4qTSiI8ZZzI1GeeKMMthsM")
USER_ID = int(os.getenv("@arie_irr"))
EVM_WALLETS = os.getenv("0xd424c944c09d3b7b6fd3365756e2ad763b3cf078", "").split(",")
SOL_WALLETS = os.getenv("GJQoG4MxVWd24PL7qvfVG5E9fmRgY9L1k2g2KjiFuCT7", "").split(",")

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USER_ID:
        return
    msg = "📊 Saldo Wallet:\n\n"
    msg += "EVM:\n"
    for addr in EVM_WALLETS:
        balance = await get_evm_balance(addr)
        msg += f"- {addr[:6]}…{addr[-4:]}: {balance} ETH\n"
    msg += "\nSolana:\n"
    for addr in SOL_WALLETS:
        balance = await get_solana_balance(addr)
        msg += f"- {addr[:6]}…{addr[-4:]}: {balance} SOL\n"
    await update.message.reply_text(msg)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Halo! Kirim /saldo untuk cek wallet kamu.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("saldo", saldo))
    app.run_polling()

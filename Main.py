import os, asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from utils.evm import get_evm_balance
from utils.solana import get_solana_balance

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = int(os.getenv("TELEGRAM_USER_ID"))
EVM_WALLETS = os.getenv("EVM_WALLETS", "").split(",")
SOL_WALLETS = os.getenv("SOL_WALLETS", "").split(",")

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
    await update.message.reply_text("👋 Halo! Kirim /saldo untuk cek saldo wallet kamu.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("saldo", saldo))
    app.run_polling()
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = "8527398174:AAH56eJiatyqbhFTSxeAUWT8y0xLE0EcTVg"

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwSaDofb_FTXuKCZ9ICFitGZDmKCsyp8bXZNiXh72_Fv8MGCl3cbFcL5jMQzrXyMgEGIg/exec"


# === /start ===
def start(update, context):
    update.message.reply_text(
        "🤖 Halo! Bot Keuangan Siap Membantu!\n\n"
        "Ketik /help untuk melihat daftar perintah.\n"
        "Ketik /laporan untuk melihat daftar laporan.\n\n"
        "💰 /saldoawal <jumlah> — set saldo awal (sekali saja)\n"
        "2️⃣ pengeluaran <keterangan> <nominal>\n"
        "3️⃣ pemasukan <keterangan> <nominal>\n\n"
        "🧾 Contoh banyak data sekaligus:\n"
        "pengeluaran beli minyak 20000, beli bendera 30000"
    )


# === /help ===
def help_command(update, context):
    update.message.reply_text(
        "📘 *Panduan Penggunaan Bot Keuangan:*\n\n"
        "1️⃣ /saldoawal <jumlah>\n"
        "   → Set saldo awal (hanya sekali di awal)\n\n"
        "2️⃣ pengeluaran <keterangan> <nominal>\n"
        "   → Catat pengeluaran\n\n"
        "3️⃣ pemasukan <keterangan> <nominal>\n"
        "   → Catat pemasukan\n\n"
        "4️⃣ /laporan\n"
        "   → Tampilkan saldo dan 1 bulan transaksi terakhir\n\n"
        "💡 Contoh input banyak data:\n"
        "   pengeluaran beli minyak 20000, beli bendera 30000",
        parse_mode="Markdown"
    )


# === /saldoawal ===
def saldo_awal(update, context):
    if len(context.args) != 1:
        update.message.reply_text("Format salah!\nContoh: /saldoawal 500000")
        return

    nominal = int(context.args[0])
    data = {"jenis": "saldoawal", "nominal": nominal}

    response = requests.post(WEB_APP_URL, json=data)
    update.message.reply_text(response.text)


# === /laporan ===
def laporan(update, context):
    try:
        data = {"jenis": "laporan", "periode": "1bulan"}
        response = requests.post(WEB_APP_URL, json=data)
        update.message.reply_text(response.text)
    except Exception as e:
        update.message.reply_text("❌ Gagal mengambil laporan. Pastikan spreadsheet terhubung.")
        print("Error laporan:", e)


# === Pesan biasa (pengeluaran/pemasukan) ===
def handle_message(update, context):
    text = update.message.text.lower()

    # Bisa banyak data sekaligus, dipisahkan koma
    parts = [p.strip() for p in text.split(",") if p.strip()]
    responses = []

    for part in parts:
        words = part.split()
        if len(words) < 3:
            responses.append("⚠️ Format salah! Contoh: pengeluaran beli minyak 20000")
            continue

        jenis = words[0]
        nominal = int(words[-1])
        keterangan = " ".join(words[1:-1])

        data = {
            "jenis": jenis,
            "nominal": nominal,
            "keterangan": keterangan
        }

        try:
            r = requests.post(WEB_APP_URL, json=data)
            responses.append(r.text)
        except Exception as e:
            responses.append(f"Gagal kirim ke server: {e}")

    update.message.reply_text("\n\n".join(responses))


# === Main ===
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("saldoawal", saldo_awal))
    dp.add_handler(CommandHandler("laporan", laporan))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🤖 Bot sedang berjalan...")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

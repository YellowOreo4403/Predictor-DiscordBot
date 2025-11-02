import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from predict_model import predict_price

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("❌ Bot Token not found! Make sure .env file contains DISCORD_TOKEN")

class MyBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash Commands Synced")

client = MyBot()

@client.event
async def on_ready():
    print(f"✅ Bot online as {client.user}")

@client.tree.command(name="predict", description="Prediksi harga rumah di Indonesia")
@app_commands.describe(
    luas_bangunan="Luas bangunan (m2)",
    luas_tanah="Luas tanah (m2)",
    kamar="Jumlah kamar tidur",
    kamar_mandi="Jumlah kamar mandi",
    lantai="Jumlah lantai",
    usia="Usia bangunan (tahun)"
)
async def predict(
    interaction: discord.Interaction,
    luas_bangunan: float,
    luas_tanah: float,
    kamar: int,
    kamar_mandi: int,
    lantai: int,
    usia: float
):
    try:
        # Urutan harus sama seperti training model
        result = predict_price(
            luas_bangunan,
            luas_tanah,
            kamar,
            kamar_mandi,
            usia,
            lantai
        )

        # Convert ke rupiah (model output assumed in juta)
        harga_rupiah = result * 10_000

        # Format ke juta / miliar
        if harga_rupiah >= 1_000_000_000:
            value = harga_rupiah / 1_000_000_000
            unit = "miliar"
        else:
            value = harga_rupiah / 1_000_000
            unit = "juta"

        formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        await interaction.response.send_message(
            f"🏡 **Prediksi Harga Rumah**\n"
            f"💰 Rp {formatted} {unit}"
        )

    except Exception as e:
        await interaction.response.send_message(f"❌ Terjadi kesalahan: {e}")


# Run the bot
client.run(TOKEN)

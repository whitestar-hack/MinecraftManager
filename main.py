import os
import discord
from discord import app_commands
from python_aternos import Client

# Identifiants Aternos et Token Discord récupérés depuis les variables d'environnement
ATERNOS_USER = os.getenv("ATERNOS_USER")
ATERNOS_PASS = os.getenv("ATERNOS_PASS")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

class MyBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # Synchronise la commande /play globalement sur Discord
        await self.tree.sync()
        print(f"Bot connecté sous le nom de {self.user}")

client = MyBot()

@client.tree.command(name="play", description="Lance un serveur Minecraft Aternos")
@app_commands.describe(nomduserveur="Exemple: mon-serveur.aternos.me ou juste le nom de votre serveur")
async def play(interaction: discord.Interaction, nomduserveur: str):
    # Répond "Le bot réfléchit..." pour éviter l'expiration du message Discord
    await interaction.response.defer(thinking=True)

    try:
        # Connexion à Aternos
        at = Client.from_credentials(ATERNOS_USER, ATERNOS_PASS)
        servers = at.list_servers()

        target_server = None
        for serv in servers:
            if nomduserveur.lower() in serv.address.lower() or nomduserveur.lower() in serv.domain.lower():
                target_server = serv
                break

        if not target_server:
            await interaction.followup.send(f"❌ Aucun serveur trouvé correspondant à : `{nomduserveur}`.")
            return

        # Démarrage du serveur
        target_server.start()
        await interaction.followup.send(f"🚀 **{interaction.user.display_name}** a lancé le serveur **{target_server.address}** ! Connexion en cours...")

    except Exception as e:
        await interaction.followup.send(f"⚠️ Erreur lors du lancement : `{str(e)}`")

# Lancement du bot
client.run(DISCORD_TOKEN)
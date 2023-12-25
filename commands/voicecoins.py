from functions import *
from import_lib import *

class VoiceCoins(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_voice_time.start()

    def cog_unload(self):
        self.check_voice_time.cancel()

    @tasks.loop(seconds=60)  # Changed loop interval to 60 seconds
    async def check_voice_time(self):
        print("DEBUG: Running check_voice_time loop")
        for guild in self.bot.guilds:
            guild_members = await self.fetch_guild_members(guild)
            user_data_list = await self.fetch_user_data(guild_members)

            for member, user_data in zip(guild_members, user_data_list):
                if member.voice is not None and member.voice.channel is not None:
                    await self.update_user_voice_time(member, user_data)

    async def fetch_guild_members(self, guild):
        return [member for member in guild.members if not member.bot]

    async def fetch_user_data(self, guild_members):
        user_data_list = [get_player_data(member.id) for member in guild_members]
        return user_data_list

    async def update_user_voice_time(self, member, user_data):
        now = datetime.now()
        voice_start_time = user_data.get("voice_start_time")
    
        if member.voice is not None and member.voice.channel is not None:
            # User is in a voice channel
            if voice_start_time is not None:
                time_difference = now - voice_start_time
                minutes, _ = divmod(time_difference.seconds, 60)
                print(f"DEBUG: {member.name} has been in the voice chat for {minutes} minutes")
    
                if minutes >= 1:
                    coins_earned = await self.calculate_coins(minutes)
                    print(f"DEBUG: {member.name} earned {coins_earned} coins")
                    user_data["coins"] += coins_earned  # Accumulate coins instead of resetting
    
                # Print the current total coins
                print(f"DEBUG: {member.name}'s total coins: {user_data['coins']}")
            else:
                print(f"DEBUG: {member.name}'s voice_start_time is NULL. Setting it to {now}")
    
            # Update the database directly with the new voice_start_time
            user_data["voice_start_time"] = now
            save_player_data(member.id, user_data)
            print(f"DEBUG: User {member.id} data saved to the database")

    async def calculate_coins(self, minutes):
        if minutes >= 60:
            coins_earned = 1000
        else:
            coins_earned = min(10 * minutes, 600)
        return coins_earned

    @check_voice_time.before_loop
    async def before_check_voice_time(self):
        await self.bot.wait_until_ready()
        print("DEBUG: Waiting for bot to be ready")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot:
            if before.channel != after.channel:
                if before.channel is not None:
                    print(f"DEBUG: {member.name} left a voice channel")
                    # User left a voice channel
                    await self.on_voice_left(member)

                if after.channel is not None:
                    print(f"DEBUG: {member.name} joined a voice channel")
                    # User joined a voice channel
                    await self.on_voice_joined(member, before, after)

    async def on_voice_joined(self, member, before, after):
        print(f"DEBUG: {member.name} joined a voice channel")
        user_data = get_player_data(member.id)
        print(f"DEBUG: on_voice_joined - user_data before update: {user_data}")
        if user_data is not None:
            user_data["voice_start_time"] = datetime.now()
            print(f"DEBUG: {member.name}'s voice_start_time set to {user_data['voice_start_time']}")
            # Update the database directly with the new voice_start_time
            save_player_data(member.id, user_data)
            print(f"DEBUG: on_voice_joined - user_data after update: {user_data}")
        else:
            print(f"DEBUG: {member.name} did not have user_data")

    async def on_voice_left(self, member):
        print(f"DEBUG: {member.name} left a voice channel")
        user_data = get_player_data(member.id)
        print(f"DEBUG: on_voice_left - user_data: {user_data}")
        if user_data is not None:
            voice_start_time = user_data.get("voice_start_time")
            if voice_start_time is not None:
                duration_seconds = (datetime.now() - voice_start_time).total_seconds()
                duration_minutes = int(duration_seconds // 60)
                print(f"DEBUG: {member.name} was in the voice channel for {duration_minutes} minutes")

                # Calculate regular coins earned
                coins_earned = await self.calculate_coins(duration_minutes)
                print(f"DEBUG: {member.name} earned {coins_earned} coins")

                # Check if the user has accumulated an hour of voice chat time
                if duration_minutes >= 60 and duration_minutes % 60 == 0:
                    # Add bonus of 500 coins
                    bonus_coins = 500
                    user_data["coins"] += bonus_coins
                    print(f"DEBUG: {member.name} earned a bonus of {bonus_coins} coins")

                # Accumulate regular coins
                user_data["coins"] += coins_earned

                # Update last_voice_time in user_data
                user_data["last_voice_time"] = datetime.now()

                # Set voice_start_time to None in user_data to indicate that the user is not in a voice channel
                user_data["voice_start_time"] = None

                # Save the updated user_data in the database
                save_player_data(member.id, user_data)

                # Print the current total coins
                print(f"DEBUG: {member.name}'s total coins: {user_data['coins']}")

                # Send an embed message to a specific text channel
                channel_id = 1182986861577240687  # Replace with the actual channel ID
                target_channel = member.guild.get_channel(channel_id)
                if target_channel:
                    embed = discord.Embed(
                        title=f"{member.name} left the voice channel",
                        description=f"{member.name} was in the voice channel for {duration_minutes} minutes and earned {coins_earned} coins. They now have {user_data['coins']} coins.",
                        color=0x00ff00,  # You can customize the color
                    )
                    await target_channel.send(embed=embed)
                else:
                    print(f"DEBUG: Target channel with ID {channel_id} not found.")
            else:
                print(f"DEBUG: {member.name} did not have voice_start_time in user_data")
        else:
            print(f"DEBUG: {member.name} did not have user_data")


async def setup(bot):
    await bot.add_cog(VoiceCoins(bot))

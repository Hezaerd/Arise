from discord.ext import commands
import random

class Random(commands.Cog, name="Random"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Random cog loaded')

    @commands.hybrid_command(name="random", aliases=["rand"])
    async def random(self, ctx, min: int, max: int):
        '''Generates a random number between min and max'''
        '''Use: >random [min] [max]'''
        await ctx.reply(f'Result: {random.randint(min, max)}')

    @commands.hybrid_command(name="choose", aliases=["choice"])
    async def choose(self, ctx, choices: str):
        '''Chooses between multiple choices'''
        '''Use: >choose "choice1 choice2 choice3"'''
        choices = choices.split(" ")
        if not all(isinstance(choice, str) for choice in choices):
            await ctx.reply('**All choices have to be strings!**')
            return
        
        await ctx.reply(f'**Choice:** {random.choice(choices)}')

    @commands.hybrid_command(name="coinflip", aliases=["flip"])
    async def coinflip(self, ctx, prediction: str = None):
        '''Flips a coin'''
        '''Use: >coinflip [head/tail]'''
        result = random.choice(["Head", "Tail"])

        if prediction is not None and prediction.lower() not in ["head", "tail"]:
            await ctx.reply('**Invalid prediction!**')
            return

        if prediction is None:
            await ctx.reply(f':coin: {result} !')
        else:
            if prediction.lower() == result.lower():
                await ctx.reply(f':coin: {result} !\n**You won!**')
            else:
                await ctx.reply(f':coin: {result} !\n**You lost!**')

    @commands.hybrid_command(name="roll", aliases=["dice"])
    async def roll(self, ctx, dice: str):
        '''Rolls dice'''
        '''Use: >roll NdN (e.g. >roll 2d6 will roll 2 6-sided dice)'''
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.reply('Format has to be in NdN!')
            return

        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.reply(f':game_die: **{dice}**\n**Result:** {result}')

    @commands.hybrid_command(name="8ball", aliases=["8b"])
    async def eightball(self, ctx, *, question: str):
        '''Ask the magic 8ball a question'''
        '''Use: >8ball [question]'''
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it, yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Ask again later.',
            'Better not tell you now...',
            'Cannot predict now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good...',
            'Very doubtful.'
        ]
        await ctx.reply(f'**Question:** {question}\n:crystal_ball: **Answer:** {random.choice(responses)}')

    def _rps_to_emoji(self, choice: str):
        if choice.lower() == "rock":
            return ":right_facing_fist:"
        elif choice.lower() == "paper":
            return ":rightwards_hand:"
        elif choice.lower() == "scissors":
            return ":v:"

    @commands.hybrid_command(name="rps", aliases=["rockpaperscissors"])
    async def rps(self, ctx, choice: str):
        '''Play rock paper scissors'''
        '''Use: >rps [rock/paper/scissors]'''
        choice = choice.lower()

        beats = {
            'rock': 'scissors',
            'paper': 'rock',
            'scissors': 'paper'
        }

        if choice not in beats.keys():
            await ctx.reply('**Invalid choice!**')
            return
        
        bot_choice = random.choice(list(beats.keys()))

        you_msg = f'**You:** {self._rps_to_emoji(choice)}'
        bot_msg = f'**Bot:** {self._rps_to_emoji(bot_choice)}'

        if choice == bot_choice:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**Draw!**')
        elif beats[choice] == bot_choice:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**You won!**')
        else:
            await ctx.reply(f'{you_msg}\n{bot_msg}\n**You lost!**')

async def setup(bot):
    await bot.add_cog(Random(bot))
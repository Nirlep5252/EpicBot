class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command()
    async def math(self, ctx, *, msg: str = None):


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


def multiply(x, y):
    return x * y

def divide(x, y):
    return x / y


await ctx.message.reply("Select operation.")
await ctx.message.reply("1.Add")
await ctx.message.reply("2.Subtract")
await ctx.message.reply("3.Multiply")
await ctx.message.reply("4.Divide")

while True:

    choice = input("Enter choice(1/2/3/4): ")


    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == '1':
            await ctx.message.reply(num1, "+", num2, "=", add(num1, num2))

        elif choice == '2':
            await ctx.message.reply(num1, "-", num2, "=", subtract(num1, num2))

        elif choice == '3':
            await ctx.message.reply(num1, "*", num2, "=", multiply(num1, num2))

        elif choice == '4':
            await ctx.message.reply(num1, "/", num2, "=", divide(num1, num2))
        break
    else:
await ctx.message.reply("Invalid Input")

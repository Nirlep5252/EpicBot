from discord import Embed
import random

errortxt = ('Invalid parameters :warning:\n',
			'the valid format is: `~minesweeper <columns> <rows> <bombs>`\n',
			'For random columns, rows, and bombs use only `~minesweeper`')
errortxt = ''.join(errortxt)

async def play(ctx, columns = None, rows = None, bombs = None):
	if columns is None or rows is None and bombs is None:
		if columns is not None or rows is not None or bombs is not None:
			return await ctx.send(errortxt)
		else:
			# Gives a random range of columns and rows from 4-13 if no arguments are given
			# The amount of bombs depends on a random range from 5 to this formula:
			# ((columns * rows) - 1) / 2.5
			# This is to make sure the percentages of bombs at a given random board isn't too high
			columns = random.randint(4,13)
			rows = random.randint(4,13)
			bombs = columns * rows - 1
			bombs = bombs / 2.5
			bombs = round(random.randint(5, round(bombs)))
	try:
		columns = int(columns)
		rows = int(rows)
		bombs = int(bombs)
	except (ValueError, TypeError):
		return await ctx.send(errortxt)
	if columns > 13 or rows > 13:
		return await ctx.send('The limit for the columns and rows are 13 due to discord limits...')
	if columns < 1 or rows < 1 or bombs < 1:
		return await ctx.send('The provided numbers cannot be zero or negative...')
	if bombs + 1 > columns * rows:
		return await ctx.send(':boom:**BOOM**, you have more bombs than spaces on the grid or you attempted to make all of the spaces bombs!')
	
	# Creates a list within a list and fills them with 0s, this is our makeshift grid
	grid = [[0 for num in range (columns)] for num in range(rows)]

	# Loops for the amount of bombs there will be
	loop_count = 0
	while loop_count < bombs:
		x = random.randint(0, columns - 1)
		y = random.randint(0, rows - 1)
		# We use B as a variable to represent a Bomb (this will be replaced with emotes later)
		if grid[y][x] == 0:
			grid[y][x] = 'B'
			loop_count = loop_count + 1
		# It will loop again if a bomb is already selected at a random point
		if grid[y][x] == 'B':
			pass

	# The while loop will go though every point though our makeshift grid
	pos_x = 0
	pos_y = 0
	while pos_x * pos_y < columns * rows and pos_y < rows:
		# We need to predefine this for later
		adj_sum = 0
		# Checks the surrounding points of our "grid"
		for (adj_y, adj_x) in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]:
			# There will be index errors, we can just simply ignore them by using a try and exception block
			try:
				if grid[adj_y + pos_y][adj_x + pos_x] == 'B' and adj_y + pos_y > -1 and adj_x + pos_x > -1:
					# adj_sum will go up by 1 if a surrounding point has a bomb
					adj_sum = adj_sum + 1
			except Exception as error:
				pass
		# Since we don't want to change the Bomb variable into a number,
		# the point that the loop is in will only change if it isn't "B"
		if grid[pos_y][pos_x] != 'B':
			grid[pos_y][pos_x] = adj_sum
		# Increases the X values until it is more than the columns
		# If the while loop does not have "pos_y < rows" will index error
		if pos_x == columns - 1:
			pos_x = 0
			pos_y = pos_y + 1
		else:
			pos_x = pos_x + 1

	# Builds the string to be Discord-ready 
	string_builder = []
	for the_rows in grid:
		string_builder.append(''.join(map(str, the_rows)))
	string_builder = '\n'.join(string_builder)
	# Replaces the numbers and B for the respective emotes and spoiler tags
	string_builder = string_builder.replace('0', '||:zero:||')
	string_builder = string_builder.replace('1', '||:one:||')
	string_builder = string_builder.replace('2', '||:two:||')
	string_builder = string_builder.replace('3', '||:three:||')
	string_builder = string_builder.replace('4', '||:four:||')
	string_builder = string_builder.replace('5', '||:five:||')
	string_builder = string_builder.replace('6', '||:six:||')
	string_builder = string_builder.replace('7', '||:seven:||')
	string_builder = string_builder.replace('8', '||:eight:||')
	final = string_builder.replace('B', '||:bomb:||')

	percentage = columns * rows
	percentage = bombs / percentage
	percentage = 100 * percentage
	percentage = round(percentage, 2)

	embed = Embed(title='\U0001F642 Minesweeper \U0001F635', color=0xC0C0C0)
	embed.add_field(name='Columns:', value=columns, inline=True)
	embed.add_field(name='Rows:', value=rows, inline=True)
	embed.add_field(name='Total Spaces:', value=columns * rows, inline=True)
	embed.add_field(name='\U0001F4A3 Count:', value=bombs, inline=True)
	embed.add_field(name='\U0001F4A3 Percentage:', value=f'{percentage}%', inline=True)
	embed.add_field(name='Requested by:', value=ctx.author.display_name, inline=True)
	await ctx.send(content=f'\U0000FEFF\n{final}', embed=embed)
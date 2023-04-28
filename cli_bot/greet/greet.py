def greet():
	frame_width = 28
	title = "Welcome to address book!"

	# Borders
	top_border = "+" + "-" * (frame_width - 2) + "+"
	side_border = "|" + " " * (frame_width - 2) + "|"

	# Titles
	title_len = len(title)
	title_side_spaces = (frame_width - title_len - 2) // 2
	title_line = "|" + " " * title_side_spaces + title + " " * (frame_width - title_side_spaces - title_len - 2) + "|"

	# Print
	print(top_border)
	print(side_border)
	print(title_line)
	print(side_border)
	print(top_border)


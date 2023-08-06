def comparison(string1, string2):
	string1 = [s.strip() for s in string1.splitlines()]
	string2 = [s.strip() for s in string2.splitlines()]
	lines = []
	line = 0
	for s1 in string1:
		linenum = line
		for s2 in string2[line:]:
			if s2 == s1:
				line = linenum+1
				lines.append(linenum)
				break;
			linenum+=1
		else:
			lines.append(-1)
	return lines

def get_lines_changed(string1, string2):
	lines = comparison(string1, string2)
	string2 = [s.strip() for s in string2.splitlines()]
	max_length = len(string2)
	ctr = 0
	lines_changed = []
	while ctr < max_length:
		if ctr not in lines:
			lines_changed.append(ctr)
		ctr += 1
	return lines_changed

def name():
	print("Welcome to snipprcomparison, a snippet comparison package.")
 
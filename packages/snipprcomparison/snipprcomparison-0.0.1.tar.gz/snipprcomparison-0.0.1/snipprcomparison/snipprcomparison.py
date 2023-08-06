def comparison(string1, string2):
	string1 = [s.strip() for s in string1.splitlines()]
	string2 = [s.strip() for s in string2.splitlines()]
	lines = []
	line = 0
	for s1 in string1:
		for linenum, s2 in enumerate(string2, line):
			if s2 == s1:
				line = linenum
				lines.append(linenum)
				break;
		else:
			lines.append(-1)
	return lines

def name():
	print("Welcome to snipprcomparison, a snippet comparison package.")
 

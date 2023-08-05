def start():
    print("import successful")
class Group:
	count = 0
	pos = 0
	def __init__(self, count):
		self.count = count
	def reset(self):
		self.pos = 0
	def next(self):
		self.pos = self.pos + 1
		return int(self.pos / self.count)

def next(df, indexName, size, type):
	print(df.count())
	newPd = df.sort_values(indexName)
	if type == "count":
		g = Group(size)
		newPd["level"] = newPd.apply(lambda x: g.next(), axis = 1)
	else:
		pass
	return newPd
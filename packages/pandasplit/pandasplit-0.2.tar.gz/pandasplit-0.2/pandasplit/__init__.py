from pandas import DataFrame


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


def next(df, index_name, size, tpe):
    new_pd = df.sort_values(index_name)
    if tpe == "count":
        g = Group(size)
        new_pd["level"] = new_pd.apply(lambda x: g.next(), axis=1)
    else:
        pass
    return new_pd

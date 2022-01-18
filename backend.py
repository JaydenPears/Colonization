import csv


class PeacefulColony:
    def __init__(self):
        pass


class PlayersColony(PeacefulColony):
    def __init__(self):
        pass


class EnemyColony(PeacefulColony):
    def __init__(self):
        pass


class ActionWithTable:
    def __init__(self, filename):
        self.filename = filename

    def get_dict(self):
        dict = {}
        with open(self.filename, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            for index, row in enumerate(reader):
                if index != 0:
                    dict[row[0]] = row[1]
        return dict

    def rewrite_file(self, dict):
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow('number_save', 'lvl')
            for key in dict:
                writer.writerow([key, dict[key]])
import csv


class PeacefulColony:
    def __init__(self, time, number_of_lives):
        self.time = time
        self.number_of_lives = number_of_lives

    def __iadd__(self, delta):
        self.number_of_lives += delta

    def remove_lives(self, delta):
        if self.number_of_lives - delta <= 0:
            return False
        else:
            return True


class PlayersColony:
    def __init__(self, time, number_of_lives):
        self.time = time
        self.number_of_lives = number_of_lives

    def __iadd__(self, delta):
        if self.number_of_lives + delta <= 10:
            self.number_of_lives += delta

    def remove_lives(self, delta):
        if self.number_of_lives - delta <= 0:
            return False
        else:
            return True


class EnemyColony:
    def __init__(self, time, number_of_lives):
        self.time = time
        self.number_of_lives = number_of_lives

    def __iadd__(self, delta):
        self.number_of_lives += delta

    def remove_lives(self, delta):
        if self.number_of_lives - delta <= 0:
            return False
        else:
            return True


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

    def get_matrix(self):
        matrix = []
        with open(self.filename, 'rt', encoding="utf-8") as f:
            read_data = f.readlines()
        for i in read_data:
            matrix.append(list(map(int, i.split())))
        return matrix

    def get_nums_from_matrix(self):
        array = []
        matrix = self.get_matrix()
        for i in matrix:
            for j in i:
                array.append(j)
        array = sorted(list(set(array)))
        return array


# ?????????????? ?????? ???????????????????? ?????????????? ???????? ?? ?????????????? ????????????????????????????
def get_right_and_left_pos(matrix, number):
    first_pos = second_pos = None
    flag = False
    for i in range(len(matrix)):
        if flag:
            break
        for j in range(len(matrix[i])):
            if matrix[i][j] == number:
                first_pos = [j, i]
                flag = True
                break
    flag = False
    for i in range(len(matrix) - 1, -1, -1):
        if flag:
            break
        for j in range(len(matrix[i]) - 1, -1, -1):
            if matrix[i][j] == number:
                second_pos = [j, i]
                flag = True
                break
    return [first_pos, second_pos]

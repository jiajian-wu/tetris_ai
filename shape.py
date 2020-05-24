class Shape:

    def __init__(self, type):
        if type == "I":
            self.all_combos = [
                [[1, 1, 1, 1],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],

                [[1, 0, 0, 0],
                 [1, 0, 0, 0],
                 [1, 0, 0, 0],
                 [1, 0, 0, 0]]
            ]
            # list to hold rightmost position of a variant
            # For example, first variant has rightmost position at index 3,
            # second variant has rightmost position at index 0
            self.pos = [
                [[0, 0], [0, 1], [0, 2], [0, 3]],
                [[0, 0], [1, 0], [2, 0], [3, 0]]
            ]
            self.rightmost = [3, 0]

        elif type == "square":
            self.all_combos = [
                [[1, 1, 0, 0],
                 [1, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]]
            ]
            self.rightmost = [1]
            self.pos = [
                [[0, 0], [0, 1], [1, 0], [1, 1]]
            ]

        elif type == 'z':
            self.all_combos = [
                [[1, 1, 0, 0],
                 [0, 1, 1, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],

                [[0, 1, 0, 0],
                 [1, 1, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 0]],
            ]
            self.rightmost = [2, 1]
            self.pos = [
                [[0, 0], [0, 1], [1, 1], [1, 2]],
                [[0, 1], [1, 0], [1, 1], [2, 0]]
            ]

        elif type == "T":
            self.all_combos = [
                [[1, 1, 1, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],

                [[1, 0, 0, 0],
                 [1, 1, 0, 0],
                 [1, 0, 0, 0],
                 [0, 0, 0, 0]],

                [[0, 1, 0, 0],
                 [1, 1, 1, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]],

                [[0, 1, 0, 0],
                 [1, 1, 0, 0],
                 [0, 1, 0, 0],
                 [0, 0, 0, 0]]
            ]
            self.rightmost = [2, 1, 2, 1]
            self.pos = [
                [[0, 0], [0, 1], [0, 2], [1, 1]],
                [[0, 0], [1, 0], [1, 1], [2, 0]],
                [[0, 1], [1, 0], [1, 1], [1, 2]],
                [[0, 1], [1, 0], [1, 1], [2, 1]]
            ]

    def print_combos(self):
        count = 0
        for i in self.all_combos:
            count += 1
            print("Variant", count, ":")
            for j in i:
                for k in j:
                    print(k, " ", end='')
                print("")
            print("\n")

class Grid:
    def __init__(self, rows, columns, **kwargs):
        if "populator" in kwargs:
            populator = kwargs["populator"]
        else:
            populator = None

        self.width = columns
        self.height = rows

        self.rows = []
        for i in range(rows):
            row = []
            for j in range(columns):
                row.append(populator)
            self.rows.append(row)

    def out_of_range(self, kind, index, item):
        raise Exception(f"{kind} index {index} out of range (must be between 1 and {item}, inclusive)")

    def check_coords(func):
        def wrapper(self, row, column, *args, **kwargs):
            if 0 < row < self.height:
                if 0 < column < self.width:
                    func(self, row, column, *args, **kwargs)
                else:
                    self.out_of_range("Column", column, self.width)
            else:
                self.out_of_range("Row", row, self.height)

        return wrapper

    @check_coords
    def get(self, row: int, column: int):
        return self.rows[row - 1][column - 1]

    def get_row(self, index: int):
        if 0 < index < self.height:
            return self.rows[index - 1]
        else:
            self.out_of_range("Row", index, self.height)

    def get_column(self, index: int):
        if 0 < index < self.width:
            return [row[index - 1] for row in self.rows]

        else:
            self.out_of_range("Column", index, self.width)
    
    @check_coords
    def insert(self, row: int, column: int, value):
        old = self.get(row, column)
        self.rows[row - 1][column - 1] = value
        return old

    @check_coords
    def delete(self, row: int, column: int):
        return self.insert(row, column, None)

class Cube:
    def __init__(self, depth, height, width, **kwargs):
        if "populator" in kwargs:
            populator = kwargs["populator"]
        else:
            populator = None

        self.depth = depth
        self.height = height
        self.width = width

        self.slices = []
        for i in range(depth):
            grid = []
            for j in range(height):
                row = []
                for k in range(width):
                    row.append(populator)
                grid.append(row)
            self.slices.append(grid)
        
def test():
    grid = Grid(10, 10, populator="hi")

    print(grid.rows[0][0])

    print(grid.get(1, 1))
    print(grid.get(4, 7))
    print(grid.get_row(3))
    print(grid.get_column(8))

if __name__ == "__main__":
    test()
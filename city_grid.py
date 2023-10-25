import random


class CityGrid:
    def __init__(self, height: int, width: int, blocked_grids: float) -> None:
        """
        Initialize the CityGrid object.
        :param height: Height of the city grid.
        :param width: Width of the city grid.
        :param blocked_grids: Percentage of blocked grids (as a float).
        """
        self.height = height
        self.width = width

        if blocked_grids < 0 or blocked_grids > 100:
            raise ValueError("Blocked grids percentage must be between 0 and 100")

        self.blocked_grids = blocked_grids
        self.grids = self.__generate_grids()

    def __generate_grids(self):
        """
        Generates the initial grid with blocked and unblocked cells.
        :return: A list representing the city grid.
        """
        grids = [['🟥' for _ in range(self.width)] for _ in range(self.height)]

        blocked_grids_number = int((self.height * self.width) * (self.blocked_grids / 100))

        for _ in range(blocked_grids_number):
            row = random.randint(0, self.height - 1)
            column = random.randint(0, self.width - 1)
            if grids[row][column] != '❌':
                grids[row][column] = '❌'

        return grids

    def _place_tower(self, row: int, col: int, radius: int):
        """
        Place a tower at given coordinates with specified radius of coverage.
        :param row: Row coordinate of the tower.
        :param col: Column coordinate of the tower.
        :param radius: Radius of coverage for the tower.
        """
        if self.grids[row][col] == '❌':
            raise Exception("Not allowed to place tower here!")

        for i in range(max(0, row - radius), min(self.height, row + radius + 1)):
            for j in range(max(0, col - radius), min(self.width, col + radius + 1)):
                if self.grids[i][j] not in ["🗼", "❌"]:
                    self.grids[i][j] = '🟩'

        self.grids[row][col] = "🗼"

    def _is_valid_location(self, row: int, col: int) -> bool:
        """
        Check if the given location is a valid unobstructed block.
        """
        return 0 <= row < self.height and 0 <= col < self.width and self.grids[row][col] != '❌'

    def place_towers(self, radius: int):
        """
        Place minimum number of towers such that all non-obstructed blocks are covered.
        """
        uncovered_blocks = [(row, col) for row in range(self.height) for col in range(self.width) if
                            self._is_valid_location(row, col)]
        towers = []

        while uncovered_blocks:
            best_tower = None
            best_coverage = set()
            for row in range(self.height):
                for col in range(self.width):
                    if self._is_valid_location(row, col) and (row, col) not in towers:
                        coverage = set()
                        for r in range(max(0, row - radius), min(self.height, row + radius + 1)):
                            for c in range(max(0, col - radius), min(self.width, col + radius + 1)):
                                coverage.add((r, c))

                        covered = coverage.intersection(uncovered_blocks)
                        if len(covered) > len(best_coverage):
                            best_tower = (row, col)
                            best_coverage = covered

            if best_tower:
                self._place_tower(best_tower[0], best_tower[1], radius)
                uncovered_blocks = list(set(uncovered_blocks) - set(best_coverage))

        return self.grids

    def visualize_grid(self):
        """
        Visualize the city grid.
        :return:
        """

        return '\n'.join([' '.join(row) for row in self.grids])

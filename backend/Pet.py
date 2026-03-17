class Pet:
    @staticmethod
    def eat(energy: int, hunger: int, happiness: int, points: int) -> tuple[int, int, int, int]:
        """
        Simulates the pet eating, updating its energy, hunger, happiness, and points.

        :param energy: Current energy level of the pet (0-100).
        :param hunger: Current hunger level of the pet (0-100).
        :param happiness: Current happiness level of the pet (0-100).
        :param points: Current points of the pet (0-100).
        :return: A tuple (energy, hunger, happiness, points) after eating, each clamped between 0 and 100.
        """
        hunger -= 10
        energy += 5
        happiness += 5
        points += 10
        energy = max(0, min(100, energy))
        hunger = max(0, min(100, hunger))
        happiness = max(0, min(100, happiness))
        points = max(0, min(100, points))
        return energy, hunger, happiness, points

    @staticmethod
    def sleep(energy: int, hunger: int, happiness: int, points: int) -> tuple[int, int, int, int]:
        """
        Simulates the pet sleeping, updating its energy, hunger, happiness, and points.

        :param energy: Current energy level of the pet (0-100).
        :param hunger: Current hunger level of the pet (0-100).
        :param happiness: Current happiness level of the pet (0-100).
        :param points: Current points of the pet (0-100).
        :return: A tuple (energy, hunger, happiness, points) after sleeping, each clamped between 0 and 100.
        """
        energy += 10
        happiness += 5
        points += 10
        energy = max(0, min(100, energy))
        hunger = max(0, min(100, hunger))
        happiness = max(0, min(100, happiness))
        points = max(0, min(100, points))
        return energy, hunger, happiness, points

    @staticmethod
    def play(energy: int, hunger: int, happiness: int, points: int) -> tuple[int, int, int, int]:
        """
        Simulates the pet playing, updating its energy, hunger, happiness, and points.

        :param energy: Current energy level of the pet (0-100).
        :param hunger: Current hunger level of the pet (0-100).
        :param happiness: Current happiness level of the pet (0-100).
        :param points: Current points of the pet (0-100).
        :return: A tuple (energy, hunger, happiness, points) after playing, each clamped between 0 and 100.
        """
        hunger += 3
        energy -= 7
        happiness += 10
        points += 10
        energy = max(0, min(100, energy))
        hunger = max(0, min(100, hunger))
        happiness = max(0, min(100, happiness))
        points = max(0, min(100, points))
        return energy, hunger, happiness, points
from city_grid import CityGrid


def main():
    city = CityGrid(6, 6, 20)

    print(city.visualize_grid())
    city.place_towers(2)
    print(city.visualize_grid())


if __name__ == "__main__":
    main()

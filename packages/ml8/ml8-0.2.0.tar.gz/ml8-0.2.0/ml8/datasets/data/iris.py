"""

"""

def deal_iris():
    with open(r"data_old\iris.csv", "r") as iris_old, open(r"data\iris.csv", "a+") as iris:
        content = iris_old.readlines()
        num = 0
        for old_item in content:
            items = old_item.split(",")
            items[4] = items[4].replace("Iris-setosa", "0")\
                                .replace("Iris-versicolor", "1")\
                                .replace("Iris-virginica", "2")

            new_item = ",".join(items)
            iris.write(new_item)
            num += 1
    return num


def deal_boston_house_prices():
    with open(r"data_old\boston_house_prices.txt", "r") as boston_house_prices_old, open(r"data\boston_house_prices.csv", "a+") as boston_house_prices:
        content = boston_house_prices_old.readlines()
        num = 0
        for old_item in content:
            new_item = ','.join(old_item.split()) + "\n"
            boston_house_prices.write(new_item)
            num += 1
    return num




def main():
    # print (deal_iris())
    print (deal_boston_house_prices())


if __name__ == "__main__":
    main()
car = {
    "brand": "Toyota",
    "model": "Camry",
    "year": 2022,
    "color": "blue"
}


car.pop("color")


print("Key-Value pairs:")
print(car.items())


if "brand" in car:
    print("Brand key exists")
else:
    print("Brand key does not exist")
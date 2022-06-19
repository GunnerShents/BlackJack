from unicodedata import name
from dataclasses import dataclass


@dataclass
class Dog:

    name: str
    breed: str
    age: int


a_list = []
a_dog = Dog("Charlie", "Lab", 5)
a_list.append(a_dog)
b_dog = Dog("Bingo", "Lab", 5)
a_list.append(b_dog)


def double(my_list):
    b_list = []
    for dog in my_list:
        new_dog = Dog("Simon", dog.breed, 10)
        b_list.append(new_dog)
    return b_list


my_dogs = double(a_list)
a_list.extend(my_dogs)

for x in a_list:
    print(x.name)
    print(x.breed)
    print(x.age)

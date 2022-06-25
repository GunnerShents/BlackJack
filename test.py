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

print(a_list)


def find(alist: list[Dog], name: str) -> Dog | None:
    for x in alist:
        if x.name == name:
            return x


a_dog = find(a_list, "Bingo")
a_list.remove(a_dog)

print(a_list)

a = 150.0
print(a, int(a))

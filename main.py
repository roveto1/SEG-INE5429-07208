from item2 import item2
from item3 import item3

if __name__ == "__main__":

    choice = input("Run item 2 or item 3? (2/3): ").strip()
    if choice == '2':
        item2()
    elif choice == '3':
        item3()
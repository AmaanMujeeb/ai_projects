#This is a code for logical puzzle solving written by me to understand
#the concept of model checking algorithm and propositional logic in
#artificial intelligence
#Puzzle:
#1.There are three people and one of them did the crime
#2.Only the criminal lies
#3.Statements are:
#Alice = Bob did it
#Bob = I didn't do it
#Charlie = Bob is lying

from itertools import product

def knowledge_base(model):
    A = model["Alice"]
    B = model["Bob"]
    C = model["Charlie"]
    Alice_comment = (A and not B) or (not A and B)
    Bob_comment = B or not B
    Charlie_comment =  (C and not B) or (not C and B)
    only_one = (A + B + C) == 1
    return only_one and Alice_comment and Bob_comment and Charlie_comment

def main():
    symbols = ["Alice", "Bob", "Charlie"]
    for values in product([True, False], repeat=3):
        model = dict(zip(symbols, values))
        if knowledge_base(model):
            for person in symbols:
                status = "Guilty" if model[person] else "Innocent"
                print(f"{person}:{status}")
            return

if __name__ == "__main__":
    main()
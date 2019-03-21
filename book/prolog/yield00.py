def person():
    yield "Chelsea"
    yield "Hillary"
    yield "Bill"

def main():
    for p in person():
        print(p)
main()
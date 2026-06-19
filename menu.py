def menu(**callables):
    while True:
        keyword = input("Please type in something: ")
        if keyword not in callables:
            print("Word not in callables")
        else:
            return callables[keyword]()




if __name__ == "__main__":
    from unittest.mock import patch

    def hello():
        return "Hello!"

    def goodbye():
        return "Goodbye!"

    def test_menu():
        with patch("builtins.input", return_value="hello"):
            assert menu(hello=hello, goodbye=goodbye) == "Hello!"

        with patch("builtins.input", return_value="goodbye"):
            assert menu(hello=hello, goodbye=goodbye) == "Goodbye!"

    test_menu()
    print("All tests passed!")

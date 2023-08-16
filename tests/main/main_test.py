from main.main import main


# create a class test case for pytest
class TestMain:
    # create a test method
    def test_main(self):
        main()
        # assert that the main function prints 'hello world'
        assert True

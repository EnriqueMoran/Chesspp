import os, sys

libPath = "".join([dir + "\\" for dir in sys.path[0].split("\\")[:-1]]) + "server\\lib"
sys.path.append(os.path.join(sys.path[0], libPath))

from fileInput import FileReader


class FileInputTest(unittest.TestCase):

    def testLoadExistingFile(self):
        """
        Tests main configuration file is correctly read
        """
        fileReader = FileReader(["main.cfg"])
        fileReader.loadConfigFiles()
        fileReader.loadMain()    # store raw data from config file

        playerPieces = int(fileReader.player_data["player_pieces"])    # read player pieces from config file
        boardColumns = int(fileReader.board_data["board_columns"])    # read board's number of columns

        self.assertEqual(playerPieces, 16)
        self.assertEqual(boardColumns, 8)


    def testLoadNonexistentFile(self):
        """
        Tests main configuration non existent file is not read
        """
        fileReader = FileReader(["nonexistentFile.cfg"])    # load non existent file
        fileReader.loadConfigFiles()
        with self.assertRaises(FileNotFoundError):
            fileReader.loadMain()


    def testLoadWrongJsonFormat(self):
        fileReader = FileReader(["database.cfg"])    # database.cfg has wrong json format content
        fileReader.loadConfigFiles()
        with self.assertRaises(json.decoder.JSONDecodeError):
            fileReader.loadDatabase()


class BoardTest(unittest.TestCase):

    pass


class PlayerTest(unittest.TestCase):

    pass


if __name__ == "__main__":
    unittest.main()
import filecmp
import os
import subprocess
import unittest
from distutils.dir_util import copy_tree

# from py2UML import Py2UML
from py2UML import Py2UML


class TestMethods(unittest.TestCase):

    def setUp(self) -> None:
        self.ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        self.IN_PATH = os.path.join(self.ROOT_DIR, "../demoCode/projects/basicOOP")
        self.OUT_PATH = os.path.join(self.ROOT_DIR, "./actualOutputs")
        self.EXPECTED_OUT_PATH = os.path.join(self.ROOT_DIR, "./expectedOutputs")
        self.DIAGRAM_NAME = "basicOOP_CD"
        self.DOT_FILE = f"classes_{self.DIAGRAM_NAME}.dot"
        self.FILE_TYPE = "png"
        self.BUFFER_LOCATION = os.path.join(self.ROOT_DIR, "./buffer.py")

    def program_started(self, process_name):
        call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
        # use buildin check_output right away
        output = subprocess.check_output(call).decode()
        # check in last line for process name
        last_line = output.strip().split('\r\n')[-1]
        # because Fail message could be translated
        return last_line.lower().startswith(process_name.lower())

    # generates correct diagrams
    def test_baseOOP_Model_Exists(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE)
        expectedDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        self.assertTrue(os.path.exists(expectedDiagramPath), "file wasnt generated")

    def test_baseOOP_Model_right_model(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        actualDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated file doesnt match expected diagram")

    # Diagram extra feature Tests
    def test_baseOOP_Model_removes_dot(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, remove_dots=True)
        dot_exists = os.path.exists(f"{self.OUT_PATH}/{self.DOT_FILE}")
        diagram_exists = os.path.exists(f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}")
        self.assertFalse(dot_exists, "dot file isnt removed")
        self.assertTrue(diagram_exists, "diagram is made")

    def test_BaseOOP_Model_Black_List(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE,
                     black_list=["chessPiece.py", "__init__.py"], remove_dots=True)
        actual_diagram_blacklist = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        expected_diagram_blacklist = f"{self.EXPECTED_OUT_PATH}/basicOOP_blacklist.{self.FILE_TYPE}"
        matches = filecmp.cmp(actual_diagram_blacklist, expected_diagram_blacklist, True)
        self.assertTrue(matches, "output digram didnt remove blacklisted classes")

    def test_clean_source(self):
        project_path = os.path.join(self.ROOT_DIR, "../demoCode/projects/messyOOP")
        backup_path = os.path.join(self.ROOT_DIR, "../demoCode/projects/messyOOPbackup")
        copy_tree(backup_path, project_path)
        Py2UML.start(project_path, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, remove_dots=True,
                     clean_source=True)
        filelist = [f for f in os.listdir(project_path)]
        for f in filelist:
            matches = filecmp.cmp(project_path + "/" + f, self.IN_PATH + "/" + f)
            self.assertTrue(matches, f"{f} wasnt cleaned")

    def test_single_file(self):
        Py2UML.start(self.IN_PATH + "/chessGame.py", self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, remove_dots=True,
                     clean_source=True)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/{self.DIAGRAM_NAME}_one.{self.FILE_TYPE}"
        actualDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated file doesnt match expected diagram")

    def test_pie_graph(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, make_pie=True, remove_dots=True)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/Pie.png"
        actualDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.png"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated Pie doesnt match expected diagram")

    def test_show_location(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, remove_dots=True, show_path=True)
        self.assertTrue(self.program_started("explorer.exe"), "program wasnt launched")

    def test_show_diagram(self):
        Py2UML.start(self.IN_PATH, self.OUT_PATH, self.DIAGRAM_NAME, self.FILE_TYPE, remove_dots=True,
                     show_diagram=True)
        self.assertTrue(self.program_started("Microsoft.Photos.exe"), "program wasnt launched")


if __name__ == '__main__':
    unittest.main()

import filecmp
import os
import unittest
from distutils.dir_util import copy_tree
from os import path

from IO import IO
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

        self.py2uml = Py2UML(in_path=self.IN_PATH, out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME,
                             out_file_type=self.FILE_TYPE)

    def tearDown(self) -> None:
        filecmp.clear_cache()
        # self.delete_all(self.OUT_PATH)

    def makeDiagram(self, py2uml, dot=None):
        if not dot:
            dot = self.DOT_FILE
        files = py2uml.get_files()
        py2uml.make_dot(files)
        py2uml.make_diagram(dot)

    def delete_all(self, folder):
        filelist = [f for f in os.listdir(folder)]
        for f in filelist:
            os.remove(os.path.join(folder, f))

    # generates correct diagrams
    def test_baseOOP_Model_Exists(self):
        self.makeDiagram(self.py2uml)
        expectedDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        self.assertTrue(path.exists(expectedDiagramPath), "file wasnt generated")

    def test_baseOOP_right_model(self):
        self.makeDiagram(self.py2uml)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        actualDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated file doesnt match expected diagram")

    # Diagram extra feature Tests
    def test_baseOOP_removes_dot(self):
        p2u = Py2UML(in_path=self.IN_PATH, out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME,
                     out_file_type=self.FILE_TYPE, clean_up_dot=True)
        self.makeDiagram(p2u)
        dot_exists = path.exists(f"{self.OUT_PATH}/{self.DOT_FILE}")
        diagram_exists = path.exists(f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}")
        self.assertFalse(dot_exists, "dot file isnt removed")
        self.assertTrue(diagram_exists, "diagram is made")

    def test_BaseOOP_Black_List(self):
        p2u = Py2UML(in_path=self.IN_PATH, out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME + "bl",
                     black_list=["chessPiece.py", "__init__.py"], clean_up_dot=True)
        self.makeDiagram(p2u, f"classes_{self.DIAGRAM_NAME}bl.dot")
        actual_diagram_blacklist = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}bl.{self.FILE_TYPE}"
        expected_diagram_blacklist = f"{self.EXPECTED_OUT_PATH}/basicOOP_blacklist.{self.FILE_TYPE}"
        matches = filecmp.cmp(actual_diagram_blacklist, expected_diagram_blacklist, True)
        self.assertTrue(matches, "output digram didnt remove blacklisted classes")

    def test_clean_source(self):
        project_path = os.path.join(self.ROOT_DIR, "../demoCode/projects/messyOOP")
        backup_path = os.path.join(self.ROOT_DIR, "../demoCode/projects/messyOOPbackup")
        copy_tree(backup_path, project_path)
        p2u = Py2UML(in_path=project_path, out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME, clean_up_dot=True,
                     clean_source_code=True)
        self.makeDiagram(p2u)

        filelist = [f for f in os.listdir(project_path)]
        for f in filelist:
            matches = filecmp.cmp(project_path + "/" + f, self.IN_PATH + "/" + f)
            self.assertTrue(matches, f"{f} wasnt cleaned")

    def test_single_file(self):
        p2u = Py2UML(in_path=self.IN_PATH + "/chessGame.py", out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME,
                     clean_up_dot=True)
        self.makeDiagram(p2u)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/{self.DIAGRAM_NAME}_one.{self.FILE_TYPE}"
        actualDiagramPath = f"{self.OUT_PATH}/{self.DIAGRAM_NAME}.{self.FILE_TYPE}"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated file doesnt match expected diagram")

    def test_pie_graph(self):
        p2u = Py2UML(in_path=self.IN_PATH, out_path=self.OUT_PATH, diagram_name=self.DIAGRAM_NAME, clean_up_dot=True)
        buffer = ""
        filelist = p2u.get_files().split(" ")
        for f in filelist:
            buffer += IO.read(f)
        p2u.make_graph(buffer)
        expectedDiagramPath = f"{self.EXPECTED_OUT_PATH}/Pie.png"
        actualDiagramPath = f"{self.OUT_PATH}/Pie.png"
        result = filecmp.cmp(expectedDiagramPath, actualDiagramPath, True)
        self.assertTrue(result, "generated file doesnt match expected diagram")


if __name__ == '__main__':
    unittest.main()

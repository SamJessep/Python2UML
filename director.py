class Director:
    def __init__(self):
        self._builder = None
        # default features
        self._features = {
            "in_path": ".",
            "out_path": ".",
            "file_type": "png",
            "diagram_name": "DIAGRAM_NAME",
            "black_list": None,
            "clean_source": False,
            "remove_dots": False,
            "make_pie": False,
            "show_diagram": False,
            "show_path": False
        }

    def set_features(self, features):
        self._features = features

    def construct(self, builder):
        self._builder = builder
        self._builder.setup(self._features["out_path"], self._features["diagram_name"], self._features["file_type"])
        self._builder.build_get_files(self._features["in_path"], self._features["black_list"])
        if self._features["clean_source"] or self._features["remove_dots"]:
            self._builder.build_cleanup(self._features["clean_source"], self._features["remove_dots"])
        if self._features["show_diagram"] or self._features["show_path"]:
            self._builder.build_show_after(self._features["show_diagram"], self._features["show_path"])
        if self._features["make_pie"]:
            self._builder.build_make_graph()

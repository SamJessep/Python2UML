from glob import glob

import decorator


class GetFiles(decorator.Decorator):

    def __init__(self, BaseComponent, in_path='.', black_list=None):
        super().__init__(BaseComponent)
        self.in_path = in_path
        if black_list is None:
            black_list = []
        self.black_list = black_list

    def run(self):
        return self.get_files()

    def select_files(self):
        black_list = []
        for file in self.black_list:
            black_list += (glob(f'{self.in_path}/{file}*', recursive=True))
        if ".py" in self.in_path:
            return [self.in_path]
        white_list = glob(f'{self.in_path}/**/*.py', recursive=True)

        for selected_item in white_list:
            for unselected_item in black_list:
                if selected_item in unselected_item:
                    black_list.append(selected_item)
                    break

        return set(white_list) - set(black_list)

    def get_files(self):
        python_files = self.select_files()
        print(f"found: {python_files}")
        return python_files

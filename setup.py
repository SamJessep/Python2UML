from pip._internal import main
import pip

required_packages = ["graphviz", "autopep8", "argparse", "pylint", "pyreverse"]
class Setup:

	def install(self,package):
		try:
			__import__(package)
		except ImportError:
			permission = input(f"{package} is needed to run this program would you like to install it? Y/N: ").lower()
			if permission == 'y':
				main(['install', package])
				print(f'{package} was installed')
			else:
				print(f'{package} wasnt installed')
				return False

	def uninstall(self, package):
		try:
			__import__(package)
			permission = input(f"Remove {package}? Y/N: ").lower()
			if permission == 'y':
				main(['uninstall', package])
				print(f'{package} was uninstalled')
			else:
				print(f'{package} wasnt uninstalled')
				return True

		except ImportError:
			return False
			
	def install_all(self):
		for package in required_packages:
			self.install(package)
		print('all dependancies installed')

	def uninstall_all(self):
		for package in required_packages:
			self.uninstall(package)


Setup().install_all()
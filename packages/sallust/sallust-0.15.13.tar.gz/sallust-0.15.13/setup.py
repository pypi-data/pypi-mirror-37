from setuptools import setup

setup(
        name='sallust',
        version='0.15.13',
        packages=['sallust', 'sallust.GUI', 'sallust.Tools','sallust.Gui.GraphicsWidgets'],
        url='https://github.com/socisomer/Sallust',
        license='GNU General Public License v3.0',
        author='Joan Albert Espinosa',
        author_email='joanalbert.espinosa@gmail.com',
        description='sallust is a modern, open source testing support application. it helps track tests cases',
        install_requires=['lxml', 'matplotlib', 'Pillow', 'numpy', 'natsort', 'fpdf']
)

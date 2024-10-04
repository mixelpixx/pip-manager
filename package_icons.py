from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def get_package_icon(package_name):
    # This is a placeholder function. In a real implementation,
    # you would have a more comprehensive list of package icons.
    common_packages = {
        'numpy': 'icons/numpy.png',
        'pandas': 'icons/pandas.png',
        'matplotlib': 'icons/matplotlib.png',
        'scikit-learn': 'icons/scikit-learn.png',
        'tensorflow': 'icons/tensorflow.png',
        'pytorch': 'icons/pytorch.png',
        'django': 'icons/django.png',
        'flask': 'icons/flask.png',
    }
    
    if package_name.lower() in common_packages:
        return QIcon(common_packages[package_name.lower()])
    else:
        return QIcon('icons/default_package.png')

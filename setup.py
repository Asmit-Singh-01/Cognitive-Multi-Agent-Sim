from setuptools import setup, Extension
import sys

# Pybind11 setup integration
try:
    import pybind11
except ImportError:
    # Agar compilation ke waqt pybind11 na ho toh errors avoid karne ke liye
    pass

ext_modules = [
    Extension(
        'physics_core',
        ['bindings.cpp'],
        include_dirs=[
            # Path to pybind11 headers
            pybind11.get_include() if 'pybind11' in sys.modules else ""
        ],
        language='c++'
    ),
]

setup(
    name='physics_core',
    version='0.1',
    author='Asmit Singh',
    description='C++ Physics Core Engine bindings for Cognitive-Multi-Agent-Sim',
    ext_modules=ext_modules,
    zip_safe=False,
)

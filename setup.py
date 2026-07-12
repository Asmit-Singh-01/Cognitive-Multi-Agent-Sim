from setuptools import setup, Extension
import pybind11

# Hum C++ extension define kar rahe hain
ext_modules = [
    Extension(
        'fast_env', # Ye Python module ka naam hoga
        ['env_engine.cpp'],
        include_dirs=[pybind11.get_include()],
        language='c++',
        extra_compile_args=['-std=c++11', '-O3'] # -O3 extreme speed optimization ke liye hai
    ),
]

setup(
    name='CognitiveSimEngine',
    version='0.1.0',
    description='High-speed C++ engine for Multi-Agent RL',
    ext_modules=ext_modules,
)


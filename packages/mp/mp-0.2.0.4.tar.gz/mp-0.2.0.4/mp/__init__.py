__all__ = ['__version__', 'PythonInterpreter']
try:
    from mp.engine import PythonInterpreter
    from mp.version import __doc__, __version__

except ImportError as e:
    print('\n' + str(e))

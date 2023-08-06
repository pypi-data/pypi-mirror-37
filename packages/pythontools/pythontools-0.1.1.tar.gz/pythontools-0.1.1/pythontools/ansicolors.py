"""
ansicolors package wrapper. This module let the pythontools to use the color function event if the
ansicolors package is not installed.
"""

try:
    from colors import color
except ImportError:
    def color(text, **kwargs):
        """Returns the given text without modifications."""
        return text

"""ai-childrens-book-studio — desktop studio that turns a one-line premise
into a finished, illustrated children's picture book (text + art).

Public surface is intentionally thin: the Qt desktop shell lives in
``bookstudio.ui``, the orchestration pipeline in ``bookstudio.core``,
and every pluggable stage (story, rhyme, illustration, layout) is a
feature module registered against ``bookstudio.registry``.
"""

from bookstudio.version import __version__, BUILD_CHANNEL

__all__ = ["__version__", "BUILD_CHANNEL"]
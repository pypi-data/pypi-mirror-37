#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Create doc tree if you follows
:ref:`Sanhe Sphinx standard <sanhe_sphinx_doc_project_style_guide>`.
"""

from __future__ import print_function
from pathlib_mate import PathCls as Path

try:
    from .util import make_dir, make_file
    from .template import TC
    from .pkg import textfile
except:  # pragma: no cover
    from docfly.util import make_dir, make_file
    from docfly.template import TC
    from docfly.pkg import textfile


class ArticleFolder(object):
    """
    Represent an ``index.rst`` file with Title sitting in a directory.

    :param dir_path: A folder contains single rst file. The rst file path
        will be ``{dir_path}/{_filename}``.
    :param title: The title line above '=========='

    **中文文档**

    一篇 Article 代表着一个位于文件夹内的 ``index.rst`` 文件. 其中必然有至少一个标题元素.
    """
    _filename = "index.rst"

    def __init__(self, dir_path=None):
        self.dir_path = dir_path
        self._title = None

    @property
    def rst_path(self):
        """
        The actual rst file absolute path.
        """
        return Path(self.dir_path, self._filename).abspath

    @property
    def rel_path(self):
        """
        File relative path from the folder.
        """
        return "{}/{}".format(Path(self.dir_path).basename, self._filename)

    @property
    def title(self):
        """
        Title for the first header.
        """
        if self._title is None:
            self._title = self.get_title()
        return self._title

    def get_title(self):
        """
        Get title line from .rst file.

        **中文文档**

        从一个 ``_filename`` 所指定的 .rst 文件中, 找到顶级标题.
        也就是第一个 ``====`` 或 ``----`` 或 ``~~~~`` 上面一行.
        """
        header_bar_char_list = "=-~"

        cursor_previous_line = None
        for cursor_line in textfile.readlines(self.rst_path, strip="both"):
            for header_bar_char in header_bar_char_list:
                if cursor_line.startswith(header_bar_char):
                    flag_full_bar_char = cursor_line == header_bar_char * len(cursor_line)
                    flag_line_length_greather_than_1 = len(cursor_line) >= 1
                    flag_previous_line_not_empty = bool(cursor_previous_line)
                    if flag_full_bar_char \
                            and flag_line_length_greather_than_1 \
                            and flag_previous_line_not_empty:
                        return cursor_previous_line.strip()
            cursor_previous_line = cursor_line

        msg = "Warning, this document doesn't have any %s header!" % header_bar_char_list
        return None

    @property
    def sub_article_folders(self):
        """
        Returns all valid ArticleFolder sitting inside of
        :attr:`ArticleFolder.dir_path`.
        """
        l = list()
        for p in Path.sort_by_fname(
                Path(self.dir_path).select_dir(recursive=False)
        ):
            af = ArticleFolder(dir_path=p.abspath)
            try:
                if af.title is not None:
                    l.append(af)
            except:
                pass
        return l

    def toc_directive(self, maxdepth=1):
        """
        Generate toctree directive text.

        :param table_of_content_header:
        :param header_bar_char:
        :param header_line_length:
        :param maxdepth:
        :return:
        """
        articles_directive_content = TC.toc.render(
            maxdepth=maxdepth,
            article_list=self.sub_article_folders,
        )
        return articles_directive_content

    def __repr__(self):
        return "Article(title=%r)" % (self.title,)


class DocTree(object):
    """
    This class is designed for taking a rst file, and find all ``.. articles::``
    directives, then automatically generate ``.. toctree::`` directive.

    The file structure has to follow
    :ref:`Sanhe Sphinx standard <sanhe_sphinx_doc_project_style_guide>`.
    """

    @classmethod
    def fly(cls,
            conf_path,
            docname,
            source,
            maxdepth=1):  # pragma: no cover
        """
        Generate toctree directive for rst file.

        :param conf_path: conf.py file absolute path
        :param docname: the rst file relpath from conf.py directory.
        :param source: rst content.
        :param maxdepth: int, max toc tree depth.
        """
        directive_pattern = ".. articles::"
        if directive_pattern not in source:
            return source

        af = ArticleFolder(
            dir_path=Path(Path(conf_path).parent, docname).parent.abspath)
        toc_directive = af.toc_directive(maxdepth)

        lines = list()
        for line in source.split("\n"):
            if directive_pattern in line.strip():
                if line.strip().startswith(directive_pattern):
                    line = line.replace(directive_pattern, toc_directive, 1)
                    lines.append(line)
                    continue
            lines.append(line)
        return "\n".join(lines)

# -*- coding: utf-8 -*-
r"""
Grid View Adapter for skew tableaux

**Grid View skew tableau operations:**

.. csv-table::
    :class: contentstable
    :widths: 30, 70
    :delim: |

    :meth:`~SkewTableauGridViewAdapter.unicode_to_cell` | Static method for typecasting unicode to cell content
    :meth:`~SkewTableauGridViewAdapter.compute_cells` | Compute tableau cells as a dictionary { coordinate pair : Integer }
    :meth:`~SkewTableauGridViewAdapter.from_cells` | Create a new tableau from a cells dictionary
    :meth:`~SkewTableauGridViewAdapter.get_cell` | Get the tableau cell content
    :meth:`~SkewTableauGridViewAdapter.set_cell` | Set the tableau cell content
    :meth:`~SkewTableauGridViewAdapter.addable_cells` | List addable cells
    :meth:`~SkewTableauGridViewAdapter.removable_cells` | List removable cells
    :meth:`~SkewTableauGridViewAdapter.add_cell` | Add a cell
    :meth:`~SkewTableauGridViewAdapter.remove_cell` | Remove a cell

AUTHORS:
- Odile Bénassy, Nicolas Thiéry

"""
from sage.combinat.skew_tableau import *
from sage.rings.integer import Integer
from sage_widget_adapters.generic_grid_view_adapter import GridViewAdapter

class SkewTableauGridViewAdapter(GridViewAdapter):
    objclass = SkewTableau
    celltype = Integer # i.e. sage.rings.integer.Integer
    cellzero = None

    @staticmethod
    def compute_cells(obj):
        r"""
        From a tableau,
        return a dictionary { coordinates pair : Integer }
        TESTS:
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: st = SkewTableau([[None, None, 1, 2], [None, 1], [4]])
        sage: SkewTableauGridViewAdapter.compute_cells(st)
        {(0, 2): 1, (0, 3): 2, (1, 1): 1, (2, 0): 4}
        """
        return {(i,j):obj[i][j] for (i,j) in obj.cells()}

    @classmethod
    def from_cells(cls, cells={}):
        r"""
        From a dictionary { coordinates pair : Integer }
        return a corresponding tableau
        TESTS:
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: SkewTableauGridViewAdapter.from_cells({(0, 1): 2, (0, 3): 6, (1, 0): 3, (2, 0): 4})
        [[None, 2, None, 6], [3], [4]]
        """
        rows = []
        for i in range(max(pos[0] for pos in cells) + 1):
            rows.append([None] * (max(pos[1] for pos in cells if pos[0] == i) + 1))
        for pos in cells:
            rows[pos[0]][pos[1]] = cells[pos]
        try:
            return cls.objclass(rows)
        except:
            raise TypeError("This object is not compatible with this adapter (%s, for %s objects)" % (cls, cls.objclass))

    @staticmethod
    def get_cell(obj, pos):
        r"""
        Get cell value
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.get_cell(t, (1,1))
        7
        """
        try:
            return obj[pos[0]][pos[1]]
        except:
            raise ValueError("Cell %s does not exist!" % str(pos))

    @classmethod
    def set_cell(cls, obj, pos, val):
        r"""
        Set cell value
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.set_cell(t, (1,1), 8)
        [[1, 2, 5, 6], [3, 8], [4]]
        """
        tl = obj.to_list()
        tl[pos[0]][pos[1]] = val
        try:
            return cls.objclass(tl)
        except:
            raise ValueError("Value '%s' is not compatible!" % val)

    @staticmethod
    def addable_cells(obj):
        r"""
        List object addable cells
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.addable_cells(t)
        [(0, 4), (1, 2), (2, 1), (3, 0)]
        """
        return obj.shape().outside_corners()

    @staticmethod
    def removable_cells(obj):
        r"""
        List object removable cells
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.removable_cells(t)
        [(0, 3), (1, 1), (2, 0)]
        """
        return obj.corners()

    @classmethod
    def add_cell(cls, obj, pos, val):
        r"""
        Add cell
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.add_cell(t, (3, 0), 8)
        [[1, 2, 5, 6], [3, 7], [4], [8]]
        sage: SkewTableauGridViewAdapter.add_cell(t, (1, 2), 8)
        [[1, 2, 5, 6], [3, 7, 8], [4]]
        sage: SkewTableauGridViewAdapter.add_cell(t, (2, 0), 9) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Cell position '(2, 0)' is not addable.
        """
        if not pos in cls.addable_cells(obj):
            raise ValueError("Position '%s' is not addable." % str(pos))
        tl = obj.to_list()
        if pos[0] >= len(tl):
            tl = tl + [[val]]
        else:
            tl[pos[0]].append(val)
        try:
            return cls.objclass(tl)
        except:
            raise ValueError("Cannot create a %s with this list!" % cls.objclass)

    @classmethod
    def remove_cell(cls, obj, pos):
        r"""
        Remove cell
        TESTS::
        sage: from sage.combinat.tableau import SkewTableau
        sage: from sage_widget_adapters.combinat.tableau_grid_view_adapter import SkewTableauGridViewAdapter
        sage: t = SkewTableau([[1, 2, 5, 6], [3, 7], [4]])
        sage: SkewTableauGridViewAdapter.remove_cell(t, (1, 1))
        [[1, 2, 5, 6], [3], [4]]
        sage: SkewTableauGridViewAdapter.remove_cell(t, (2, 1)) # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        ValueError: Cell position '(2, 1)' is not removable.
        """
        if not pos in cls.removable_cells(obj):
            raise ValueError("Cell position '%s' is not removable." % str(pos))
        tl = obj.to_list()
        tl[pos[0]].pop()
        if not tl[pos[0]]:
            tl.pop()
        try:
            return cls.objclass(tl)
        except:
            raise ValueError("Cannot create a %s with this list!" % cls.objclass)

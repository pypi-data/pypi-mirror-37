from __future__ import print_function

from contextlib import contextmanager

from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class plot_manager(object):
    """ Creates pdf file using :func:`matplotlib.backends.backend_pdf.PdfPages`
 and returns the handle to this pdf.

    `*args` and `*kwargs` are passed to `PdfPages`
    """
    def __init__(self, outfile, print_outfile=True, *args, **kwargs):
        self.outfile = outfile
        self.print_outfile = print_outfile
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.pp = PdfPages(self.outfile, *self.args, **self.kwargs)
        return self.pp

    def __exit__(self, type, value, traceback):
        self.pp.close()
        if self.print_outfile:
            print(self.outfile)


class single_fig_manager(object):
    """ Create a :class:`matplotlib.figure.Figure`

    `args` and `kwargs` are passed to the :class:`Figure` constructor

    :param matplotlib.backends.backend_pdf.PdfPages pp: handle that has a
        savefig method
    """
    def __init__(self, pp, *args, **kwargs):
        self.pp = pp
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        self.fig = Figure(*self.args, **self.kwargs)
        FigureCanvas(self.fig)
        return self.fig

    def __exit__(self, type, value, traceback):
        self.pp.savefig(self.fig, transparent=True)
        # self.pp.savefig(self.fig, transparent=True, bbox_inches="tight")
        self.fig.clear


class single_ax_manager(single_fig_manager):
    """ Create an axis with a single subplot in a `Figure` object.

    Subclassed from :class:`single_fig_manager`, and all the arguments are the
    same
    """
    def __enter__(self):
        self.fig = super(single_ax_manager, self).__enter__()
        ax = self.fig.add_subplot(1, 1, 1)
        return ax


@contextmanager
def plot_ax_manager(outfile, *args, **kwargs):
    """ Create a pdf with name `outfile` containing one plot"""
    with plot_manager(outfile, *args, **kwargs) as pp:
        with single_ax_manager(pp) as ax:
            yield ax

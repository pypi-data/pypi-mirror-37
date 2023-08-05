from datetime import datetime
import numpy as np
import xarray
from matplotlib.pyplot import figure
from matplotlib.colors import LogNorm
from matplotlib.ticker import LogFormatterMathtext  # ,ScalarFormatter
import matplotlib.colors as colors
from typing import Tuple, Sequence, Any
#
from sciencedates.ticks import tickfix

sfmt = LogFormatterMathtext()
#    sfmt = ScalarFormatter()
#    sfmt.set_powerlimits((-2,2)) #force scientific notation for numbers with 10^a where A<a<B
#    sfmt.set_scientific(True)
#    sfmt.set_useOffset(False)

# bright events
# vlims = {4278:[500,15000], 4861:[100,1000], 5200:[100,2000], 6700:[100,2000],
#         5577:[4e3,1e5],6300:[1000,20000]}

# hard events like 2007-03-23
vlims = {'4278': [100, 15000],
         '4861': [50, 1000],
         '5200': [100, 2000],
         '6700': [100, 2000],
         '5577': [100, 5e4],
         '6300': [50, 1000]}

chem = {'4278': r'$N_{2}^{+}$ 1N',
        '4861': r'H$_\beta$',
        '5200': '[NI]',
        '6700': r'N$_2$ 1P',
        '5577': '[OI]32',
        '6300': '[OI]21'}


def plotmspspectra(I: xarray.Dataset, elfid):
    wl = list(I.data_vars.keys())
    # %% plots
    fg = figure(figsize=(20, 12))
    ax = fg.subplots(len(wl), 1, sharex=True)

    spectrasubplot(I, fg, ax, elfid, False, vlims)
    tickfix(I.time, fg, fg.gca())

    fg.text(0.89, 0.5, 'Rayleighs', ha='center', va='center', rotation='vertical')
    fg.text(0.01, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.utcfromtimestamp(I.time[0].item() / 1e9).strftime('%Y-%m-%d') +
                '  Meridian Scanning Photometer: Peak Intensity',
                y=0.99)
    fg.tight_layout(pad=1.1)


def spectrasubplot(I: xarray.Dataset, fg, ax,
                   elfid: Sequence[float], indlbl: bool=False, clim=None):
    wl = list(I.data_vars.keys())
    assert isinstance(indlbl, bool)

    for a, l in zip(ax, wl):
        if clim is None:
            c: Any = (None, None)
        elif isinstance(clim, dict) and l in vlims:
            c = vlims[l]
        elif len(clim) == 2:
            c = (None, None)
        else:
            wl

        h = a.pcolormesh(I.time, I.elevation,
                         I[l].values.T,
                         cmap='cubehelix_r', norm=LogNorm(),
                         vmin=c[0], vmax=c[1])

        hc = fg.colorbar(h, ax=a, format=sfmt)
        if indlbl:
            hc.set_label('Rayleighs')

        for f in elfid:
            a.axhline(f, color='gold', alpha=0.8, linestyle='--')

        a.set_title(f'{float(l) / 10:.1f} nm  ' + chem[l])

        a.invert_yaxis()
        a.autoscale(True, tight=True)


def plotratio(ratio, wlreq: Tuple[str, str], I: xarray.Dataset,
              elfid, ratlim, verbose: bool=False):
    if ratio is None:
        return

    ratio = ratio.T

    fg = figure(figsize=(20, 12))
    ax = fg.subplots(3, 1, sharex=True)

    spectrasubplot(I, fg, ax[:2], elfid, True, [1e3, 1e4])  # FIXME make ratlim based

    hi = ax[2].pcolormesh(ratio.time, ratio.elevation,
                          ratio.values,
                          cmap='bwr',
                          norm=MidpointNormalize(midpoint=ratlim[1]),
                          vmin=ratlim[0], vmax=ratlim[2])

    for f in elfid:
        ax[2].axhline(f, color='gold', alpha=0.85, linestyle='--')

    ax[2].invert_yaxis()
    ax[2].autoscale(True, tight=True)

    fg.colorbar(hi, ax=ax[2]).set_label(f'{wlreq[0]} / {wlreq[1]}')

    fg.text(0.085, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')

    fg.suptitle(datetime.utcfromtimestamp(I.time[0].item() / 1e9).strftime('%Y-%m-%d') +
                f'  Meridian Scanning Photometer: {wlreq[0]} / {wlreq[1]} Intensity Ratio')
    # y=0.99)

    tickfix(ratio.time, fg, ax[2])
# %% make lots of line subplots
    if verbose:
        nsub = ratio.time.size
        ncol = 4
        nrow = nsub // ncol

        fg = figure()
        axs = fg.subplots(nrow, ncol, sharey=True, sharex=True)
        for i, ax in enumerate(axs.ravel()):
            if i == nsub:
                break
            ax.plot(ratio[:, i], ratio.elevation)
            ax.set_title(datetime.utcfromtimestamp(ratio.time[i].item() / 1e9).strftime('%H:%M:%S'))

            for f in elfid:
                ax.axhline(f, color='gold', alpha=0.85, linestyle='--')

        ax.invert_yaxis()

        fg.text(0.05, 0.5, 'elevation from North [deg.]', ha='center', va='center', rotation='vertical')
        fg.text(0.5, 0.02, f'Intensity ratio: {wlreq[0]} / {wlreq[1]}', ha='center', va='center')

        fg.suptitle(datetime.utcfromtimestamp(I.time[0].item() / 1e9).strftime('%Y-%m-%d') +
                    f'  Meridian Scanning Photometer: {wlreq[0]} / {wlreq[1]} Intensity Ratio')


class MidpointNormalize(colors.Normalize):
    """
    http://matplotlib.org/users/colormapnorms.html
    may appear in a future version of Matplotlib
    """

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        # I'm ignoring masked values and all kinds of edge cases to make a
        # simple example...
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return np.ma.masked_array(np.interp(value, x, y))

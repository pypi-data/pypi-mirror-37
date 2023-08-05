from ..lightcurves import *

def test_download_kepler_lc():
    '''
    This function tests the wrapper for downloading
    a single quarter of Kepler data.
    '''

    lc = download_kepler_lc('Kepler-17')
    lc.plot(marker='.', linewidth=0)
    folded = lc.fold(1.48571092)
    folded.scatter(marker='.', linewidth=0)

def test_locate():
    '''
    This function should draw a single circle
    around every transit in the Kepler-17 light curve.
    '''

    # download a Kepler-17 light curve
    lc = download_kepler_lc('Kepler-10', quarter=1)

    # make a light curve plot
    lc.plot(marker='.', linewidth=0)

    # draw lines for the planet on top
    locations = locate_transits(lc, period=0.837491, t0=2454964.57513, color='royalblue', name='Kepler-10b')
    locations = locate_transits(lc, period=45.294301, t0=2455062.26648, color='darkorange', name='Kepler-10c')

    plt.legend(bbox_to_anchor=(1,1), loc='upper left')
    plt.tight_layout()

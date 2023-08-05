from lightkurve import KeplerLightCurveFile, lightcurve
import matplotlib.pyplot as plt
import numpy as np
from .tools import *

def download_kepler_lc(star='Kepler-186',
                       quarter='all',
                       cadence='long',
                       quality_bitmask='hard',
                       kind='PDCSAP_FLUX'):
    '''
    This function is a wrapper to download one or more quarters of Kepler
    lightcurve data, and extract a LightCurve object from it.

    When downloading a Kepler LightCurveFile from online, we get lots
    of information, including multiple different kinds of light curves
    for the same star. The goal of this little wrapper is to make it
    easy to get just one single light curve to play with.

    This has been tested only on data from the main Kepler mission.
    For K2 data, you may need to download a TPF.

    Parameters
    ----------

    star: str, int
        The name of the star whose light curve you want to download.
        This can be a name ("Kepler-42", "KOI-961") or a KIC number
        (8561063)

    quarter: str, int
        Which Kepler quarter to download?
            'all' = download the entire mission of data
            1, 2, 3 ... = download a specific quarter

    cadence: str
        'long' for Kepler long cadence
        'short' for Kepler short cadence

    quality_bitmask: str, int
        'none' = ignore no data
        'default' = ignore data with serious quality issues
        'hard' = be a little more cautious in what we call good data
        'hardest' = be too cautious about what we call good data

    kind: str
        "SAP_FLUX" = simple aperture photometry
        "PDCSAP_FLUX" = SAP, with pre-search data conditioning applied to get
        rid of some instrumental systematics from the light curves (but watch
        out! some astrophysical signals might be messed up too!)

    Returns
    -------

    lc: LightCurve object
        This is a `lightkurve`-style LightCurve object, which contains
        the attributes `lc.time` (times in JD) and `lc.flux` (the brightness
        of the star), as well as lots of methods for analysis and plotting.

    '''

    # download a KeplerLightCurveFile from the MAST archive
    lcf = KeplerLightCurveFile.from_archive(star,
                                            quarter=quarter,
                                            cadence=cadence,
                                            quality_bitmask=quality_bitmask)

    # if a list, stitch things together (crudely! will be terrible for SAP!)
    if type(lcf) == list:

        # make a normalized light curve from the first light curve file
        lc = lcf[0].get_lightcurve(kind).normalize()

        # append the normalized light curves from all other light curve files
        for f in lcf[1:]:
            thisquarter = f.get_lightcurve(kind)
            lc = lc.append(thisquarter.normalize())

    # if a single quarter, simply return that light curve
    else:
        lc = lcf.get_lightcurve(kind)

    # return the light curve
    return lc



def locate_transits(lc, period, t0=0, name=None, color='green', **kw):

    '''

    This function takes in a lightcurve object along with the planet's
    period and epoch in order to identify on the plot each expected location
    of a transit

    lc should be a lightkurve object which has times and fluxes.
    period should be in days
    t0 should be in BJD
    '''

    # pull out time and flux arrays
    time = lc.time
    flux = lc.flux

    # figure out the right time format
    if isinstance(lc, lightcurve.FoldedLightCurve):
        epoch = 0.0
        period = 1.0
    else:
        if lc.time_format == 'bkjd':
            epoch = bjd2bkjd(t0)
        elif lc.time_format == 'btjd':
            epoch = bjd2btjd(t0)
        else:
            epoch = t0

    # calculate the integer orbit numbers, and mid-transit locations
    allorbitnumbers = np.round((lc.time - epoch)/period).astype(np.int)
    n = np.arange(np.min(allorbitnumbers), np.max(allorbitnumbers))
    transit_loc = n*period + epoch

    #avg_flux = np.median(flux)
    #fig,ax = plt.subplots()
    #plt.title('Transit locations')
    #plt.xlabel('Time (JD)')
    #lt.ylabel('Flux')
    #plt.xlim(time[0],time[-1])
    #plt.scatter(time,flux)

    for i, this_transit in enumerate(transit_loc):
        if i == 0:
            label=name or '{period}{multiply}n + {epoch:.5f}'.format(multiply=r'$\times$', **locals())
        else:
            label=None
        plt.axvline(this_transit, ymin=0.9, ymax=0.95, alpha=0.4, color=color, label=label, **kw)
    return transit_loc


def extract_transits(lc, period, epoch, duration, baseline):
    '''
    Not yet implemented.
    '''

    time = lc.time
    flux = lc.flux


    return transits, notransits

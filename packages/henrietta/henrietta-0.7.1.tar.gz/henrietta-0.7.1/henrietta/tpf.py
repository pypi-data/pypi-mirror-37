from lightkurve import KeplerTargetPixelFile
from .imports import *
from .tools import *

def download_kepler_tpf(star='Kepler-186',
                        quarter=1,
                        cadence='long',
                        **kw):
    '''
    This function is a wrapper to download one or more "Target Pixel Files" (TPF)
    of Kepler data. Each TPF is basically a movie; it contains a time series
    of images in a tiny little area around a particular Kepler target.

    This has been tested only on data from the main Kepler mission and K2.

    Parameters
    ----------

    star: str, int
        The name of the star whose light curve you want to download.
        This can be a name ("Kepler-42", "KOI-961") or a KIC number
        (8561063)

    quarter: str, int
        Which Kepler quarter to download?
            1, 2, 3 ... = download a specific quarter

    cadence: str
        'long' for Kepler long cadence
        'short' for Kepler short cadence

    Returns
    -------

    tpf: KeplerTargetPixelFile object
        This is a `lightkurve`-style TargetPixelFile object, which contains
        the attributes `tpf.time` (times in JD) and `tpf.flux` (the brightness
        of each pixel as a function of time), as well as lots of methods for
        analysis and plotting.
    '''

    # download a KeplerLightCurveFile from the MAST archive
    tpf = KeplerTargetPixelFile.from_archive(star,
                                             quarter=quarter,
                                             cadence=cadence,
                                             **kw)
    return tpf

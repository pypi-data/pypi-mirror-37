import numpy as np, matplotlib.pyplot as plt


def create_test_array(N=5, xsize=100, ysize=100, nstars=None, single=False, seed=None):
    '''
    Create a fake stack of images of stars
    (no cosmics injected, no jitter, Gaussian PDF).

    Parameters:
    -----------
    N : int
        The number of images.
    xsize : int
        The number of columns.
    ysize : int
        The number of rows.
    nstars : int
        The number of stars to include (defaults to be \propto to image area)
    single : bool
        Should this be just a single star in the center, or should it be many?

    Returns
    -------
    image_stack : array
        (N, ysize, xsize) in shape
    '''

    # seed the random number generator
    np.random.seed(seed)

    # create images of x, y, and an empty one to fill with stars
    x1d = np.arange(0, xsize)
    y1d = np.arange(0, ysize)
    x, y = np.meshgrid(x1d, y1d)
    stars = np.zeros_like(x)

    # create N random position for stars
    if single:
        nstars = 1
        sx = np.random.normal(xsize / 2.0, 1)
        sy = np.random.normal(ysize / 2.0, 1)
    else:
        if nstars is None:
            nstars = np.minimum(int(xsize * ysize / 4), 1000)
        sx = np.random.uniform(0, xsize, nstars)
        sy = np.random.uniform(0, ysize, nstars)

    # set some background level
    bg = 30

    # create a semi-reasonable magnitude distribution for stars
    if single:
        topmag = 5
    else:
        topmag = 10
    sf = 10000 * 10**(-0.4 * np.random.triangular(0, topmag, topmag, nstars))

    # define the cartoon PSF for the stars
    sigma = 1.0

    def gauss(x, y, x0, y0):
        return np.exp(-0.5 * ((x - x0)**2 + (y - y0)**2) / sigma**2)

    # create a cube with an image for each star, and sum them together into one image
    stars = (sf * gauss(x[:, :, np.newaxis],
                        y[:, :, np.newaxis], x0=sx, y0=sy)).sum(2)

    # create a model images
    model = (bg + stars)[np.newaxis, :, :] * np.ones(N).reshape((N, 1, 1))

    # add some noise to it
    image = np.random.normal(model, np.sqrt(model))

    return image

'''
Define an Aperture object, which
    -has a location
    -does photometry
    -can be plotted and picked
    -can be unplotted
'''

from ..imports import *
import photutils

class InteractiveAperture(photutils.CircularAperture):

    def __init__(self, name='', pos=(0,0), loupe=None,  aperture_radius=3):

        # initialize the CircularAperture as normal
        photutils.CircularAperture.__init__(self, pos, aperture_radius)

        # keep track of this aperture's name
        self.name = name

        self.loupe = loupe

        self.flux = np.nan

    def plot(self, ax):
        '''
        Plot this aperture onto the given axes.
        '''

        # create an empty dictionary to store any plots
        self.plotted = {}

        # (this can handle only single-position apertures)
        pos = self.positions[0]

        # (pull out the apeture radius)
        aperture_radius = self.r

        # create the circle
        self.plotted['circle'] = plt.Circle(pos, aperture_radius, color='black',fill=False,zorder=100,picker=True)
        ax.add_artist(self.plotted['circle'])
        self.plotted['marker'] = plt.scatter(pos[0], pos[1], marker='+', alpha=0.3, color='black')
        self.plotted['label'] = plt.text(pos[0]+aperture_radius+1, pos[1], self.name, va='center', zorder=11, color='black')

    def erase(self):
        '''
        Remove any traces of this aperture from the plot.
        '''

        for k in self.plotted.keys():

            self.plotted[k].remove()
            #with self.loupe.out:
            #    print('  removing {}'.format(k))

    def update(self):
        '''
        After a plot has already been created, update its hidden properties,
        as well as its appearance on the interactive plot.
        '''

        # update the radius
        self.r = self.loupe.aperture_radius

        # update the plot
        pos = self.positions[0]
        self.plotted['circle'].set_radius(self.r)
        self.plotted['label'].set_position((pos[0]+self.r+1, pos[1]))
        self.plotted['marker'].set_offsets(pos)

        # actually do the photometry
        self.phot_table = photutils.aperture_photometry(self.loupe.image, self)
        self.flux = self.phot_table['aperture_sum'].data[0]

    def __str__(self):
        '''
        How should this aperature appear as a string (for example, if it is
        included in a `'{}'.format()` statement)?
        '''
        return '{:>8} at ({:4.1f}, {:4.1f}) sums to {:10.1f} (area of {:.1f} pixels).'.format(self.name, self.positions[0][0], self.positions[0][1],  self.flux, self.area())

class ApertureWithBackground(InteractiveAperture):
    pass
    #def __init__(self, name='', pos=(0,0), aperture_radius=3 ):
    #    pass

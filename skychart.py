from astropy.coordinates import SkyCoord, EarthLocation, AltAz, ICRS, GCRS, get_moon, get_body
from astropy.time import Time
from astropy.wcs import WCS
from astropy.table import Table
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.scale as mscale
import matplotlib.font_manager as fm
from util import *
import time as pytime
start_time = pytime.time()

font_path = './fonts/Libertinus-7.040/static/OTF/'
font_files = fm.findSystemFonts(fontpaths=font_path)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
    
mscale.register_scale(stereographic.StereographicZenithScale)
red = '#C80815'
light_blue = '#4673bc'
dark_yellow = '#d4b300'

def skychart(time=None, location=None, show=False):
    '''
    Return skychart at a time in a location. Time should be an astropy.time.Time instance and location should be an astropy.coordinates.EarthLocation instance.'''
    # time
    if time is None:
        time = Time.now()
        # time = Time('2022-12-23 8:00:00')
    # oberving location
    if location is None:
        loc_lat = 25.62
        loc_lon = 101.13
        loc_height = 2223
        location = EarthLocation(lat=loc_lat * u.deg,
                            lon=loc_lon * u.deg,
                            height=loc_height * u.m)
    
    obsgeoloc, obsgeovel = location.get_gcrs_posvel(time)
    loc_gcrs = GCRS(obstime=time, obsgeoloc=obsgeoloc, obsgeovel=obsgeovel)

    az_frame = AltAz(obstime=time, location=location)
    # zenith = AltAz(az=0 * u.deg, alt=90 * u.deg, obstime=time, location=location)

    # the celestial body
    sun = get_body('sun', time, location)
    moon = get_moon(time, location)

    fig = plt.figure(figsize=(8,8), dpi=100)
    ax = fig.add_subplot(111, projection='polar')
    ax.set_rscale('stereographiczenith')
    ax.xaxis.grid(False)
    ax.yaxis.grid(False)
    ax.set_yticks([])
    ax.set_ylim(0,np.pi/2)
    ax.set_theta_zero_location("N")
    ax.set_xticks([0, np.pi/2,np.pi,np.pi/2*3], ('N', 'E', 'S', 'W'))
    ax.get_xticklabels()[0].set_color(red)

    # zenith
    # the marker '+' looks ugly in polar projection
    # ax.plot(0,0, marker='+')
    ax.plot([0,np.pi],[0.04,0.04], c=dark_yellow, lw=0.5,zorder=0)
    ax.plot([np.pi/2,np.pi/2*3],[0.04,0.04], c=dark_yellow, lw=0.5,zorder=0)

    # equator
    eq_lon=np.arange(0,361,1)
    eq_lat = np.zeros_like(eq_lon)
    eq = SkyCoord(eq_lon,eq_lat,unit=u.deg,frame=loc_gcrs).transform_to(az_frame)
    eq = np.array([eq.az.value, 90 - eq.alt.value])/180 * np.pi
    ax.plot(eq[0],eq[1],zorder=-1,c=light_blue,lw=plt.rcParams['axes.linewidth'])

    # moon
    moon_logo.draw_moon_logo(ax, az_frame, moon, sun, loc_gcrs,zoom_factor=10, resolution=40, light_color=0.9)

    # Bright star
    star.draw_star(ax,az_frame)

    plt.tight_layout()
    if show is True:
        plt.show()
    
    return fig

if __name__ == '__main__':
    fig = skychart(show= True)
    save_path = './test/test.png'
    # fig.savefig(save_path,dpi=300)
    print("--- %s seconds ---" % (pytime.time() - start_time))
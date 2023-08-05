
# Healpix to WCS

You can extract a WCS image from a HEALPix with `healpix2wcs`.

There are, for convenience, two ways of providing the desired WCS coordinates :
- with a WCS FITS header.
- as parameters directly.


## Using a WCS FITS header

Say you already have a FITS file with a WCS header, named `my_wcs.fits`,
and you want to extract data from `my_heapix.fits` in the sky section described
by your WCS FITS file, and put it in `my_new_wcs.fits` :


``` python
from drizzlib import healpix2wcs

healpix2wcs(
    'my_healpix.fits',
    header='my_wcs.fits',
    output='my_new_wcs.fits'
)
```


## Using parameters


``` python
from drizzlib import healpix2wcs

healpix2wcs(
    'my_healpix.fits',
    pixel_size=.5,
    image_size=[20, 20],
    ctype=['GLON-TAN', 'GLAT-TAN'],
    output='my_new_wcs.fits'
)
```


## Additional parameters

There are more parameters available, see the docstring of `healpix2wcs`.
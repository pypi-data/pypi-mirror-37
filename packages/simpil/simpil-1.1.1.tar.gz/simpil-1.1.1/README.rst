simPIL
======

Please see https://simpil.readthedocs.io/ for more documentation and examples.

Provides an easy to use class for creating reading/fetching images files, adding
text and saving/retrieving image data.

It abstracts away some boiler plate for PIL/Pillow for a few things I want to do:

* Read image from file
* Write image to file
* Load image from string
* Load image from file object (StringIO)
* Load image from url
* Add text, shadowed text and outline text
* Autosave changes
* Get raw image data from object without saving.
# dozy 

Simple and user-friendly tools for operating images or videos.

Show errors explicitly and useful informations provied for users.

# Examples
```bash
# Operate images 
>>> from dozy import image
>>> dog = image.load('imgs/dog.jpg')
>>> type(dog)
<class 'numpy.ndarray'>
>>> dog.shape
(340, 510, 3)
>>> image.show(dog)
>>> sub_dog = image.crop(dog, x0=0, y0=0, x1=150, y1=150)
>>> image.save('imgs/sub_dog.jpg', sub_dog)
True
>>> cat = image.load('imgs/cat.jpg')
>>> cat = image.resize(cat, dog.shape[0], dog.shape[1])
>>> comb_vertical = image.combine(dog, cat, axis=0)
>>> comb_horizon = image.combine(dog, cat, axis=1)
```

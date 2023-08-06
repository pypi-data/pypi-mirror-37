# dozy 

Simple and user-friendly tools for operating images or videos.

Show errors explicitly and useful informations provied for users.

# Examples
```bash
# Operate images 
>>> from dozy import image  # import image module from dozy
>>> dog = image.load('imgs/dog.jpg')  # load an image from disk
>>> type(dog)  # dog is a numpy array
<class 'numpy.ndarray'>
>>> dog.shape  # you can use any method of numpy.array to operate it
(340, 510, 3)
>>> image.show(dog)  # an graphic window when be opened to show the image
>>> sub_dog = image.crop(dog, x0=0, y0=0, x1=150, y1=150) # crop an image
>>> image.save('imgs/sub_dog.jpg', sub_dog)  # save an image to disk
True
>>> cat = image.load('imgs/cat.jpg')  # load another image from disk
>>> cat = image.resize(cat, dog.shape[0], dog.shape[1])  # resize an image
>>> comb_vertical = image.combine(dog, cat, axis=0)  # combine two images vertically
>>> comb_horizon = image.combine(dog, cat, axis=1)  # combine two images horizon

# operate videos
>>> video.record('videos/capture.mp4')  # record a video using camera and save it
OpenCV: FFMPEG: tag 0x5634504d/'MP4V' is not supported with codec id 12 and format 'mp4 / MP4 (MPEG-4 Part 14)'
OpenCV: FFMPEG: fallback to use tag 0x7634706d/'mp4v'
>>> video.play('videos/capture.mp4')  # play just recorded video to see all is fine
>>> video.extract('videos/capture.mp4', 'frms/capture')  # extract frames from a video
dir frms/capture didn\'t exist, created here for you
All frames have been saved.
>>> video.merge('frms/capture', 'videos/merged_capture.mp4')  # create a video using a sequence of images in a dir
Using fps 25 and size 480x640 to save video
All images have been written to the video.
```

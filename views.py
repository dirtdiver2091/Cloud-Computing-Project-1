import config
import os
import uuid

from s3_operations import list_content, upload
from flask import Flask, request, render_template, redirect
from PIL import Image, ImageOps, ImageFilter

views = Flask(__name__)

def applyFilter(filename, filter):

    # Retrieve image here
    image = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Images' + filename

    i = image.split('.')
    changedImageName = i[0] + '-changed.jpg'

    # The edited image
    changedImage = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Changed Images' + changedImageName

    # Save image here
    im = Image.open(image)

    if filter == 'gray':
        im = ImageOps.grayscale(image)
    elif filter == 'blur':
        im = ImageOps.filter(ImageFilter.BLUR)
    elif filter == 'solar':
        im = ImageOps.solarize(image, threshold=80)

    im.save(changedImage)

    return changedImageName

if __name__ == "__main__":
	views.run(debug=True)
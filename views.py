from PIL import Image, ImageOps, ImageFilter

def applyFilter(filename, filter):

    image = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Images' + filename

    i = image.split('.')
    changedImageName = i[0] + '-changed.jpg'

    changedImage = 'C:\Users\Andrew Pidhajny\Temple Classes\Senior Year\Spring Semester\Cloud Computing\Project 1\Code\Cloud-Computing-Project-1\Changed Images' + changedImageName

    if filter == 'gray':
        im = ImageOps.grayscale(image)
    elif filter == 'blur':
        im = ImageOps.filter(ImageFilter.BLUR)
    elif filter == 'solar':
        im = ImageOps.solarize(image, threshold=80)

    im.save(changedImage)

    return changedImageName

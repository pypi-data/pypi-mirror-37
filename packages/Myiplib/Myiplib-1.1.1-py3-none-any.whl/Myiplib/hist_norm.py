import numpy as np
from skimage.io import ImageCollection, imread
from skimage.transform import resize

def imread_resize(img, size=(1024, 1024)):
    """

    :param img: Imput Image
    :param size: Tuple size to resize
    :return: First three channels and resized image
    """
    img = imread(img)
    img = resize(img, size)
    img = img[..., :3]  # drop transparent layer
    return img

def generate_RGB(Hyper_img, processing='wb'):
    response_mat = np.load('/home/data/Projects/pix2pix/data/raw/response_CANNON.npy')
    Hyper_img = Hyper_img[...,:31]
    RGB = np.dot(Hyper_img, response_mat)
    if processing=='wb':
        # # white every channel
        for i in range(response_mat.shape[1]):
            # RGB[...,i] = RGB[...,i]/np.mean(RGB[...,i])*0.5
            RGB[..., i] = RGB[..., i] / np.sum(response_mat, axis=0)[i]
    if processing=='minmax':
        RGB = (RGB - RGB.min()) / (RGB.max() - RGB.min())
    if processing=='hist_eq':
        RGB = normalize_hist(RGB)

    return RGB

def normalize_hist(img,process=True):
    # histogram normalization
    assert img.dtype in ['float64' , 'float32']
    if process:
        img_m = np.mean(img,axis=-1)
        img_ms = np.sort(img_m.flatten())
        n_pxs = len(img_ms)
        lb = img_ms[int(np.ceil(n_pxs*0.05))]
        ub = img_ms[int(np.floor(n_pxs*0.95))]
        img_p = (img-lb)/(ub-lb) * 150/255.
        img_p = np.clip(img_p,0,1)
    else:
        raise RuntimeError
    # img_p = img_p.astype('uint8')

    return img_p

def gray_world(img):
    for i in range(img.shape[-1]):
        img[...,i] = img[...,i]/np.mean(img[...,i])*0.5

        img = np.clip(img,0,1)
    return img

def illumination_norm(img):
    return (img-img.min())/(img.max()-img.min())
    # return np.clip(img/img.mean(),0,1)

def crop_imgs(img):
    return img
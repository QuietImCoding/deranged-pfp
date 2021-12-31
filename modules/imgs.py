import random
from wand.image import Image
from urllib.request import urlopen

def get_pfp(api_context, user):
    uobj = api_context.get_user(screen_name = user)
    uimg = uobj.profile_image_url_https.replace('_normal', '')
    response = urlopen(uimg)
    return Image(file=response)

def open_image(fname):
    return Image(filename=fname)

def overlay_pfp(api, user, img):
    overpfp = get_pfp(api, user)
    overpfp.resize(img.width, img.height)
    methods = [
        'bumpmap','darken','darken_intensity','difference','divide_dst',
        'hard_light','luminize', 'modulus_add', 'modulus_subtract', 'pegtop_light', 'pin_light'
    ]
    method = random.choice(methods)
    print(f"Overlaying with method {method}")
    img.composite_channel('all_channels', overpfp, method, 0, 0)
    img.save(filename='test.png')
    return(img)

def crop_img(img, unhinged_rating, center):
    print(f"Processing with unhinged:{unhinged_rating}, center:{center}")
    scale = int(min([img.width-center[0],
                     img.height-center[1],
                     center[0], center[1]]) - (unhinged_rating * 100))
    print(f"Cropping to: left:{center[0] - scale}, top:{center[1] - scale}, right:{center[0] + scale}, bottom:{center[1] + scale}")
    img.crop(left=center[0] - scale,
             top=center[1] - scale,
             right=center[0] + scale,
             bottom=center[1] + scale)
    
    saturation = 100.0 + (500 * unhinged_rating)
    print(saturation)
    img.modulate(saturation=saturation)
    return(img)



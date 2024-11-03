import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SolidFillColorMask

# Function to add rounded corners to the logo
def add_corners(im, rad):
    """Add rounded corners to an image."""
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def style_inner_eyes(img):
    img_size = img.size[0]
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((60, 60, 90, 90), fill=255)  # top left eye
    draw.rectangle((img_size - 90, 60, img_size - 60, 90), fill=255)  # top right eye
    draw.rectangle((60, img_size - 90, 90, img_size - 60), fill=255)  # bottom left eye
    return mask

def style_outer_eyes(img):
    img_size = img.size[0]
    mask = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255)  # top left eye
    draw.rectangle((img_size - 110, 40, img_size - 40, 110), fill=255)  # top right eye
    draw.rectangle((40, img_size - 110, 110, img_size - 40), fill=255)  # bottom left eye
    draw.rectangle((60, 60, 90, 90), fill=0)  # top left eye
    draw.rectangle((img_size - 90, 60, img_size - 60, 90), fill=0)  # top right eye
    draw.rectangle((60, img_size - 90, 90, img_size - 60), fill=0)  # bottom left eye
    return mask  

# Load and prepare the logo
logo_path = 'logo.png'  # Path to your logo
logo = Image.open(logo_path).convert("RGBA")  # Ensure logo is in RGBA mode
rounded_logo = add_corners(logo, 100)  # Apply rounded corners to the logo

# Save the rounded logo as a separate image to use in the QR code
rounded_logo_path = 'rounded_logo.png'
rounded_logo.save(rounded_logo_path)

# Create QR code with the rounded logo
qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)
qr.add_data('https://www.instagram.com/princess_andjela_tortice/')  # Update with your URL

# Create the inner and outer eye images with colors
qr_inner_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                  eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                                  color_mask=SolidFillColorMask(front_color=(24, 21, 31))).convert("RGBA")

qr_outer_eyes_img = qr.make_image(image_factory=StyledPilImage,
                                  eye_drawer=RoundedModuleDrawer(radius_ratio=1),
                                  color_mask=SolidFillColorMask(front_color=(208, 23, 183))).convert("RGBA")      

# Generate the main QR code image with rounded logo as color mask
qr_img = qr.make_image(
    image_factory=StyledPilImage,
    module_drawer=GappedSquareModuleDrawer(),
    color_mask=ImageColorMask(color_mask_path=rounded_logo_path),
    embeded_image_path=rounded_logo_path  # Embed the rounded logo
).convert("RGBA")

# Create masks for inner and outer eyes
inner_eye_mask = style_inner_eyes(qr_img).convert("L")
outer_eye_mask = style_outer_eyes(qr_img).convert("L")

# Composite the images together with the masks
intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)

# Save the final QR code image
final_image.save("final_qr_code.png")
print("QR code with rounded logo and custom eyes generated and saved!")

import qrcode
from PIL import Image, ImageDraw
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import GappedSquareModuleDrawer
from qrcode.image.styles.colormasks import ImageColorMask

# Function to add rounded corners to the logo
def add_corners(im, rad):
    """Add rounded corners to an image."""
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

# Load and prepare the logo
logo_path = 'logo.png'  # Update this to your logo path
logo = Image.open(logo_path)
logo = add_corners(logo, 100)  # Add rounded corners to the logo

# Create QR code
qr = qrcode.QRCode(
    version=4,
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

qr.add_data('https://andjelaljubenkovic.rs/')  # Update this with your desired data

# Generate the QR code with your logo
qr_img = qr.make_image(image_factory=StyledPilImage,
                       module_drawer=GappedSquareModuleDrawer(),
                       color_mask=ImageColorMask(color_mask_path=logo_path),
                        embeded_image_path=logo_path)  # Embed rounded logo directly

# Save the final QR code image
qr_img.save("qr.png")
print("QR code generated and saved!")

import qrcode
from PIL import Image
import os
import warnings

# For ignoring warnings
warnings.filterwarnings("ignore")

####################################
# Enter your text or URL
YOUR_TEXT_OR_URL = 'https://andjelaljubenkovic.rs/'  # Your website link
####################################
# Set size of the logo
logosize = 75
####################################

# Set path to your file from command line arguments
import sys
infile = sys.argv[-1]  # This will take the image path from command line arguments
####################################

# Convert RGB to HEX function
def rgb_to_hex(rgb):
    return '#' + '%02x%02x%02x' % rgb

# Get filename
filename = infile.split('.')[0]

# Read image
logo = Image.open(infile)

# Convert to RGBA to maintain transparency
logo_rgb = logo.convert("RGBA") 

# Calculate the average color of the logo
data = logo_rgb.getdata()
r = g = b = a = 0
num_pixels = len(data)

for pixel in data:
    r += pixel[0]
    g += pixel[1]
    b += pixel[2]
    a += pixel[3]

# Average the color values
r //= num_pixels
g //= num_pixels
b //= num_pixels

# If the logo has significant transparency, you might want to adjust how the color is derived
if a < 255 * 0.5:  # If more than 50% of the pixels are transparent, use a fallback color
    r, g, b = 0, 0, 0  # Fallback color (black) if the logo is mostly transparent

# Set size of the logo
basewidth = logosize
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)  # Use LANCZOS for resizing

# Create QR code with high error correction
qr_big = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
qr_big.add_data(YOUR_TEXT_OR_URL)
qr_big.make()

# Using the average color of the image for the QR code
colorcode = rgb_to_hex((r, g, b))
img_qr_big = qr_big.make_image(fill_color=colorcode, back_color="white").convert('RGB')

# Position the logo in the center of the QR code
pos = (
    (img_qr_big.size[0] - logo.size[0]) // 2,
    (img_qr_big.size[1] - logo.size[1]) // 2
)
img_qr_big.paste(logo, pos)

# Create final_QR directory
try:
    os.mkdir("final_QR")
except FileExistsError:
    print("Folder already exists")

# Save as filenameQR.png format    
img_qr_big.save(f"final_QR/{filename}QR.png")

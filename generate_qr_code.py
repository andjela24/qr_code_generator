import qrcode
from PIL import Image, ImageDraw, ImageFont

# Function to create a QR code with a logo
def create_qr_with_logo(data, logo_path, output_path, text=None, logo_size_ratio=0.25):
    # Step 1: Generate the QR code
    qr = qrcode.QRCode(
        version=1,  # Version can be adjusted
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Width of the border (in boxes)
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Create the QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Step 2: Open the logo image
    logo = Image.open(logo_path).convert("RGBA")

    # Resize the logo
    logo_size = int(qr_img.size[0] * logo_size_ratio)  # Calculate size based on QR code size
    logo = logo.resize((logo_size, logo_size))  # Removed Image.ANTIALIAS

    # Step 3: Calculate the position to overlay the logo
    logo_position = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)

    # Step 4: Overlay the logo onto the QR code
    qr_img.paste(logo, logo_position, logo)

    # Step 5: Optionally, add text below the QR code
    if text:
        qr_img = qr_img.convert("RGB")  # Convert to RGB for text overlay
        draw = ImageDraw.Draw(qr_img)

        # Define the font and text position
        try:
            font_path = "path/to/your/custom_font.ttf"  # Specify your custom font file path
            font = ImageFont.truetype(font_path, 24)
        except IOError:
            font = ImageFont.load_default()  # Fallback to default font if custom font isn't found

        # Measure text size and position
        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((qr_img.size[0] - text_width) // 2, qr_img.size[1] - text_height - 10)

        # Add text onto the image
        draw.text(text_position, text, font=font, fill="black")

    # Step 6: Save the final QR code image
    qr_img.save(output_path)
    print(f"QR code saved as {output_path}")

# Usage
data = "https://andjelaljubenkovic.rs/"  # Your data
logo_path = "background_logo.png"  # Path to your logo image
output_path = "custom_qr_code.png"  # Output path for the QR code
text = "Scan me for more info"  # Optional text below the QR code

create_qr_with_logo(data, logo_path, output_path, text)

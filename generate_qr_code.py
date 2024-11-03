import qrcode  # Import the qrcode library

# Step 1: Define the data for the QR code
data = "https://andjelaljubenkovic.rs/"  # Replace with your actual URL or file link

# Step 2: Create a QRCode object with desired configurations
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR code (1 is the smallest, goes up to 40)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
    box_size=10,  # Size of each box in the QR code grid
    border=4,  # Width of the border (in boxes)
)

# Step 3: Add data to the QR code
qr.add_data(data)
qr.make(fit=True)  # Optimize the QR code size based on data

# Step 4: Create an image of the QR code
img = qr.make_image(fill_color="black", back_color="white")

# Step 5: Save the QR code as an image file
img.save("cv_qr_code.png")  # Saves the QR code as a PNG file

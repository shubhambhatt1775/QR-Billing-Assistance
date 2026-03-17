import qrcode

# Your UPI ID
upi_id = "palakkela@okaxis"
name = "Palak Kela"
amount = "100"

# UPI payment link
upi_link = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR"

# Generate QR
qr = qrcode.make(upi_link)

# Save QR image
qr.save("C:/prog/project/project/qr/qrcus/static/images/QrCode.png")

print("QR Code Generated Successfully")
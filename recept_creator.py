from cryptography.fernet import Fernet
from fpdf import FPDF
from PIL import Image
import qrcode
import os
from datetime import datetime

class SecureReceiptPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        pass

# Settings
start_serial = 12
total_receipts = 500
receipts_per_page = 4
box_width = 95
box_height = 140
left_margin = 10
top_margin = 10

# Encryption settings
ENCRYPTION_KEY = b"NWRmMTk3ZWUwY2RjNjA3NWY4NzQ2NmQyOGRkYzczMmM="  # Securely generated key
fernet = Fernet(ENCRYPTION_KEY)

# Generate serial numbers
receipts = list(range(start_serial, start_serial + total_receipts))

# Setup PDF
pdf = SecureReceiptPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=False)
pdf.set_margins(left=left_margin, top=top_margin, right=10)
pdf.set_font("Arial", size=10)

# Create folder for temporary QR codes
os.makedirs("temp_qr", exist_ok=True)

for idx, serial in enumerate(receipts):
    if idx % receipts_per_page == 0:
        pdf.add_page()

    # Calculate quadrant position
    col = (idx % 4) % 2
    row = (idx % 4) // 2
    x_position = left_margin + col * (box_width + 5)
    y_position = top_margin + row * (box_height + 5)

    # Receipt box with bold border
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.rect(x_position, y_position, box_width, box_height)

    # Watermark with lighter gray and centered
    pdf.set_text_color(200, 200, 200)
    pdf.set_font("Arial", "B", 20)
    pdf.set_xy(x_position + 5, y_position + box_height / 2 - 5)
    pdf.cell(box_width, 10, "* ORIGINAL COPY *", ln=1, align="C")

    # Header with larger bold red font and centered
    pdf.set_text_color(200, 0, 0)
    pdf.set_font("Arial", 'B', 13)
    pdf.set_xy(x_position, y_position + 5)
    pdf.cell(box_width, 8, "TRUCK FILLING LOAD RECEIPT", ln=1, align='C')

    pdf.set_font("Arial", size=10)
    pdf.set_xy(x_position + 2, y_position + 18)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"Receipt No: {serial}", ln=1)

    # Receipt fields with blue labels
    fields = [
        "Driver Name        : _____________________________",
        "Truck Number       : _____________________________",
        "Date               : __________    Time: ___________",
        "",
        "Received By (Driver)     : _______________________",
        "Approved By (Authorized) : _______________________",
        "",
        "Note: Submit this receipt to accounts to claim payment."
    ]

    line_y = y_position + 24
    for line in fields[:-1]:
        pdf.set_xy(x_position + 4, line_y)
        pdf.set_text_color(0, 0, 150)
        pdf.cell(0, 6, line, ln=1)
        line_y += 6

    # Final note in italic
    pdf.set_xy(x_position + 4, line_y)
    pdf.set_text_color(0, 0, 150)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 6, fields[-1], ln=1)

    # QR code (encrypted serial and timestamp)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{serial}|{timestamp}"
    encrypted = fernet.encrypt(message.encode()).decode()
    qr_data = encrypted
    qr_code = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr_code.add_data(qr_data)
    qr_code.make(fit=True)
    qr_img = qr_code.make_image(fill_color="black", back_color="white")
    qr_path = f"temp_qr/qr_{serial}.png"
    qr_img.save(qr_path)
    pdf.image(qr_path, x=x_position + box_width - 25, y=y_position + box_height - 25, w=25, h=25)

# Clean up
for file in os.listdir("temp_qr"):
    os.remove(os.path.join("temp_qr", file))
os.rmdir("temp_qr")

# Save output
pdf.output("Secure_Truck_Filling_Load_Receipts.pdf")
print("Receipts generated successfully!")
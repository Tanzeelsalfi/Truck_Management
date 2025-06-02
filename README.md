
## Setup and Installation

1.  **Clone the Repository (or create files):**
    Ensure you have `app.py`, `recept_creator.py`, and the `templates` and `static` directories with their respective HTML files.

2.  **Create a Python Virtual Environment (Highly Recommended):**
    Open your terminal in the `your_project_folder`:
    ```bash
    python3 -m venv myenv
    ```
    Activate the environment:
    *   macOS/Linux: `source myenv/bin/activate`
    *   Windows: `myenv\Scripts\activate`

3.  **Install Dependencies:**
    With the virtual environment activated, install all required Python packages:
    ```bash
    pip install Flask cryptography openpyxl qrcode Pillow fpdf2
    ```
    *   `Flask`: Web framework for `app.py`.
    *   `cryptography`: For Fernet encryption (used by both scripts).
    *   `openpyxl`: For Excel export in `app.py`.
    *   `qrcode`: For generating QR code images in `recept_creator.py`.
    *   `Pillow`: Image processing library (a dependency for `qrcode`).
    *   `fpdf2`: For PDF generation in `recept_creator.py`.

4.  **Create `static` folder and add `favicon.ico`:**
    Inside `your_project_folder`, create a folder named `static`. Place your `favicon.ico` image file inside this `static` folder.

5.  **CRITICAL: Configure Encryption Key:**
    *   The `ENCRYPTION_KEY` variable in **both** `app.py` and `recept_creator.py` **MUST BE IDENTICAL**.
    *   The provided key `b"ZbQhX1XImwRiBxn4-mnh1U1RJH5AzzTX0L2ndQnGpgo="` is for demonstration only.
    *   **Generate your own unique Fernet key ONCE:**
        1.  Open a Python interpreter (e.g., type `python3` in your terminal).
        2.  Run the following commands:
            ```python
            from cryptography.fernet import Fernet
            key = Fernet.generate_key()
            print(key.decode()) # This will print your new key string
            ```
        3.  Copy the outputted key string (it will look like a random sequence of characters).
        4.  Open `app.py` and `recept_creator.py`.
        5.  Replace the line `ENCRYPTION_KEY = b"ZbQhX1XImwRiBxn4-mnh1U1RJH5AzzTX0L2ndQnGpgo="` in **both files** with your new key, ensuring it's a byte string (prefixed with `b`):
            ```python
            ENCRYPTION_KEY = b"YOUR_NEW_UNIQUE_KEY_HERE"
            ```
    *   **Keep this key secure and backed up!** If you change or lose this key:
        *   QR codes generated with an old key will not be verifiable by the app using a new key.
        *   The app using an old key cannot verify QR codes generated with a new key.

6.  **Review Flask App Secret Key:**
    *   In `app.py`, change the value of `app.secret_key` to a different strong, unique random string. This is important for Flask's session security (used for flash messages). Example: `app.secret_key = os.urandom(24)` (though for consistency across restarts, a hardcoded random string is fine for this app).

## Usage

### 1. Generating Encrypted PDF Receipts (using `recept_creator.py`)

1.  **Activate your virtual environment** (if not already active).
2.  **Navigate to your project directory** in the terminal.
3.  **Customize Settings (Optional):** Open `recept_creator.py` and modify variables like `start_serial`, `total_receipts`, `receipts_per_page`, etc., if needed. Ensure `ENCRYPTION_KEY` matches `app.py`.
4.  **Run the script:**
    ```bash
    python recept_creator.py
    ```
5.  This will generate a file named `Secure_Truck_Filling_Load_Receipts.pdf` in your project folder. This PDF contains the printable receipts with encrypted QR codes. Print these receipts for use.

### 2. Running the Flask Web Application (`app.py`)

1.  **Activate your virtual environment.**
2.  **Navigate to the project directory.**
3.  **Run the Flask application:**
    ```bash
    python app.py
    ```
4.  The terminal will show the local URL, typically `http://127.0.0.1:5001`.
5.  **Accessing the App:**
    *   **Desktop:** Open a web browser to `http://127.0.0.1:5001`.
    *   **Mobile (for camera scanning):**
        *   **Recommended Method (using ngrok):**
            1.  Keep the Flask app (`app.py`) running.
            2.  Open a **new, separate terminal window/tab**.
            3.  If you have `ngrok` installed (download from ngrok.com), run: `ngrok http 5001`
            4.  `ngrok` will display a public `https://<random-string>.ngrok.io` URL.
            5.  Open this HTTPS URL on your mobile device's browser. The camera should now work reliably.
        *   **Alternative (Android USB Port Forwarding):** (See previous detailed instructions if needed).

### 3. Using the Web Application Features

*   **Main Scanner Page (`/` or the ngrok URL):**
    *   **Scan QR:** Point your device camera at a QR code from a generated receipt. The data will fill the textarea, and the form will auto-submit.
    *   **Truck Number:** Before the auto-submit (or for the next scan after a modal closes), select a truck from the dropdown or choose "Other" to enter a custom one. This selection will be "sticky" for subsequent scans on that browser session until changed or the modal for a *new different type* of result is shown.
    *   **Results:** A modal pop-up shows success (✅) or error (❌) messages. Close the modal to clear the QR field and prepare for the next scan.
*   **History Page (`/history`):**
    *   View all verified scans: Serial, QR Timestamp, System Timestamp, Truck No.
    *   Select and delete individual scans (with confirmation).
*   **Manage Trucks Page (`/trucks`):**
    *   Add new truck numbers to the master list that populates the dropdown on the scanner page.
    *   Delete truck numbers from the master list (with confirmation).
*   **Export Report Page (`/export`):**
    *   Enter a "Price Per Load" for value calculations.
    *   Download a styled Excel file (`receipt_scan_report_styled.xlsx`) with three sheets:
        1.  Detailed list of all scans with individual load values and truck subtotals.
        2.  Summary by truck (total receipts and total value per truck).
        3.  Overall summary.
*   **Delete All Scans (Navigation Bar):**
    *   Accessible from any page.
    *   Prompts for confirmation before **permanently deleting all scan records** (does not affect the truck master list).

## QR Code Data Format

The `recept_creator.py` encrypts data in the following plain text format before encryption:

`SERIAL_NUMBER|YYYY-MM-DD HH:MM:SS`

Example: `SN00012|2023-10-27 15:45:00`

The `app.py` application decrypts this data. Both scripts must use the identical `ENCRYPTION_KEY`.

## Troubleshooting

*   **"pyngrok library not found" (If you were to re-add `pyngrok` to `app.py`):** Ensure `pyngrok` is installed in the *active virtual environment* (`pip install pyngrok`).
*   **Camera Not Working on Mobile:** This is almost always due to not accessing the site over a secure context (HTTPS). Use `ngrok` as described above. Also, check browser permissions for camera access for the specific `ngrok.io` site.
*   **Database File (`receipt_scans.db`):** If you make changes to table structures in `init_db()` (e.g., adding/removing columns), it's safest to delete the existing `receipt_scans.db` file in your project directory. The `init_db()` function will then recreate it with the new schema when `app.py` starts. *Warning: This deletes all existing scan and truck master list data.*
*   **Encryption Key Mismatch:** If QR codes scan but the Flask app shows "Invalid/Tampered data" or "Malformed decrypted data", the `ENCRYPTION_KEY` in `app.py` does not match the one used in `recept_creator.py` when those QR codes were generated. Ensure they are identical.
*   **Excel Export Issues:** Ensure `openpyxl` is installed correctly. Check the Flask terminal for any errors during the Excel generation process if the download fails or the file is corrupted.
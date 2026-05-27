import os
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from parser import (
    read_pdf_data,
    parse_label,
    send_to_api
)

# ================= CONFIG =================

INPUT_FOLDER = "input"
PROCESSED_FOLDER = "processed"
FAILED_FOLDER = "failed"

# ================= HANDLER =================

class PDFHandler(FileSystemEventHandler):

    def process_pdf(self, pdf_path):

        try:

            print(f"\n[INFO] New PDF detected: {pdf_path}")

            # wait until file copy finishes
            time.sleep(2)

            # read PDF
            items, raw_text = read_pdf_data(pdf_path)

            # parse data
            parsed_data = parse_label(
                items,
                raw_text
            )

            print("\n====== EXTRACTED DATA ======")

            for k, v in parsed_data.items():
                print(f"{k:20}: {v}")

            # send to API
            response = send_to_api(parsed_data)

            if response and response.status_code == 200:

                move_file(
                    pdf_path,
                    PROCESSED_FOLDER
                )

                print("\n[SUCCESS] PDF processed successfully.")

            else:

                move_file(
                    pdf_path,
                    FAILED_FOLDER
                )

                print("\n[ERROR] API request failed.")

        except Exception as e:

            print(f"\n[ERROR] {e}")

            move_file(
                pdf_path,
                FAILED_FOLDER
            )

    # triggered when new file appears
    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".pdf"):
            return

        self.process_pdf(event.src_path)

# ================= UTILITIES =================

def move_file(src_path, destination_folder):

    filename = os.path.basename(src_path)

    dest_path = os.path.join(
        destination_folder,
        filename
    )

    shutil.move(src_path, dest_path)

    print(f"[INFO] Moved file to: {dest_path}")

# ================= START WATCHER =================

def process_existing_files(handler):

    for filename in os.listdir(INPUT_FOLDER):

        if filename.lower().endswith(".pdf"):

            full_path = os.path.join(
                INPUT_FOLDER,
                filename
            )

            handler.process_pdf(full_path)

# ================= MAIN =================

if __name__ == "__main__":

    # create folders
    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)
    os.makedirs(FAILED_FOLDER, exist_ok=True)

    event_handler = PDFHandler()

    # process old files first
    process_existing_files(event_handler)

    observer = Observer()

    observer.schedule(
        event_handler,
        INPUT_FOLDER,
        recursive=False
    )

    observer.start()

    print(f"\n[WATCHER] Monitoring folder: {INPUT_FOLDER}")

    try:

        while True:
            time.sleep(1)

    except KeyboardInterrupt:

        print("\n[WATCHER] Stopping watcher...")

        observer.stop()

    observer.join()
import os
import time
import shutil

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from parser import read_pdf_data, parse_label, send_to_api

INPUT_FOLDER = "input"
PROCESSED_FOLDER = "processed"

class PDFHandler(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        if not event.src_path.lower().endswith(".pdf"):
            return

        try:
            print(f"\n[INFO] Phát hiện PDF mới: {event.src_path}")

            # đợi file copy xong
            time.sleep(2)

            items, raw_text = read_pdf_data(event.src_path)

            parsed_data = parse_label(items, raw_text)

            print("\n====== KẾT QUẢ ======")

            for k, v in parsed_data.items():
                print(f"{k:20}: {v}")

            send_to_api(parsed_data)

            # move file
            filename = os.path.basename(event.src_path)

            dest_path = os.path.join(
                PROCESSED_FOLDER,
                filename
            )

            shutil.move(event.src_path, dest_path)

            print(f"\n[INFO] Đã chuyển sang processed/{filename}")

        except Exception as e:
            print("\n[LỖI]", e)

if __name__ == "__main__":

    os.makedirs(INPUT_FOLDER, exist_ok=True)
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    event_handler = PDFHandler()

    for filename in os.listdir(INPUT_FOLDER):
        if filename.lower().endswith(".pdf"):
            event_handler.on_created(
                type('Event', (object,), {'src_path': os.path.join(INPUT_FOLDER, filename), 'is_directory': False})
            )

    observer = Observer()

    observer.schedule(
        event_handler,
        INPUT_FOLDER,
        recursive=False
    )

    observer.start()

    print(f"[WATCHER] Đang theo dõi folder: {INPUT_FOLDER}")

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        observer.stop()

    observer.join()
import os
import zipfile
import shutil
import argparse

def process_empty_folders(root_path, delete_only=False, zip_only=False):
    zip_output = os.path.join(root_path, "empty_folders.zip")
    zipf = None

    if not delete_only:
        zipf = zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED)

    for item in os.listdir(root_path):
        folder_path = os.path.join(root_path, item)
        # Chỉ xử lý folder cấp 1
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            print(f"Found empty folder: {folder_path}")

            if zipf:
                zipf.writestr(item + "/", "")
                print(f" → Added to zip")

            if not zip_only:
                shutil.rmtree(folder_path)
                print(f" → Deleted")

    if zipf:
        zipf.close()
        print(f"\n✅ Empty folders compressed into: {zip_output}")

def main():
    parser = argparse.ArgumentParser(description="Compress and/or delete empty folders (level 1 only).")
    parser.add_argument(
        "-i", "--input",
        type=str,
        default=r"E:\DDD",
        help="Root path to scan (default: E:\\DDD)"
    )
    parser.add_argument(
        "--delete-only",
        action="store_true",
        help="Delete empty folders only (no zip)."
    )
    parser.add_argument(
        "--zip-only",
        action="store_true",
        help="Zip empty folders only (do not delete)."
    )

    args = parser.parse_args()

    if args.delete_only and args.zip_only:
        print("❌ You cannot use --delete-only and --zip-only at the same time.")
        return

    root_path = args.input
    if not os.path.exists(root_path):
        print(f"❌ Path not found: {root_path}")
        return

    process_empty_folders(root_path, delete_only=args.delete_only, zip_only=args.zip_only)

if __name__ == "__main__":
    main()

import os
import subprocess
import re
import ctypes
import argparse

# --- Get script directory ---
def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

# --- Clipboard handling ---
CF_TEXT = 1

kernel32 = ctypes.windll.kernel32
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32 = ctypes.windll.user32
user32.GetClipboardData.restype = ctypes.c_void_p

def get_clipboard_text():
    user32.OpenClipboard(0)
    try:
        if user32.IsClipboardFormatAvailable(CF_TEXT):
            data = user32.GetClipboardData(CF_TEXT)
            data_locked = kernel32.GlobalLock(data)
            text = ctypes.c_char_p(data_locked)
            value = text.value
            kernel32.GlobalUnlock(data_locked)
            return value.decode('utf-8')  # Decode using UTF-8
    finally:
        user32.CloseClipboard()

# --- URL Validation ---
def is_valid_url(url):
    regex = r"^(https?://)?(www\.)?([a-zA-Z0-9]+(-?[a-zA-Z0-9])*\.)+[a-z]{2,}(:[0-9]+)?(/.*)?$"
    return bool(re.match(regex, url))

# --- Download using subprocess (similar to yt-dlp command) ---
def download_video(url, output_path, download_type):
    # Get the directory of the current script
    script_dir = get_script_directory()

    # Build the path to the yt-dlp.exe executable in the current directory
    yt_dlp_path = os.path.join(script_dir, 'yt-dlp.exe')

    # Start building the command
    command = [yt_dlp_path, '-o', output_path, url]

    # Choose command based on download type
    if download_type == 'audio':
        command.insert(1, '-x')  # Extract audio
        command.insert(2, '--audio-format')
        command.insert(3, 'mp3')
        command.insert(4, '--audio-quality')
        command.insert(5, '0')
        print("\n" + "=" * 20)
        print("DOWNLOADING AUDIO")
        print("Please be patient, this may take a while depending on the size of the audio.")
        print("WARNING: Ensure you have the rights to download and use this audio.")
        print("=" * 20 + "\n")
    else:  # Default to video if not specified or not 'audio'
        command.insert(1, '-S')
        command.insert(2, 'vcodec:h264')
        command.insert(3, '-f')
        command.insert(4, 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4')
        print("\n" + "=" * 20)
        print("DOWNLOADING VIDEO")
        print("Please be patient, this may take a while depending on the size of the video.")
        print("WARNING: Ensure you have the rights to download and use this video.")
        print("=" * 20 + "\n")

    # Print the command for debugging
    print('Running command:', ' '.join(command))

    # Run the command and handle any errors
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print('Error occurred while downloading:', e)
    finally:
        # Open the output directory in the file explorer
        os.startfile(os.path.dirname(output_path))

    # Print watermark
    print("\n" + "=" * 20)
    print("This tool was created by LightMind")
    print("=" * 20 + "\n")

        
# --- Get most recently changed project folder ---
def get_most_recently_changed_project_folder(root_dir, *extra_subfolders):
    most_recent_project = None
    max_file_mtime = 0

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_mtime = os.path.getmtime(file_path)

            if file_mtime > max_file_mtime:
                max_file_mtime = file_mtime
                most_recent_project = dirpath

    if most_recent_project:
        relative_path = os.path.relpath(most_recent_project, root_dir)
        project_name = relative_path.split(os.sep)[0]
        return os.path.join(root_dir, project_name, *extra_subfolders) 
    else:
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download video from clipboard URL to most recently changed project folder.")
    parser.add_argument("root_dir", help="The root directory to search within.")
    parser.add_argument("extra_subfolders", nargs="*", help="Optional extra subfolders to append.")
    parser.add_argument("--type", choices=['audio', 'video'], default='video', help="Type of download (audio or video).")
    args = parser.parse_args()

    changed_folder = get_most_recently_changed_project_folder(args.root_dir, *args.extra_subfolders)

    if changed_folder:
        # Get clipboard contents
        clipboard_text = get_clipboard_text()

        # Check if it's a valid URL
        if not clipboard_text:
            print("No URL found in clipboard. Please copy a valid URL and try again.")
        elif not is_valid_url(clipboard_text):
            print("Invalid URL found in clipboard. Please copy a valid URL and try again.")
        else:
            # Output path handling
            output_path = os.path.join(changed_folder, "%(title)s.%(ext)s")

            # Download the video
            download_video(clipboard_text, output_path, args.type)
    else:
        print("No files found within subdirectories.")
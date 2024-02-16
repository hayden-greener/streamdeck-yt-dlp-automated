# Streamdeck-YT-DLP Automated

Streamdeck-YT-DLP Automated is a Python command-line utility for downloading video or audio from a URL copied to the clipboard. It's designed to be compatible with devices like a Stream Deck for easy operation.

This script interacts with your system's clipboard. While it utilizes windll calls through ctypes for a generally secure approach, there's always a potential for compatibility issues with certain programs.

## Prerequisites

Ensure you have the following installed on your local machine:

- Python 3.5 or higher
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) command-line utility

## Installation

1. Clone this repository to your local machine.

## Usage

Execute the script from the command line using the following syntax:

```bash
python script_path/main.py <root_dir> <extra_subfolders> --type <download_type>
```

Where:

- `<root_dir>`: The root directory to search within.
- `<extra_subfolders>`: Optional extra subfolders to append.
- `<download_type>`: Type of download (audio or video). Default is 'video'.

For example:

```bash
python script_path/main.py "video_projects_dir" "footage_subfolder"
```

This command downloads a video from the clipboard URL to the most recently modified project in the footage subfolder.

```bash
python script_path/main.py "video_projects_dir" "audio_subfolder" --type audio
```

This command downloads an audio file from the clipboard URL to the most recently modified project in the audio subfolder.

```bash
python script_path/main.py "video_projects_dir" --type audio
```

This command downloads a audio file from the clipboard URL directly to the root directory specified by "video_projects_dir", ignoring any subfolders.


Replace `script_path`, `video_projects_dir`, `footage_subfolder`, and `audio_subfolder` with your actual paths and names.
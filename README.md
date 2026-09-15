# vidclip

A simple tool that **downloads a YouTube video**, or **saves just a clip** from it (for example from 1:20 to 2:05).

It tries to download in **1080p**. If that isn’t available, it uses **720p**.

You do **not** need to know programming. You install it once, then run a short command.

---

## Before you start (Windows)

You need **Python** on your computer. That’s a free program vidclip uses in the background.

1. Open [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Click the big yellow **Download** button
3. Run the installer
4. On the first screen, tick **Add python.exe to PATH**
5. Click **Install Now**
6. When it finishes, **close any Command Prompt or PowerShell windows** you already had open

If Python is already installed, you can skip this.

---

## Get the vidclip folder

If you downloaded this from GitHub:

1. On the GitHub page, click the green **Code** button
2. Click **Download ZIP**
3. Unzip the file (right-click → **Extract All**)
4. Open the unzipped folder. You should see `install.bat` inside it

If someone already sent you the folder, just open that folder.

---

## Install vidclip (once)

1. Double-click **`install.bat`**
2. If Windows asks “Do you want to allow this app…?”, click **Yes**
3. Wait until it says it is installed
4. **Close that window**
5. Open a **new** terminal:
   - Click Start
   - Type `PowerShell`
   - Open **Windows PowerShell**

Check that it worked:

```text
vidclip doctor
```

You should see lines for Python, ffmpeg, and js. If instead you see `'vidclip' is not recognized`, close PowerShell and open a brand-new window, then try `vidclip doctor` again.

---

## Download a video

### Easiest way

In PowerShell, type:

```text
vidclip
```

Then:

1. Paste the YouTube link and press Enter
2. For a **full video**, leave Start time and End time blank (just press Enter)
3. For a **clip**, type times like `1:20` and `2:05`
4. Leave “Save as” blank unless you want a specific file name

When it finishes, it prints **Saved:** and the file location.

### One-line way

Full video:

```text
vidclip "https://www.youtube.com/watch?v=VIDEO_ID"
```

Clip from 1 minute 20 seconds to 2 minutes 5 seconds:

```text
vidclip "https://www.youtube.com/watch?v=VIDEO_ID" --start 1:20 --end 2:05
```

Save with a name you choose, in a folder you choose:

```text
vidclip "https://www.youtube.com/watch?v=VIDEO_ID" --start 1:20 --end 2:05 -o my-clip.mp4 -d "C:\Users\YOURNAME\Videos"
```

Replace the link with your real YouTube URL. Keep the quotes around the link.

The file is saved in **the folder you are in** when you run the command, unless you use `-d` to pick another folder.

---

## If something goes wrong

| What you see | What to do |
|---|---|
| `'vidclip' is not recognized` | Close the terminal, open a **new** PowerShell window, try again. If it still fails, run `install.bat` again. |
| Python was not found during install | Reinstall Python and tick **Add python.exe to PATH**, then open a new window and run `install.bat` again. |
| “This video is not available” but you can watch it in the browser | In PowerShell run `vidclip update`, then try the download again. |
| First download is slow / mentions Deno | That’s normal the first time. vidclip is fetching a helper it needs for YouTube. |

---

## Mac or Linux

1. Install Python 3.10 or newer
2. Open Terminal in this folder
3. Run:

```bash
chmod +x install.sh
./install.sh
```

4. Open a new terminal, then run `vidclip doctor` and `vidclip`

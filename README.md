# vidclip

A simple tool that **downloads a YouTube video**, or **saves just a clip** from it (for example from 1:20 to 2:05).

You can choose **1080p**, **720p**, **480p**, or **360p**. If the size you pick isn’t available, it uses the next size down.

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

You should see lines for Python, ffmpeg, and js.

**If it says `vidclip` is not recognized:**

1. You must open a **brand-new** PowerShell window after `install.bat` (old windows do not pick up PATH).
2. Or run it from the vidclip folder (this works even without PATH):

```text
cd C:\Code\vid-clipper
.\vidclip.cmd doctor
```

Replace `C:\Code\vid-clipper` with the folder that contains `install.bat` if yours is different.

---

## Already installed? Update or reinstall

Do this when the folder has new files (for example a new quality option), or when you want to reinstall the tool.

**Windows**

1. Get the latest folder the same way as before (Download ZIP from GitHub, or use the updated folder someone sent you)
2. Open that folder
3. Double-click **`install.bat`** again (it is safe to run more than once)
4. Close that window
5. Open a **new** PowerShell window
6. Run:

```text
vidclip doctor
```

**Mac or Linux**

From the latest folder, run `./install.sh` again, then open a new terminal.

**If downloads start failing** (YouTube changed something, but you did not get a new vidclip folder):

In PowerShell or Terminal, run:

```text
vidclip update
```

That only refreshes the YouTube helper. It does **not** replace a full reinstall. If the tool itself has new features, run `install.bat` / `install.sh` as above.

---

## Download a video

### Easiest way

In PowerShell, first go to the vidclip folder if `vidclip` is not recognized:

```text
cd C:\Code\vid-clipper
.\vidclip.cmd
```

If `vidclip` works on its own after install, you can just type:

```text
vidclip
```

Then:

1. Paste the YouTube link and press Enter
2. For a **full video**, leave Start time and End time blank (just press Enter)
3. For a **clip**, type times like `1:20` and `2:05`
4. Choose quality: `1080`, `720`, `480`, or `360` (press Enter for 1080)
5. Leave “Save as” blank unless you want a specific file name

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

720p, 480p, or 360p (smaller file, faster download):

```text
vidclip "https://www.youtube.com/watch?v=VIDEO_ID" --quality 720
vidclip "https://www.youtube.com/watch?v=VIDEO_ID" -q 480
vidclip "https://www.youtube.com/watch?v=VIDEO_ID" -q 360
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
| `'vidclip' is not recognized` | Open a **new** PowerShell window after install. Or go to the vidclip folder and run `.\vidclip.cmd` instead of `vidclip`. |
| Python was not found during install | Reinstall Python and tick **Add python.exe to PATH**, then open a new window and run `install.bat` again. |
| “This video is not available” but you can watch it in the browser | In PowerShell run `vidclip update`, then try the download again. If that is not enough, run `install.bat` again from the latest folder. |
| New features are missing (for example 360p) | You have an old install. Run `install.bat` again from the latest folder. |
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

To update later, run `./install.sh` again from the latest folder.

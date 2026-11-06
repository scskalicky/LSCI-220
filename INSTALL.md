# LSCI 220: Getting set up

## Install (once only)

1. Download the course folder: **[LINK TO COURSE FOLDER]**

2. Unzip it. You should have a folder called `lsci220`.

3. Move the `lsci220` folder somewhere on your computer that you can easily find again. We suggest **not** putting it in a folder that syncs to OneDrive, iCloud, Dropbox or Google Drive, as syncing can cause problems with the course software.

4. Open a terminal inside the `lsci220` folder.
   - **Mac:** open **Terminal**, type `cd ` (with a space after it), drag the `lsci220` folder onto the Terminal window, and press Enter.
   - **Windows:** open the `lsci220` folder in File Explorer, right-click on an empty space, and choose **Open in Terminal**.

5. Install uv by pasting this command and pressing Enter:
   - **Mac:**
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - **Windows:**
     ```
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

6. Close the terminal window, then open a new one inside the `lsci220` folder (as in step 4).

7. Start marimo:
   ```
   uv run marimo edit
   ```
   The first time takes a few minutes while Python and the course libraries download.

8. Your browser opens the marimo home page. Click **`00_check_setup.py`**.

9. Scroll to the bottom of the notebook. A green **"All checks passed"** box means you're set up.

## Every time you use LSCI 220

1. Open a terminal inside the `lsci220` folder (install step 4).

2. Type `uv run marimo edit` and press Enter.

3. Work in your browser. Keep the terminal window open while you work.

4. When you're finished, close the browser tab, then press **Ctrl + C** in the terminal. If it asks whether to quit, type `y` and press Enter.

## Making your own notebook

1. On the marimo home page, click **Create a new notebook**.

2. Click **untitled marimo notebook** at the top of the page.

3. Type a name ending in `.py` (for example `assignment1.py`) and press Enter.

4. Your notebook is saved in the `lsci220` folder and appears on the home page next time.

## Tips for using marimo

### Indentation errors

Python uses indentation (spaces at the start of a line) to group code inside loops, `if` statements and functions. Every line in the same group must be indented by exactly the same amount.

The code in the course notebooks is indented with 2 spaces, but pressing **Tab** in marimo adds 4 spaces. If you add a line to existing code with Tab, you can get an `IndentationError`, even though the code looks fine.

To fix this, format the cell: click the **`...`** button at the top right of the cell and choose **Format cell** (or press **Cmd + B** on Mac, **Ctrl + B** on Windows). marimo will tidy up the cell so that all of the indentation is consistent.

## Backing up your work

1. Your notebooks are the `.py` files in the `lsci220` folder. Back them up regularly, for example by copying them to a USB drive or to your cloud storage.

2. If you know how to use GitHub, you can keep your notebooks in a GitHub repository instead.

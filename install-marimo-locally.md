# Install guide: Local marimo and python install

These are instructions for running marimo and the course material on your computer, locally. You should use this method if you have a personal laptop or computer you can reliably access through the course. You should not try this method on shared university computers. 

## Install (once only)

1. Download the course material (which is a zip folder): **[LINK TO COURSE FOLDER]**

2. Unzip it. You should have a folder called `LSCI-220`.

3. Move the `LSCI-220` folder somewhere on your computer that you can easily find again. I would suggest **not** putting it in a folder that actively syncs to OneDrive, iCloud, Dropbox or Google Drive. This is because syncing can cause problems with how the code works. That being said, you should still backup your course folder as you work through the material, especially as you make your own notebooks. 

4. Now you need to use your terminal to install marimo. First you have to naviate your terminal to the folder. If you know how to do so using terminal commands, go on. If not, here are easy ways to do so:
   - **Mac:** open **Terminal**, type `cd ` (with a space after it), drag the `LSCI-220` folder onto the Terminal window, and press Enter. This should point the terminal at the folder.
   - **Windows:** open the `LSCI-220` folder in File Explorer, right-click on an empty space, and choose **Open in Terminal**.

5. In the terminal, install uv by pasting this command and pressing Enter:
   - **Mac:**
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - **Windows:**
     ```
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```

6. Close the terminal window, then open a new one inside the `LSCI-220` folder (as in step 4).

7. Start marimo:
   ```
   uv run marimo edit
   ```
   This will install Python and everything else you need to run the course materials. The first time takes a few minutes while Python and the course libraries download. 

8. Your browser should automatically open the marimo home page. You should see a lot of options and all the notebooks in the course folder. Click **`00_check_setup.py`**. Follow the instructions and click the yellow "run all stale cells" button which is on the bottom rigth of your screen. 

9. Scroll to the bottom of the notebook. A green **"All checks passed"** box means you're set up.

## Every time you want to use the material LSCI 220

1. Open a terminal inside the `LSCI-220` folder (install step 4).

2. Type `uv run marimo edit` and press Enter.

3. Marimo will open in your browser. Keep the terminal window open while you work.

4. When you're finished, close the browser tab, then press **Ctrl + C** in the terminal. If it asks whether to quit, type `y` and press Enter.

## Making your own notebook

1. On the marimo home page, click **Create a new notebook**.

2. Click **untitled marimo notebook** at the top of the page.

3. Type a name ending in `.py` (for example `assignment1.py`) and press Enter.

4. Your notebook is saved in the `LSCI-220` folder and appears on the home page next time.

## Tips for using marimo

### Indentation errors

Python uses indentation (spaces at the start of a line) to group code inside loops, `if` statements and functions. Every line in the same group must be indented by exactly the same amount.

The code in the course notebooks is indented with 2 spaces, but pressing **Tab** in marimo adds 4 spaces. If you add a line to existing code with Tab, you can get an `IndentationError`, even though the code looks fine.

To fix this, format the cell: click the **`...`** button at the top right of the cell and choose **Format cell** (or press **Cmd + B** on Mac, **Ctrl + B** on Windows). marimo will tidy up the cell so that all of the indentation is consistent.

## Backing up your work

1. Your notebooks are the `.py` files in the `LSCI-220` folder. Back them up regularly, for example by copying them to a USB drive or to your cloud storage.

2. If you know how to use GitHub, you can keep your notebooks in a GitHub repository instead.

3. You can always redownload the course notebook and retain an original version of the course material. The main resources are simply files in folder, which you can move on your own outside of marimo.
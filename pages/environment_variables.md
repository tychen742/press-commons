# Environment Variables and PATH

An **environment variable** is a named setting that the operating system hands to every program you start. Tools read them to find their install folders, your home directory, and your preferences. The most important one for development is `PATH`, the list of folders the shell searches when you type a command. Learn to read, set, and check variables: most "command not found" errors and many "wrong version" surprises come from `PATH`.

```{contents}
:local:
:depth: 2
```

```{index} environment variable; PATH
```

## What a Variable Holds

A variable is a name and a text value. By convention, names are uppercase, such as `HOME`, `PATH`, or `JAVA_HOME`. Programs started from your terminal inherit a copy of the terminal's variables, so a change in one terminal window does not affect programs started elsewhere, and a change you make while a program is running does not reach that program.

## Read a Variable

::::{tab-set}
:::{tab-item} Windows
In PowerShell, `$env:` reads one variable, and `Get-ChildItem Env:` lists them all:

```powershell
$env:USERNAME
$env:Path
Get-ChildItem Env:
```
:::

:::{tab-item} macOS and Linux
Put `$` before the name to read a variable. `printenv` lists them all:

```bash
echo $HOME
echo $PATH
printenv
```
:::
::::

## How PATH Works

`PATH` is a list of folders. Windows separates the entries with `;`, and macOS and Linux separate them with `:`. When you type a command such as `python`, the shell checks each folder from the first entry to the last and runs the first match. Two consequences follow:

- If the folder that holds a tool is not on `PATH`, the shell reports that the command is not found, even though the tool is installed.
- If several versions of a tool are installed, the one in the earliest folder wins. To change the default, change the order of the entries.

To see which program a command runs, and every match in search order:

::::{tab-set}
:::{tab-item} Windows
```powershell
where.exe python
```
:::

:::{tab-item} macOS and Linux
```bash
which -a python3
```
:::
::::

## Set a Variable for One Terminal Session

A change made this way lasts until you close the terminal window. Use it to try a value before you make it permanent.

::::{tab-set}
:::{tab-item} Windows
```powershell
$env:MY_SETTING = "value"
$env:Path = "C:\tools\mytool\bin;" + $env:Path
```
:::

:::{tab-item} macOS and Linux
```bash
export MY_SETTING="value"
export PATH="$HOME/tools/mytool/bin:$PATH"
```
:::
::::

Put the new folder at the front of `PATH` to make it win over other versions, or at the end to make it a fallback. Keep the old value in the line (`$env:Path` or `$PATH`), or you will remove every other folder from `PATH` for that session.

## Set a Variable Permanently

::::{tab-set}
:::{tab-item} Windows
1. In Windows Search, type "environment variables" and open **Edit the system environment variables**. The System Properties window appears.

   ```{figure} figures/path-windows-system-properties.png
   :name: commons-path-windows-system-properties
   :alt: The Windows System Properties window on the Advanced tab, with the Environment Variables button at the bottom.
   :width: 400px

   The System Properties window
   ```

2. Click **Environment Variables**.
3. Under **User variables for [user]**, click **New** to add a variable, or select **Path** and click **Edit** to change the folder list.
4. In the Path editor, use **New** to add a folder, and **Move Up** or **Move Down** to change the search order.
5. Click **OK** in each window, then close and reopen PowerShell. You may need to sign out or restart.

The `setx` command sets a user variable from the command line, for example `setx MY_SETTING "value"`. It affects terminals opened afterward, not the one you typed it in. Avoid `setx` for `PATH`: it can cut a long value short.
:::

:::{tab-item} macOS and Linux
Put the `export` line in your shell configuration file so every new terminal runs it. Open the file in an editor such as `nano`:

```bash
nano ~/.zshrc      # zsh, the macOS default
nano ~/.bashrc     # bash, the usual Linux default
```

Add the line at the end of the file:

```bash
export MY_SETTING="value"
export PATH="$HOME/tools/mytool/bin:$PATH"
```

Save the file, then reload it in the current terminal (new terminals read it on their own):

```bash
source ~/.zshrc    # or: source ~/.bashrc
```
:::
::::

## Check Your Change

1. Open a new terminal window (or reload the file on macOS and Linux).
2. Read the variable back: `$env:MY_SETTING` in PowerShell, `echo $MY_SETTING` in zsh or bash.
3. Run the tool's own version command, and use `where.exe` or `which -a` to confirm it is the copy you meant.

If the old value or an old version still appears, you are probably in a terminal that was open before the change, or an earlier folder on `PATH` holds another copy of the tool. Check for typos in the folder path; a missing folder does not cause an error, it is just ignored.

## Variables for Specific Tools

<!-- slot: tool_examples -->
Some tools read a variable that names their install folder, and some need their `bin` folder on `PATH`. The tool's installation instructions say which. Your book's guide for the tool shows the exact values for your system.
<!-- /slot: tool_examples -->

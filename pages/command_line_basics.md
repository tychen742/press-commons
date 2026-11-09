# Command Line Basics

A command-line interface (CLI) lets you operate a computer by entering text commands. You will use it to find files, create folders, and start development tools. Learn the working directory and the prompt first: they tell you where a command will operate and which program is waiting for input.

```{contents}
:local:
:depth: 2
```

```{index} terminal; operating-system shell; prompt
```

## Terminal and Shell

A **terminal** is the window displaying text input and output. A **shell** is the program inside it that interprets operating-system commands. Windows Terminal can run PowerShell; macOS Terminal commonly runs Zsh; Linux terminals commonly run Bash. The same terminal can also host an application or a language REPL.

A prompt indicates that the current program is ready for input. Examples include `PS C:\Users\Alex>` in PowerShell and a prompt ending in `$` or `%` in Bash or Zsh. These are examples, not text to copy into a command. If you have entered a language REPL, exit it before typing operating-system commands. See {doc}`Interactive Language Environments <interactive_language_environments>`.

```{index} paths; working directory; relative path; absolute path
```

## Files, Folders, and Paths

A **directory**, also called a folder, contains files and other directories. A **path** identifies their location. An absolute path begins at a filesystem root, such as `C:\Users\Alex\workspace` on Windows or `/Users/alex/workspace` on macOS. A relative path starts from the shell's **current working directory**: the folder in which commands operate.

`.` means the current directory; `..` means its parent. Changing the working directory does not move the files. Put quotes around paths containing spaces, for example `cd "course projects"`.

```{index} pwd; Get-Location; cd; mkdir; ls; Get-ChildItem
```

## Navigate and Create a Practice Folder

Choose the commands for the shell you are using. PowerShell and Bash/Zsh are different command languages, even when their basic commands look similar.

| Task | Windows PowerShell | macOS/Linux Bash or Zsh |
| --- | --- | --- |
| Show the current directory. | `Get-Location` | `pwd` |
| Go to your home directory. | `cd ~` | `cd ~` |
| List files and folders. | `Get-ChildItem` | `ls` |
| Create a folder. | `mkdir tooling_practice` | `mkdir tooling_practice` |
| Enter that folder. | `cd tooling_practice` | `cd tooling_practice` |
| Return to its parent. | `cd ..` | `cd ..` |

From your home directory, create `tooling_practice`, enter it, and show its location. If the folder already exists, enter it instead of creating another one. Open a text editor, save `notes.txt` in that folder, and list the folder again. Explain the difference between the file's name and its full path.

```{index} command arguments; command history; terminal copy and paste
```

## Run and Repeat Commands

A command can include arguments, values describing what it should do. `cd tooling_practice` names a destination; `cd ..` names its parent. Your language guide will supply commands for building or running programs. Run them from the folder it specifies.

Press the up arrow to recall earlier commands. Tab completion can help fill in filenames. Copy only the command, excluding the prompt and displayed output. In macOS terminals, paste with Command+V; in Windows Terminal, use Ctrl+Shift+V; many Linux terminals also use Ctrl+Shift+V. Terminal applications can configure these shortcuts differently. Ctrl+C usually interrupts the running program rather than copying text.

If a command is not found, check its spelling, confirm the tool is installed, and open a new terminal after installation. If the tool is installed but still not found, its folder may be missing from `PATH`; see {doc}`Environment Variables and PATH <environment_variables>`. If a file is not found, check your working directory and the path you supplied.

```{index} Linux commands; grep; find; ps; kill; curl; chmod
```

## Common Linux and macOS Commands

The commands below are the ones you will use most often in a Bash or Zsh shell on Linux or macOS.[^linux-source] On Windows, they work in Windows Subsystem for Linux (WSL) or Git Bash, not in PowerShell. The examples use sample names such as `notes.txt` and `app.log`; replace them with your own. To learn more about any command, run `man` followed by its name, for example `man grep` (press `q` to leave).

<style>
.lx-sheet{display:grid;gap:14px;margin:1em 0;font-family:system-ui,sans-serif}
.lx-group{--lx:#be185d;border:1px solid #cbd5e1;border-top:4px solid var(--lx);border-radius:10px;background:#fff;color:#0f172a;padding:10px 14px 6px}
.lx-group h3{margin:0 0 6px;font-size:1.05rem;font-weight:700;color:var(--lx)}
.lx-row{display:grid;grid-template-columns:minmax(0,16rem) minmax(0,1fr);gap:4px 16px;padding:6px 0;border-top:1px solid #e2e8f0;align-items:baseline}
.lx-group h3+.lx-row{border-top:0}
.lx-row code{font:600 .92em ui-monospace,monospace;color:var(--lx);background:none;padding:0;white-space:pre-wrap;overflow-wrap:anywhere}
.lx-row span{font-size:.95em;color:#334155}
.lx-row span code{font-weight:400;color:#0f172a;background:#e2e8f0;padding:0 .25em;border-radius:3px}
.lx-search{--lx:#be185d}.lx-files{--lx:#1d4ed8}.lx-proc{--lx:#7e22ce}.lx-net{--lx:#15803d}.lx-view{--lx:#b45309}
@media (max-width:560px){.lx-row{grid-template-columns:1fr;gap:2px}}
html[data-theme="dark"] .lx-group{background:#1e293b;color:#e2e8f0;border-color:#334155;border-top-color:var(--lx)}
html[data-theme="dark"] .lx-row{border-top-color:#334155}
html[data-theme="dark"] .lx-row span{color:#cbd5e1}
html[data-theme="dark"] .lx-row span code{background:#334155;color:#e2e8f0}
html[data-theme="dark"] .lx-search{--lx:#f472b6}html[data-theme="dark"] .lx-files{--lx:#60a5fa}html[data-theme="dark"] .lx-proc{--lx:#c084fc}html[data-theme="dark"] .lx-net{--lx:#4ade80}html[data-theme="dark"] .lx-view{--lx:#fbbf24}
</style>
<div class="lx-sheet">
<section class="lx-group lx-search" aria-label="Search and Filter"><h3>Search and Filter</h3><div role="list"><div class="lx-row" role="listitem"><code>grep &quot;error&quot; app.log</code><span>Show the lines of a file that contain a word. Add <code>-i</code> to ignore case.</span></div><div class="lx-row" role="listitem"><code>grep -r &quot;TODO&quot; src</code><span>Search every file under a directory.</span></div><div class="lx-row" role="listitem"><code>find . -name &quot;*.txt&quot;</code><span>Find files by name under the current directory; <code>*</code> matches any characters.</span></div><div class="lx-row" role="listitem"><code>locate notes.txt</code><span>Find files by name quickly from a prebuilt index. Not installed everywhere, and the index can be out of date; <code>find</code> always works.</span></div><div class="lx-row" role="listitem"><code>less app.log</code><span>Read a file one screen at a time. Space goes forward, <code>b</code> back, <code>/word</code> searches, <code>q</code> quits.</span></div><div class="lx-row" role="listitem"><code>tail -n 20 app.log</code><span>Show the last 20 lines. <code>tail -f</code> keeps showing new lines as they are written (Ctrl+C stops).</span></div></div></section>
<section class="lx-group lx-files" aria-label="Files and Directories"><h3>Files and Directories</h3><div role="list"><div class="lx-row" role="listitem"><code>pwd</code><span>Show the current directory's full path.</span></div><div class="lx-row" role="listitem"><code>ls -al</code><span>List all files, including hidden ones (names that start with <code>.</code>), with sizes, dates, and permissions.</span></div><div class="lx-row" role="listitem"><code>cd projects</code><span>Change to another directory. <code>cd ..</code> goes up one level, <code>cd ~</code> goes home.</span></div><div class="lx-row" role="listitem"><code>mkdir projects</code><span>Create a directory. <code>mkdir -p a/b/c</code> creates the missing parents too.</span></div><div class="lx-row" role="listitem"><code>cp notes.txt backup.txt</code><span>Copy a file. Copy a directory with <code>cp -r</code>.</span></div><div class="lx-row" role="listitem"><code>mv notes.txt docs/</code><span>Move a file, or rename it: <code>mv old.txt new.txt</code>.</span></div><div class="lx-row" role="listitem"><code>rm notes.txt</code><span>Delete a file. <code>rm -r</code> deletes a directory and everything in it. There is no trash and no undo.</span></div></div></section>
<section class="lx-group lx-view" aria-label="View and Edit Files"><h3>View and Edit Files</h3><div role="list"><div class="lx-row" role="listitem"><code>cat notes.txt</code><span>Print a whole file. Best for short files; use <code>less</code> for long ones.</span></div><div class="lx-row" role="listitem"><code>head -n 5 notes.txt</code><span>Show the first 5 lines (10 without <code>-n</code>).</span></div><div class="lx-row" role="listitem"><code>touch notes.txt</code><span>Create an empty file, or update the modified time of one that exists.</span></div><div class="lx-row" role="listitem"><code>nano notes.txt</code><span>Edit a file in the terminal. Ctrl+O saves and Ctrl+X exits; the shortcuts are listed at the bottom of the screen.</span></div><div class="lx-row" role="listitem"><code>ln -s /data/shared shared</code><span>Create a symbolic link: a shortcut named <code>shared</code> that points to another path.</span></div><div class="lx-row" role="listitem"><code>chmod +x run.sh</code><span>Change permissions; here, allow the file to run as a program. <code>ls -l</code> shows the current permissions.</span></div></div></section>
<section class="lx-group lx-proc" aria-label="Processes and Jobs"><h3>Processes and Jobs</h3><div role="list"><div class="lx-row" role="listitem"><code>ps aux</code><span>List every running process with its owner, process ID (PID), and CPU and memory use.</span></div><div class="lx-row" role="listitem"><code>top</code><span>Show processes live, busiest first. Press <code>q</code> to quit.</span></div><div class="lx-row" role="listitem"><code>jobs</code><span>List the jobs started from this shell. Ctrl+Z pauses the running job; <code>command &amp;</code> starts one in the background.</span></div><div class="lx-row" role="listitem"><code>fg %1</code><span>Bring job 1 back to the foreground.</span></div><div class="lx-row" role="listitem"><code>bg %1</code><span>Resume paused job 1 in the background.</span></div><div class="lx-row" role="listitem"><code>kill 4321</code><span>Ask process 4321 to stop. If it does not, <code>kill -9 4321</code> stops it at once, without letting it clean up.</span></div></div></section>
<section class="lx-group lx-net" aria-label="Networking and Diagnostics"><h3>Networking and Diagnostics</h3><div role="list"><div class="lx-row" role="listitem"><code>ping -c 4 example.com</code><span>Check whether a host answers and how long replies take. Without <code>-c 4</code>, Linux keeps going until Ctrl+C.</span></div><div class="lx-row" role="listitem"><code>curl https://example.com</code><span>Fetch a URL and print the response; the usual way to call a web API. <code>curl -O URL</code> saves it as a file.</span></div><div class="lx-row" role="listitem"><code>wget https://example.com/data.csv</code><span>Download a file. Not installed on macOS by default; use <code>curl -O</code> there.</span></div><div class="lx-row" role="listitem"><code>nslookup example.com</code><span>Look up a domain's IP address in DNS.</span></div><div class="lx-row" role="listitem"><code>dig example.com</code><span>Show a detailed DNS answer, including record types and how long it may be cached.</span></div><div class="lx-row" role="listitem"><code>traceroute example.com</code><span>Show each network hop on the way to a host; useful when a site is slow or unreachable.</span></div></div></section>
</div>

```{rubric} Footnotes
```

[^linux-source]: The grouping and choice of commands are adapted from a Linux commands post on X {cite}`pythonpr_2026_linux`. This section gives each command a concrete example, corrects `In -s` to `ln -s`, and notes where a command differs between Linux and macOS or is not installed by default.

# Offline Series Manager
~~*This needs a better name*~~

# Module development
Place two files in `modules/`: `modulename.json` and `modulename.py`, adjusting the names of the files as desired. The names must be identical.
`modulename.json` should have two keys in it:
 - `name`, the name of the module, which must match the name of the file without the .json (case-sensitive)
 - `menu_listing`, what the menu option for this module will be.

When a user runs your module it will run the `main()` function from your file with one argument: `video`, the name of the video file. It does not include the `videos/` directory.

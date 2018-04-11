# VIAJE
### Vim Isn't an Acceptable Jex Editor

## Installation

This plugin depends on the xxd executable being in your path. For Linux users,
this step is almost certainly already done. Windows users: good luck with that.
Let me know if you have some tips.

To install the plugin, clone the repo, then copy the `ftplugin` directory into
`~/.vim`. Or, if you're sane, add the line

    Plugin 'dmwit/viaje'

to your collection of [vundle](https://github.com/VundleVim/Vundle.vim)
packages. (Other vim package managers should be similar.)

## Usage

Edit a file in binary mode. From the command line:

    vim -b exploits.exe

Or from within vim:

    :e ++bin exploits.exe

I haven't written any filetype autodetection rules, so for now you must turn on
hex-editing mode manually by setting the filetype:

    :set ft=xxd

You'll see something like this:

    00000000: 7f45 4c46 0201 0100 0000 0000 0000 0000  .ELF............
    00000010: 0200 3e00 0100 0000 0004 4000 0000 0000  ..>.......@.....
    00000020: 4000 0000 0000 0000 d818 0000 0000 0000  @...............
    00000030: 0000 0000 4000 3800 0900 4000 1d00 1c00  ....@.8...@.....
    00000040: 0600 0000 0500 0000 4000 0000 0000 0000  ........@.......
    00000050: 4000 4000 0000 0000 4000 4000 0000 0000  @.@.....@.@.....
    00000060: f801 0000 0000 0000 f801 0000 0000 0000  ................

You can edit the hex codes in the middle. The ASCII representation on the right
is ignored (and updated) when writing. The byte numbers on the left are not
ignored, so be careful that you keep them in synch with whatever changes you
make. xxd really expects exactly 16 bytes worth of hex codes on each line, so
if you need to insert or delete something that isn't a multiple of 16 bytes
that's going to really suck.

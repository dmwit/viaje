import vim
from subprocess import Popen, PIPE

# Get the encoding used to interpret bytes stored in vim's buffers. When
# 'binary' is set, vim doesn't attempt to interpret its buffers as text, so in
# that case there's not really a "right" thing to do, but the latin1 encoding
# faithfully roundtrips any sequence of bytes, so we collude with get_fenc()
# and report that when 'binary' is set.
def get_enc():
    bos = vim.current.buffer.options
    enc = vim.options['encoding']
    if bos['binary']: enc = 'latin1'
    return enc

# Get the encoding used to store codepoints in a file. When 'binary' is set,
# vim doesn't attempt to convert from the bytes in its internal buffers to text
# and back to bytes again, so in that case there's not really a "right" thing
# to do, but the latin1 encoding faithfully roundtrips any sequence of bytes,
# so we collude with get_enc() and report that when 'binary' is set.
def get_fenc():
    bos = vim.current.buffer.options
    fenc = bos['fileencoding']
    if not fenc: fenc = vim.options['encoding']
    if bos['binary']: fenc = 'latin1'
    return fenc

# Make a best-effort attempt to get the bytes that were in the file
# corresponding to the current buffer. It is the user's responsibility to make
# sure that the file was opened under one of the following conditions:
# * the file was specified on the command line and -b was used
# * ++bin was included in the :edit command
# * the 'binary' option is set
# * 'fileencodings' was chosen in a way that makes it possible to losslessly
#   decode the file and all the codepoints that result are representable in the
#   currently set 'encoding'
# * ++enc was included in the :edit command, and the encoding chosen there is
#   capable of losslessly decoding the file, and all the codepoints that result
#   are representable in the currently set 'encoding'
def get_bytes():
    b = vim.current.buffer

    if b.options['binary']:
        newline = u'\n'
    elif b.options['fileformat'] == 'dos':
        newline = u'\r\n'
    elif b.options['fileformat'] == 'unix':
        newline = u'\n'
    elif b.options['fileformat'] == 'mac':
        newline = u'\r'
    else:
        # should be impossible
        raise('Unexpected fileformat %s' % b.options['fileformat'])

    enc = get_enc()
    text = newline.join(s.decode(enc) for s in b)

    if b.options['endofline']:
        text += newline

    return text.encode(get_fenc())

def xxd(args):
    proc = Popen(['xxd'] + args, stdin=PIPE, stdout=PIPE)
    stdout, _ = proc.communicate(get_bytes())
    if proc.returncode != 0: raise('xxd bombed out')
    return stdout.decode('latin1')

def to_human():
    enc = get_enc()
    vim.current.buffer[:] = [line.encode(enc) for line in xxd([]).splitlines()]

def from_human():
    # N.B. *not* splitlines()! That function tries to be too clever about \r
    # and \r\n. This is only correct because we are setting 'binary' in the
    # vimscript that loads this.
    enc = get_enc()
    vim.current.buffer[:] = [line.encode(enc) for line in xxd(['-r']).split('\n')]

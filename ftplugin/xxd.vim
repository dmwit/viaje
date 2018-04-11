if exists("b:did_xxd_ftplugin")
    finish
endif

let b:undo_ftplugin = "unlet b:did_xxd_ftplugin"
let b:did_xxd_ftplugin = 1

execute("pyfile " . fnamemodify(resolve(expand("<sfile>:p")), ":h") . "/xxd.py")

let b:undo_ftplugin .= " | execute(\"python from_human()\")"
python to_human()

if 1-&binary
    let b:undo_ftplugin .= " | setlocal nobinary"
endif
setlocal binary

" There's no sane way to track whether/how to undo this as editing progresses.
" So we won't add this to b:undo_ftplugin.
set noendofline
" We used to set 'fileformat' and 'fileencoding' in this block of non-undone
" code. But when 'binary' is set, those are ignored, so we can avoid the
" "how to undo it" problem completely by just never doing it.

augroup xxd
    autocmd! BufWritePre <buffer>
    autocmd  BufWritePre <buffer> python from_human()

    autocmd! BufWritePost <buffer>
    autocmd  BufWritePost <buffer> python to_human()
augroup END
let b:undo_ftplugin .= " | augroup xxd"
let b:undo_ftplugin .= " | autocmd! BufWritePre <buffer>"
let b:undo_ftplugin .= " | autocmd! BufWritePost <buffer>"
let b:undo_ftplugin .= " | augroup END"


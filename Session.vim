let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
exe "cd " . escape(expand("<sfile>:p:h"), ' ')
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +1 munin/bot/bot.py
badd +1 munin/control/control.py
badd +1 munin/irc_bot/irc_bot.py
badd +1 munin/ircbot.py
badd +1 munin/__main__.py
badd +1 ~/Programmation/Python/Onolen/modules/reaction/reaction.py
badd +1 ~/Programmation/Python/Onolen/modules/system/system.py
badd +1 munin/functionnalities/dice_launcher/dice_launcher.py
badd +1 munin/functionnalities/corrector/corrector.py
badd +1 munin/functionnalities/git_watcher/git_watcher.py
badd +1 munin/functionnalities/__init__.py
badd +1 munin/functionnalities/todolist/todolist.py
badd +1 munin/functionnalities/helper/helper.py
badd +1 munin/functionnalities/prolog_db/prolog_db.py
badd +1 munin/functionnalities/rsswatcher/rsswatcher.py
badd +14 munin/functionnalities/functionnalities.py
badd +3 ~/Programmation/Projets/EvolAcc/EvolAcc
badd +44 ~/Programmation/Projets/EvolAcc/EvolAcc/evolacc/config/config.py
badd +1 munin/config/config.py
badd +11 ~/Programmation/Projets/EvolAcc/EvolAcc/evolacc/config/conflog.py
badd +0 munin/plugin/plugin.py
argglobal
silent! argdel *
argadd ~/Programmation/Python/Munin/munin/bot/bot.py
set stal=2
edit munin/bot/bot.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 12 - ((11 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
12
normal! 0
lcd ~/Programmation/Python/Munin
tabedit ~/Programmation/Python/Munin/munin/control/control.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 15 - ((14 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
15
normal! 0
lcd ~/Programmation/Python/Munin
tabedit ~/Programmation/Python/Munin/munin/plugin/plugin.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 1 - ((0 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
1
normal! 0
lcd ~/Programmation/Python/Munin
tabedit ~/Programmation/Python/Munin/munin/config/config.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 18 - ((17 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
18
normal! 0
lcd ~/Programmation/Python/Munin
tabedit ~/Programmation/Python/Munin/munin/__main__.py
set splitbelow splitright
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
argglobal
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
silent! normal! zE
let s:l = 6 - ((5 * winheight(0) + 28) / 56)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
6
normal! 0
lcd ~/Programmation/Python/Munin
tabnext 3
set stal=1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :

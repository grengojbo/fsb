" Конфигурационный файл Vim IDE
" Запрещаем восстановление настроек из сессии, " т. к. тогда при изменении ~/.vimrc даже после
" перезагрузки IDE новые настройки не будут вступать в силу.
set sessionoptions-=options
" Настраиваем работу с ctags -->
set tags+=.vim/ctags
function! MyUpdateIdeCtags()
    silent !ctags --languages=Python -f .vim/ctags -R .
endfunction
let MyUpdateCtagsFunction = "MyUpdateIdeCtags"
" Настраиваем работу с ctags <--
" Обновляем базу ctags при старте IDE
call {MyUpdateCtagsFunction}()
" При сохранении любого *.py файла обновляем базу ctags
au BufWritePost *.py :call {MyUpdateCtagsFunction}()
" При закрытии Vim'а сохраняем информацию о текущей сессии
au VimLeave * :mksession! .vim/ide.session
" Загружаем ранее сохраненную сессию -->
if getfsize(".vim/ide.session") >= 0
    source .vim/ide.session
endif
" Загружаем ранее сохраненную сессию <--

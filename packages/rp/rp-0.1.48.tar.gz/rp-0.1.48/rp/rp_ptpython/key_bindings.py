from __future__ import unicode_literals

from rp.prompt_toolkit.document import Document
from rp.prompt_toolkit.enums import DEFAULT_BUFFER
from rp.prompt_toolkit.filters import HasSelection, IsMultiline, Filter, HasFocus, Condition, ViInsertMode, EmacsInsertMode
from rp.prompt_toolkit.key_binding.vi_state import InputMode
from rp.prompt_toolkit.key_binding.registry import Registry
from rp.prompt_toolkit.keys import Keys,Key
from rp.prompt_toolkit.buffer import Buffer

from rp import *
__all__ = (
    'load_python_bindings',
    'load_sidebar_bindings',
    'load_confirm_exit_bindings',
)
from rp import *

class TabShouldInsertWhitespaceFilter(Filter):
    """
    When the 'tab' key is pressed with only whitespace character before the
    cursor, do autocompletion. Otherwise, insert indentation.

    Except for the first character at the first line. Then always do a
    completion. It doesn't make sense to start the first line with
    indentation.
    """
    def __call__(self, cli):
        b = cli.current_buffer
        before_cursor = b.document.current_line_before_cursor

        return bool(b.text and (not before_cursor or before_cursor.isspace()))

def has_selected_completion(buffer):# If we have a completion visibly selected on the menu
    return buffer.complete_state and buffer.complete_state.complete_index is not None


def load_python_bindings(python_input):
    """
    Author: Ryan Burgert
    """
    registry = Registry()

    sidebar_visible = Condition(lambda cli: python_input.show_sidebar)
    handle = registry.add_binding
    has_selection = HasSelection()
    vi_mode_enabled = Condition(lambda cli: python_input.vi_mode)

    #region Ryan Burgert Stuff
    from rp.prompt_toolkit.key_binding.input_processor import KeyPressEvent
    from rp.prompt_toolkit.document import Document
    #region Template
    def _(event):# Parenthesis completion
        #
        assert isinstance(event,KeyPressEvent)
        #
        from rp.prompt_toolkit.buffer import Buffer
        buffer=event.cli.current_buffer
        assert isinstance(buffer,Buffer)
        #
        document=buffer.document
        assert isinstance(document,Document)
        document.insert_after()
        #
        text=document.text_after_cursor
        assert isinstance(text,str)
        #
    # buffer.insert_text("(")
    # if not text or text[0] in " \t\n":
    #     buffer.insert_text(")")
    #     buffer.cursor_left(count=1)
#endregion
    for char in '~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./':# Normal keyboard inputs
        def go(c):
            @handle(c,filter=has_selection)
            def _(event):
                buffer=event.cli.current_buffer
                # buffer.on_text_changed+=lambda *x:buffer.save_to_undo_stack(clear_redo_stack=False)
                buffer.cut_selection()# Overwrite text if we have something selected
                buffer.insert_text(c)
        go(char)



    #
    @handle(Keys.ShiftLeft)
    def _(event):
        """
        Select from the history.
        """
        buffer=event.cli.current_buffer
        if buffer.document.current_line_before_cursor:
            buffer.cursor_left(1000000)
        elif buffer.cursor_position:
            buffer.cursor_up()
            move_line_down(buffer)
            buffer.cursor_up()
            buffer.cursor_left(1000000)

    # @handle(Keys.ControlBackslash)
    # def _(event):
    #     buffer=event.cli.current_buffer
    #     pseudo_terminal(merge_dicts(r_iterm_comm.globa,{ans:buffer.document.text}))

    @handle(Keys.ShiftRight)
    def _(event):
        buffer=event.cli.current_buffer
        if buffer.document.current_line_after_cursor:
            buffer.cursor_right(1000000)
        else:
            move_line_down(buffer)
    def move_line_down(buffer,up=False):
        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        buffer.cursor_left(1000000)
        if not buffer.cursor_position:
            buffer.delete(2)
        buffer.cursor_right(1000000)
        # print("Ima doing/ it!")
        delete_current_line(buffer)
        buffer.cursor_right(10000)
        buffer.cursor_down(1)
        buffer.cursor_left(10000)
        #region Adaptive indentation: Currently not implemented. Sticking to simplicity.
        if False:
            buffer.insert_line_above(copy_margin=not up)
            buffer.insert_text(current_line.lstrip() if not up else current_line)
            text=buffer.document.text
            lstrip=text.lstrip()
        else:
            buffer.insert_line_above(copy_margin=False)
            buffer.insert_text(current_line)
            lstrip=text=buffer.document.text

        # buffer.cursor_down(1)
        # buffer.cursor_right(1000000)
        buffer.document=Document(lstrip,buffer.document.cursor_position+(len(lstrip)-len(text)),buffer.document.selection)

    #These keys don't respond on the mac terminal
    # @handle(Keys.ShiftUp)
    # def _(event):
    #     print(324982308974078923)
    #     event.cli.current_buffer.cursor_right(1000000)
    #
    # @handle(Keys.ShiftDown)
    # def _(event):
    #     print(324982308974078923)
    #     buffer=event.cli.current_buffer
    #     document=buffer.document
    #     current_line=document.current_line

    @handle(Keys.ControlD)# Duplicate current line Only applies when there's text, else it will trigger the exit
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        buffer.cursor_right(10000)
        current_line=document.current_line
        # buffer.insert_line_below()
        buffer.insert_text("\n"+current_line)

    def delete_current_line(buffer):
        document=buffer.document
        current_line=document.current_line
        buffer.cursor_left(10000)
        firstline=buffer.cursor_position==0
        buffer.delete(len(current_line))
        buffer.delete_before_cursor()
        if firstline:
            buffer.delete()
        else:
            buffer.cursor_down()


    @handle(Keys.ControlDelete)# Delete current line
    def _(event):
        buffer=event.cli.current_buffer
        delete_current_line(buffer)

    #region Bracket Match Writers
    function_comma_flag=False# Used to keep track of when we are writing arguments to fucntions that were initially parenthesized with the spacebar
    can_take_no_args=False# Doesn't practically matter right now if function_comma_flag is false
    @handle(" ")
    def _(event):# Spacebar
        buffer=event.cli.current_buffer


        nonlocal function_comma_flag# ,can_take_no_args
        # from rp import mini_terminal
        # exec(mini_terminal)
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor

        if document.text=='':# What else would we possibly want the spacebar for?
            buffer.insert_text('ans()')
            buffer.cursor_left()
            function_comma_flag=True
            return


        if before.startswith('!'):# Don't do anything special
            buffer.insert_text(' ')
            return

        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor
        if before_line=='def':
            buffer.insert_text(' :')
            buffer.cursor_left()
            return
        from rp import is_namespaceable
        if before_line.startswith('def ') and len(before_line.split(' '))==2:
            if after_line.strip()==':' and is_namespaceable(before_line.split(' ')[-1]):
                buffer.insert_text('()')
                buffer.cursor_left()
                return

        if before_line.endswith(' imoprt') or before_line.startswith("imoprt"):# This is a really common typo for me
            buffer.delete_before_cursor(6)
            buffer.insert_text('import ')
            return



        from rp import space_split,is_namespaceable
        import rp.r_iterm_comm as r_iterm_comm
        split=space_split(before_line)
        from rp import printed
        from_or_import_on_beginning_of_line=before_line.lstrip().startswith("import ") or before_line.lstrip().startswith("from ")
        try:
            function_comma_flag=function_comma_flag and( after_line.startswith(")") or after_line.startswith("'") or after_line.startswith('"') or after_line.startswith(']') or after_line.startswith(']') )
            token_of_interest=name_of_interest=None
            try:
                # fansi_print("\n\n"+split[-1]+"\n\n")

                string=''
                for char in reversed(before_line):
                    if not is_namespaceable(char) and char not in '.':
                        break
                    string=char+string
                name_of_interest=string
                token_of_interest=eval(string,r_iterm_comm.globa)  # ≣token_of_interest=r_iterm_comm.rp_evaluator(string,True)# Should be just a name so there should be no side effects

                #
                # for char in string:
                #     if not char.isalnum() and char not in '.' and not is_namespaceable(char):
                #         string=string.replace(char,' ')
                # name_of_interest=string
                # token_of_interest=eval(string,r_iterm_comm.globa)# ≣token_of_interest=r_iterm_comm.rp_evaluator(string,True)# Should be just a name so there should be no side effects
            except:pass
            if not from_or_import_on_beginning_of_line and not before_line.endswith(" ") and callable(token_of_interest):
                function_comma_flag=True
                import inspect
                # try:
                #     can_take_no_args=len(inspect.getfullargspec(token_of_interest).args)==0
                # except:# Probably a builtin function
                #     can_take_no_args=0 or token_of_interest is print
                buffer.insert_text('()')
                buffer.cursor_left(count=1)
            # region Brackets....they work but conceptually they're annoying.
            # elif not from_or_import_on_beginning_of_line and not before_line.endswith(" ") and hasattr(token_of_interest,'__getitem__'):
            #     buffer.insert_text('[]')
            #     buffer.cursor_left(count=1)
            #endregion
            elif before_line and after_line and before_line[-1]+after_line[0] in ['()','[]','{}']:
                if document.text=='ans()':
                    buffer.delete()
                    buffer.delete_before_cursor(count=40000)
                    buffer.insert_text(' ')
                    return

                buffer.delete_before_cursor(count=1)
                buffer.cursor_right(count=1)
                buffer.delete_before_cursor(count=1)
                # if can_take_no_args:
                #     if function_comma_flag:
                #             buffer.insert_text(',')
                #     else:
                #             buffer.insert_text('(),')
                # else:
                #     if function_comma_flag:
                #         buffer.insert_text(',')
                #     else:
                #         buffer.insert_text(' ')
                if function_comma_flag and after_line.startswith("))"):
                    buffer.insert_text(',')
                else:
                    buffer.insert_text(' ')
            elif function_comma_flag and after_line.startswith(')'):
                if before_line.endswith(","):
                    buffer.delete_before_cursor()
                    buffer.cursor_right()
                    if after_line.startswith("))"):
                        buffer.insert_text(',')
                else:
                    buffer.insert_text(',')
            elif not after_line and all(is_namespaceable(x) for x in split) and len(split)==2 and split[0]=='def':
                buffer.insert_text('():')
                buffer.cursor_left(count=2)
            elif before_line.lstrip() in['if','while','for','with','try','except'] or split and name_of_interest=='lambda':
                buffer.insert_text(' :')
                buffer.cursor_left(count=1)
            elif before_line and after_line and before_line[-1]==','and after_line[0]==':':# for after lambda x,a,b,c,cursor:
                buffer.delete_before_cursor(count=1)
                buffer.cursor_right(count=1)
            elif len(split)>=2 and split[-2]=='lambda' and ':'not in name_of_interest or after_line=='):' and not before_line.rstrip().endswith(','):# new argument in def
                buffer.insert_text(',')
            else:
                buffer.insert_text(' ')
        except Exception as e:
            from rp import print_stack_trace
            print_stack_trace(e)
    @handle(":")
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        before=document.text_before_cursor
        after= document.text_after_cursor

        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor
        if after_line==':':
            buffer.cursor_right(count=1)
        else:
            buffer.insert_text(':')
    @handle("=")
    def _(event):
        import rp.r_iterm_comm as r_iterm_comm

        buffer=event.cli.current_buffer
        document=buffer.document
        #
        before=document.text_before_cursor
        after= document.text_after_cursor
        before_line=before.split('\n')[-1]# all on same line, but before cursor
        after_line=after.split('\n')[0]# ditto but after cursor
        char_operators=['','+','-','*','/','%','//','**','&','|','^','>>','<<']
        letter_operators=['and','or','not','==','!=','>=','<=']
        var=r_iterm_comm.last_assignable_comm
        if before_line.lstrip().endswith('.'):# the .= operator
            buffer.delete_before_cursor(count=1)
            assign_to=before_line.lstrip()
            buffer.insert_text("="+assign_to)
        elif before=='ans('and after==')':# Space + equals -> import torch;
            buffer.delete()
            buffer.delete_before_cursor(count=1000)
            buffer.insert_text("ans="+str(var))

        elif var and before==var+"=":
            buffer.delete_before_cursor(count=1000)
            buffer.insert_text("==")

        elif var and not after and before in letter_operators:# User hasn't typed anything in yet
            buffer.cursor_left(count=10000)
            buffer.insert_text(var)
            buffer.insert_text("=")
            buffer.insert_text(var)
            if before.isalpha():# and, or, not
                buffer.insert_text(" ")# We need a space
            buffer.cursor_right(count=10000)
        elif var and not after and before in char_operators:# User hasn't typed anything in yet
            buffer.cursor_left(count=10000)
            buffer.insert_text(var)
            buffer.cursor_right(count=10000)
            buffer.insert_text('=')
        else:
            buffer.insert_text('=')

    import os
    if os.name != 'nt':#If we are NOT running windows, which screws EVERYTHING up...
        # @handle(Keys.ControlC)
        # def _(event):
        #     buffer=event.cli.current_buffer
        #     # document=buffer.document
        #     # before=document.text_before_cursor
        #     # after= document.text_after_cursor
        #     buffer.insert_text('RETURN')
        @handle(Keys.ControlH)
        def _(event):
            buffer=event.cli.current_buffer
            buffer.insert_text('HISTORY')
        @handle(Keys.ControlU)
        def _(event):
            buffer=event.cli.current_buffer
            buffer.insert_text('UNDO')
        @handle(Keys.ControlP)
        def _(event):
            buffer=event.cli.current_buffer
            buffer.insert_text('PREV')



    @handle(Keys.Backspace)
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        selection_tuples=list(document.selection_ranges())
        if not selection_tuples:
            before=document.text_before_cursor
            after= document.text_after_cursor
            if before and after:
                pair=before[-1]+after[0]
                if pair in ['()','{}','[]',"''",'""']:
                    buffer.cursor_right(count=1)
                    buffer.delete_before_cursor(count=2)
                    return
            buffer.delete_before_cursor(count=1)
        else:
            buffer.cut_selection()

    @handle(Keys.Right)
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        selection_tuples=list(document.selection_ranges())
        for t in selection_tuples:
            buffer._set_cursor_position(t[1])
            buffer.exit_selection()
        else:
            cpos=buffer.cursor_position
            buffer.cursor_right(1)
            if buffer.cursor_position==cpos:
                buffer=event.cli.current_buffer
                buffer._set_cursor_position(min(buffer.cursor_position + 1,len(buffer.document.text)))
            # buffer.cursor_right(0)# Gets stuck on ends of lines. Not as good as the new version

    @handle(Keys.Left)
    def _(event):
        buffer=event.cli.current_buffer
        document=buffer.document
        selection_tuples=list(document.selection_ranges())
        for t in selection_tuples:# Handle arrow-keys on selection by putting the cursor on beginning or end of selection
            buffer._set_cursor_position(min(t[0]+1,len(buffer.document.text)))
            buffer.exit_selection()
        else:
            cpos=buffer.cursor_position
            buffer.cursor_left(1)
            if cpos==buffer.cursor_position:
                buffer=event.cli.current_buffer
                buffer._set_cursor_position(max(buffer.cursor_position - 1,0))

    @handle(Keys.Down)
    def _(event):
        buffer=event.cli.current_buffer
        assert isinstance(buffer,Buffer)
        if has_selected_completion(buffer) or not '\n' in buffer.document.text:
            buffer.auto_down()# Will select next completion
            try:
                if not has_selected_completion(buffer) or not '\n' in buffer.document.text3:#
                    buffer.auto_down()# So we don't get stuck when we come back around again
            except:pass
        else:
            temp=buffer.complete_state
            try:
                buffer.complete_state=False
                buffer.auto_down()# Will select next completion
            finally:
                buffer.complete_state=temp

    @handle(Keys.Up)
    def _(event):
        buffer=event.cli.current_buffer
        assert isinstance(buffer,Buffer)
        if has_selected_completion(buffer):#  Up is the only one that can initially select a history item
            buffer.auto_up()# Will select next completion
            if not has_selected_completion(buffer):
                buffer.auto_up()# So we don't get stuck when we come back around again
        else:
            temp=buffer.complete_state
            try:
                buffer.complete_state=False# So we don't select a completion
                buffer.auto_up()# Will select next completion
            finally:
                buffer.complete_state=temp





    @handle(Keys.ControlZ)# On mac this is alt+z
    def _(event):
        buffer=event.cli.current_buffer
        # print(buffer._redo_stack)
        buffer.undo()

    import rp.r_iterm_comm as r_iterm_comm
    @handle(Keys.ControlV)# On mac this is alt+z
    def _(event):
        buffer=event.cli.current_buffer
        from rp import string_from_clipboard
        clip=r_iterm_comm.clipboard_text
        try:
            clip=string_from_clipboard()
        except:
            pass# Paste failed
        buffer.cut_selection()
        buffer.insert_text(clip)


    @handle(Keys.ControlC)# ,filter=has_selection)# On mac this is alt+z
    def _(event):
        buffer=event.cli.current_buffer
        selection_tuples=list(buffer.document.selection_ranges())

        #region
        if not selection_tuples:
            selection_tuples=[]
            line=buffer.document.current_line
            to_copy="\n" + line# ' ' * (len(line)-len(line.lstrip()))
            buffer.cursor_right(12323213)
        else:
            to_copy=""
            for t in selection_tuples:
                to_copy+=buffer.document.text[t[0]:t[1]+1]
        r_iterm_comm.clipboard_text=to_copy
        from rp import string_to_clipboard
        try:
            string_to_clipboard(to_copy)
        except:
            pass# Copy failed


    def inc_dec(inc_or_dec:str):# ++ ⟶ +=1
        @handle(inc_or_dec)
        def _(event):
            buffer=event.cli.current_buffer
            document=buffer.document
            before=document.text_before_cursor
            before_line=document.current_line_before_cursor
            after_line=document.current_line_after_cursor
            after= document.text_after_cursor
            current_line= document.current_line
            # import r_iterm_comm
            # if not after and r_iterm_comm.last_assignable_comm and before[-1]==inc_or_dec:# So you can do ++ -> assignable ++= (because +=1 -> assignable+=1)
            #     buffer.cursor_left(count=1000)
            #     buffer.insert_text(r_iterm_comm.last_assignable_comm)
            #     buffer.cursor_right(count=1000)
            #     return
            # print('GAGAGAGA')
            from rp import is_namespaceable
            if inc_or_dec == '-' and all(is_namespaceable(x) for x in before_line if x not in ' ') and before_line.lstrip().startswith('def '):# When writing the title of a function, you don't have to use _ you can type - and it will turn it into _
                buffer.insert_text('_')
                return
            if inc_or_dec=='+' and (after_line.startswith('"') or after_line.startswith('"')):
                buffer.insert_text('+')
                buffer.cursor_left()
                return
            if before and before[-1]==inc_or_dec and is_namespaceable(before_line[:-1].lstrip()):
                if not after_line:
                    buffer.insert_text("=1")
                else:
                    buffer.insert_text(inc_or_dec)
                    buffer.cursor_left()
            else:
                buffer.insert_text(inc_or_dec)
            # if inc_or_dec=='+':
            #     print("ewfoijfdsijoijowfijofejio")
            #     if before.endswith('+') and after and after[0] in '\'"':
            #         buffer.cursor_left()
    inc_dec('+')
    inc_dec('-')

    # @handle("h")
    # def sploo(x):
    #     print("A")
    # @handle("h")
    # def sploo(x):
    #     print("B")


    bracket_pairs={"()","[]","{}"}
    def thing(begin,end):
        @handle(begin)
        def _(event):# Parenthesis completion
            buffer=event.cli.current_buffer
            if not surround(buffer,begin,end):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                buffer.insert_text(begin)
                if not after or after[0].isspace() or before and before[-1]+after[0]in bracket_pairs or document.find_matching_bracket_position()!=0:
                    buffer.insert_text(end)
                    buffer.cursor_left(count=1)
        @handle(end)
        def _(event):# Parenthesis completion
            buffer=event.cli.current_buffer
            if not surround(buffer,begin,end):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                if not after or after[0]!=end:#  or before.count(begin)>before.count(end):#Last part is checking for parenthesis matches. I know somewhere there's a way to do this already thats better and isnt confused by strings but idk where that is
                    buffer.insert_text(end)
                else:
                    buffer.cursor_right(count=1)
    for bracket_pair in bracket_pairs:
        thing(bracket_pair[0],bracket_pair[1])

    def surround(buffer,begin,end):
        from rp.prompt_toolkit.selection import SelectionState
        document=buffer.document
        text=document.text
        selection_tuples=list(document.selection_ranges())
        for range in selection_tuples:
            buffer.document=Document(text=text[:range[0]]+begin+text[range[0]:range[1]+1]+end +text[range[1]+1:],cursor_position=range[0]+1,selection=None)
            buffer.document._selection=SelectionState(original_cursor_position=range[1]+1,type=document.selection.type)
        # exec(mini_terminal)
        # from rp.rp_ptpython.utils import get_jedi_script_from_document
        # script=get_jedi_script_from_document(document,r_iterm_comm.globa,r_iterm_comm.globa)
        # script.call_signatures()
        return bool(selection_tuples)# Returns whether we have a selection
    def thing2(char):
        @handle(char)
        def _(event,filter=has_selection):# Parenthesis completion
            buffer=event.cli.current_buffer
            if not surround(buffer,char,char):
                document=buffer.document
                before=document.text_before_cursor
                after= document.text_after_cursor
                before_line=document.current_line_before_cursor
                after_line=document.current_line_after_cursor

                if after.startswith(char) and not before.endswith(char):
                    buffer.cursor_right()
                # else:
                #     buffer.insert_text(char)
                #     buffer.cursor_left()
                #     buffer.insert_text(char)

                elif not after_line or not before and not after or before and after and before[-1]in'(=!#%&*+,-./:;<>^|~' and after[0]in')=!#%&*+,-./ :;<>^|~' or before and after and before[-1]+after[0] in 2*char:
                    buffer.insert_text(char)
                    buffer.cursor_left()
                    buffer.insert_text(char)
                else:
                    buffer.insert_text(char)

    for char in '"\'':
        thing2(char)

    # @handle(',')
    # def thing3(char):
    #     @handle(char)
    #     def _(event,filter=~has_selection):# Parenthesis completion
    #         buffer=event.cli.current_buffer
    #         document=buffer.document
    #         before=document.text_before_cursor
    #         after= document.text_after_cursor
    #         if before.endswith('(') and after.startswith(')'):
    #             buffer.cursor_right()
    #         buffer.insert_text(char)
    # for char in '!#%&*,./:;<>^|~':# + and - allready taken
    #     thing3(char)

    @handle(Keys.ControlSpace)# For commenting
    def _(event):  # Parenthesis completion
        # def toggle_comment_on_line(x):
        #     y=x.lstrip()
        #     if y.startswith("#"):# Line is commented out
        #         i=x.find('#')
        #         return x[:i]+x[i+1:]
        #     l=len(x)-len(y)
        #     return l*' ' +'#' + y
        buffer=event.cli.current_buffer
        # buffer.transform_current_line(toggle_comment_on_line)
        # buffer.insert_text("ⵁ")
        # buffer.delete_before_cursor
        document=buffer.document
        current_line=document.current_line
        before_line=document.current_line_before_cursor
        after_line=document.current_line_after_cursor
        buffer.cursor_left(10000)
        lstrip=current_line.lstrip()
        w=len(current_line)-len(lstrip)
        buffer.cursor_right(w)
        if lstrip.startswith('#'):
            buffer.delete()
        else:
            buffer.insert_text('#')
        buffer.cursor_down()
    #endregion

    @handle(Keys.ControlT,eager=True)
    def _(event):
        """
        Cursor to top.
        """
        event.cli.current_buffer.history_backward()
    @handle(Keys.ControlB,eager=True)
    def _(event):
        """
        Cursor to top.
        """
        event.cli.current_buffer.history_forward()

    @handle(Keys.ControlL)
    def _(event):
        """
        Clear whole screen and render again -- also when the sidebar is visible.
        """
        event.cli.renderer.clear()
    @handle(Keys.F2)
    def _(event):
        """
        Show/hide sidebar.
        """
        python_input.show_sidebar = not python_input.show_sidebar

    @handle(Keys.F3)
    def _(event):
        """
        Select from the history.
        """
        python_input.enter_history(event.cli)

    @handle(Keys.F4)
    def _(event):
        """
        Toggle between Vi and Emacs mode.
        """
        python_input.vi_mode = not python_input.vi_mode

    @handle(Keys.F6)
    def _(event):
        """
        Enable/Disable paste mode.
        """
        python_input.paste_mode = not python_input.paste_mode

    @handle(Keys.F1)
    def _(event):
        """
        Enable/Disable mouse mode.
        """
        python_input.enable_mouse_support = not python_input.enable_mouse_support

    @handle(Keys.Tab, filter= ~sidebar_visible & ~has_selection & TabShouldInsertWhitespaceFilter())
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        buffer=event.cli.current_buffer
        buffer.insert_text('    ')
        after_line = buffer.document.current_line_after_cursor
        if not after_line.lstrip():
            buffer.cursor_left(4)
    #region  Ryan Burgert Method
    @handle(Keys.BackTab,filter=IsMultiline())
    def _(event):
        """
        When tab should insert whitespace, do that instead of completion.
        """
        # from r import mini_terminal
        buffer=event.cli.current_buffer
        for whocares in range(4):
            try:
                if buffer.document.current_line.startswith(' ') or not has_selected_completion(buffer):
                    buffer.cursor_left()
                    buffer.transform_current_line(lambda x:x[1:])
                # buffer.transform_current_line(lambda x:(x[1:]if x.startswith(' '*4)else x.lstrip()))
                # buffer.transform_current_line(lambda x:(x[4:]if x.startswith(' '*4)else x.lstrip()))
            except:
                pass# Error migght happen if cursor is in bad place. Not sure what to do about that; but its an edge case so I'm just gonna squelch it.
        #endregion


    @handle(Keys.ControlJ, filter= ~sidebar_visible & ~has_selection &(ViInsertMode() | EmacsInsertMode()) &HasFocus(DEFAULT_BUFFER) & IsMultiline())
    def _(event):
        """
        Behaviour of the Enter key.

        Auto indent after newline/Enter.
        (When not in Vi navigaton mode, and when multiline is enabled.)
        """
        b = event.current_buffer
        empty_lines_required = python_input.accept_input_on_enter or 10000
        text = b.document.text_after_cursor
        current_line = b.document.current_line
        after_line = b.document.current_line_after_cursor
        before_line = b.document.current_line_before_cursor

        # if  (after_line.startswith('"""') and before_line.endswith ('"""')) or\
        #     (after_line.startswith("'''") and before_line.endswith ("'''")):
        #     print("ASOID")
        #     b.insert_text('\n')
        #     return
        def at_the_end(b):
            """ we consider the cursor at the end when there is no text after
            the cursor, or only whitespace. """
            assert isinstance(b,Buffer)
            text = b.document.text_after_cursor
            current_line = b.document.current_line
            after_line = b.document.current_line_after_cursor
            before_line = b.document.current_line_before_cursor
            #region RYAN BURGERT STUFF
            assert isinstance(text,str)
            def beginswithany(a,*b):
                for x in b:
                    if a.startswith(x):
                        return True
                return False
            line_before_cursor=b.document.current_line_before_cursor
            if line_before_cursor.lstrip() and not beginswithany(line_before_cursor[::-1],' ',',',':',';','{','[','"""',"'''") and not '"""' in line_before_cursor and not "'''" in line_before_cursor and '(' in line_before_cursor or beginswithany(line_before_cursor,'for ','def ','lambda ','while ','with ','if ','except ','try ') or not text or text.split('\n')[0] in ["):",']',')','}',':']:# Presumably at the end of def( a,b,c,d,e^): where ^ is cursor
                event.cli.current_buffer.cursor_right(1000000)# Move cursor to end of line then proceed as normal
                text = b.document.text_after_cursor
            #endregion

            return text == '' or (text.isspace() and not '\n' in text)

        # if at_the_end(b):# TODO Stuff here
            # print("""def a b c d e (enter)
# ->
# def a(b,c,d,e):
# """)
        if python_input.paste_mode:
            # In paste mode, always insert text.
            b.insert_text('\n')

        elif at_the_end(b) and b.document.text.replace(' ', '').endswith('\n' * (empty_lines_required - 1)):
            if b.validate():
                # When the cursor is at the end, and we have an empty line:
                # drop the empty lines, but return the value.
                b.document = Document(
                    text=b.text.rstrip(),
                    cursor_position=len(b.text.rstrip()))

                b.accept_action.validate_and_handle(event.cli, b)
        else:
            auto_newline(b)

    @handle(Keys.ControlD, filter=~sidebar_visible & Condition(lambda cli:
            # Only when the `confirm_exit` flag is set.
            python_input.confirm_exit and
            # And the current buffer is empty.
            cli.current_buffer_name == DEFAULT_BUFFER and
            not cli.current_buffer.text))
    def _(event):
        """
        Override Control-D exit, to ask for confirmation.
        """
        python_input.show_exit_confirmation = True

    return registry


def load_sidebar_bindings(python_input):
    """
    Load bindings for the navigation in the sidebar.
    """
    registry = Registry()

    handle = registry.add_binding
    sidebar_visible = Condition(lambda cli: python_input.show_sidebar)

    @handle(Keys.Up, filter=sidebar_visible)
    @handle(Keys.ControlP, filter=sidebar_visible)
    @handle('k', filter=sidebar_visible)
    def _(event):
        " Go to previous option. "
        python_input.selected_option_index = (
            (python_input.selected_option_index - 1) % python_input.option_count)

    @handle(Keys.Down, filter=sidebar_visible)
    @handle(Keys.ControlN, filter=sidebar_visible)
    @handle('j', filter=sidebar_visible)
    def _(event):
        " Go to next option. "
        python_input.selected_option_index = (
            (python_input.selected_option_index + 1) % python_input.option_count)

    @handle(Keys.Right, filter=sidebar_visible)
    @handle('l', filter=sidebar_visible)
    @handle(' ', filter=sidebar_visible)
    def _(event):
        " Select next value for current option. "
        option = python_input.selected_option
        option.activate_next()

    @handle(Keys.Left, filter=sidebar_visible)
    @handle('h', filter=sidebar_visible)
    def _(event):
        " Select previous value for current option. "
        option = python_input.selected_option
        option.activate_previous()

    @handle(Keys.ControlC, filter=sidebar_visible)
    @handle(Keys.ControlG, filter=sidebar_visible)
    @handle(Keys.ControlD, filter=sidebar_visible)
    @handle(Keys.ControlJ, filter=sidebar_visible)
    @handle(Keys.Escape, filter=sidebar_visible)
    def _(event):
        " Hide sidebar. "
        python_input.show_sidebar = False

    return registry


def load_confirm_exit_bindings(python_input):
    """
    Handle yes/no key presses when the exit confirmation is shown.
    """
    registry = Registry()

    handle = registry.add_binding
    confirmation_visible = Condition(lambda cli: python_input.show_exit_confirmation)

    @handle('y', filter=confirmation_visible)
    @handle('Y', filter=confirmation_visible)
    @handle(Keys.ControlJ, filter=confirmation_visible)
    @handle(Keys.ControlD, filter=confirmation_visible)
    def _(event):
        """
        Really quit.
        """
        event.cli.exit()

    @handle(Keys.Any, filter=confirmation_visible)
    def _(event):
        """
        Cancel exit.
        """
        python_input.show_exit_confirmation = False

    return registry
diddly=0

def auto_newline(buffer):
    r"""
    Insert \n at the cursor position. Also add necessary padding.
    """
    insert_text = buffer.insert_text

    if buffer.document.current_line_after_cursor:
        # When we are in the middle of a line. Always insert a newline.
        insert_text('\n')
    else:
        # Go to new line, but also add indentation.
        current_line = buffer.document.current_line_before_cursor.rstrip()
        insert_text('\n')

        # Unident if the last line ends with 'pass', remove four spaces.
        unindent = current_line.rstrip().endswith(' pass')

        # Copy whitespace from current line
        current_line2 = current_line[4:] if unindent else current_line

        for c in current_line2:
            if c.isspace():
                insert_text(c)
            else:
                break

        # If the last line ends with a colon, add four extra spaces.
        if current_line[-1:] == ':':
            for x in range(4):
                insert_text(' ')

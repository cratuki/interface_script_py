# At the time of writing, this is not used in the project. But it would be
# useful to someone who needed to do a fast port of this library to another
# language platform. (In python, you can use shlex.shlex for this, which is
# what I am doing in the library.)

def parse_line_to_tokens(line):
    '''
    Tokenises a line.
    
    Respects quotation mark boundaries that indicate strings containing
    spaces, or escapted quotation marks.

    Respects comments, denoted by a hash symbol that is not inside of a quoted
    block.
    '''
    tokens = []
    acc = []
    def esc_append(c):
        if c == '\n':
            pass
        else:
            acc.append(c)
    mode_normal   = 0
    mode_squotes  = 1
    mode_dquotes  = 2
    mode_escape_n = 3 # escape, normal mode
    mode_escape_s = 4 # escape, single-quote mode
    mode_escape_d = 5 # escape, double-quote mode
    var_mode = [mode_normal]
    def set_mode(m):
        var_mode[0] = m
    def mode():
        return var_mode[0]
    def spin(force=False):
        s = ''.join(acc).strip()
        if force or s: tokens.append(s)
        while acc: acc.pop()
        var_mode[0] = mode_normal
    for c in line.strip():
        if mode() == mode_escape_n:
            esc_append(c)
            set_mode(mode_normal)
        elif mode() == mode_escape_s:
            esc_append(c)
            set_mode(mode_squotes)
        elif mode() == mode_escape_d:
            esc_append(c)
            set_mode(mode_dquotes)
        elif mode() == mode_normal:
            if c == '\\':
                set_mode(mode_escape_n)
            elif c == ' ':
                # end of word
                spin()
            elif c == '#':
                # comment
                spin()
                break
            elif c == '"':
                # enter double quotes
                spin()
                set_mode(mode_dquotes)
            elif c == "'":
                # enter single quotes
                spin()
                set_mode(mode_squotes)
            else:
                acc.append(c)
        elif mode() == mode_squotes:
            if c == '\\':
                set_mode(mode_escape_s)
            elif c == "'":
                # exit single quotes
                spin(True)
            else:
                acc.append(c)
        elif mode() == mode_dquotes:
            if c == '\\':
                set_mode(mode_escape_d)
            elif c == '"':
                # exit double quotes
                spin(True)
            else:
                acc.append(c)
        else:
            raise Exception('Should not get here [%s]'%mode())
    if mode() != mode_normal:
        raise Exception("invalid line. [%s]"%(line))
    spin()
    return tokens

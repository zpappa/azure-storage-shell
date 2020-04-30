import curses

# get the curses screen window
screen = curses.initscr()

# turn off input echoing
curses.noecho()

# respond to keys immediately (don't wait for enter)
curses.cbreak()

# map arrow keys to special values
screen.keypad(True)

try:
    while True:
        char = screen.getch()
        screen.addstr("azss:>")
        if char == curses.KEY_RIGHT:
            # print doesn't work with curses, use addstr instead
            screen.addstr(0, 6, 'right')
        elif char == curses.KEY_LEFT:
            screen.addstr(0, 6, 'left ')
        elif char == curses.KEY_UP:
            screen.addstr(0, 6, 'up   ')
        elif char == curses.KEY_DOWN:
            screen.addstr(0, 6, 'down ')
        elif isinstance(chr(char), str):
            screen.addstr(0, 6, chr(char))
finally:
    # shut down cleanly
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

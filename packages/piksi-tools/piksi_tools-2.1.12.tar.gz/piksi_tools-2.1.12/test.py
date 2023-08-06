
buf = "This is my test buffer \nThis is the second line. \n This is the last line \n"
def scrollback_write(bufin,s):
    prior_line_beginning = bufin.rfind('\n', 0, bufin.rfind('\n')) # get last line
    print len(bufin)
    print prior_line_beginning
    return bufin[:prior_line_beginning] + '\n' + s + '\n'

print buf
a = scrollback_write(buf, "Replacement line for last line #1")
a += "added a lines # 1 \n"
a += "added a lines # 2 \n"
print "about to print a with added another line"
print scrollback_write(a, "Replacement line for last line #2")
#print buf



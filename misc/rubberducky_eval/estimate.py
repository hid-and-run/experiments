import sys
import os

def parse_script(fn):
    try:
        script = open(fn).read().strip().split("\n")
    except:
        return -1
    count = 0
    idx = 0
    wrong_mode = False
    feedback_required = False
    while idx < len(script):
        s = script[idx].strip()
        try:
            cmd = s.split(" ")[0]
        except:
            idx += 1
            continue
        if cmd == "STRING" or cmd == "STRINGLN":
            if len(s.strip()) == len(cmd.strip()):
                idx += 1
                while idx < len(script) and cmd != "END_STRING":
                    s = script[idx]
                    try:
                        cmd = s.split(" ")[0]
                    except:
                        idx += 1
                        continue
                    
                    count += len(s)
                    idx += 1
            else:
                count += len(s) - len(cmd)
        if cmd == "GUI" or cmd == "WINDOWS":
            count += len(s) - len(cmd)
        if cmd == "TAB" or cmd == "ENTER" or cmd == "UP" or cmd == "DOWN" or cmd == "LEFT" or cmd == "RIGHT" or cmd == "UPARROW" or cmd == "DOWNARROW" or cmd == "LEFTARROW" or cmd == "RIGHTARROW" or cmd == "PAGEUP" or cmd == "PAGEDOWN" or cmd == "HOME" or cmd == "END" or cmd == "INSERT" or cmd == "DELETE" or cmd == "DEL" or cmd == "BACKSPACE" or cmd == "TAB" or cmd == "SPACE" or cmd == "ESCAPE" or cmd == "F1" or cmd == "F2" or cmd == "F3" or cmd == "F4" or cmd == "F5" or cmd == "F6" or cmd == "F7" or cmd == "F8" or cmd == "F9" or cmd == "F10" or cmd == "F11" or cmd == "F12":
            count += 1
        if cmd == "CTRL" or cmd == "CONTROL" or cmd == "COMMAND" or cmd == "SHIFT" or cmd == "ALT":
            count += len(s.split(" "))
            
        if s == "ATTACKMODE STORAGE":
            wrong_mode = True
        
        if "$_CAPSLOCK_ON" in s or "$_NUMLOCK_ON" in s or "$_SCROLLLOCK_ON" in s:
            feedback_required = True
        
        idx += 1
        
    if wrong_mode or feedback_required:
        return -1
    return count


mypath = "."
files = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(mypath) for f in filenames]


to_parse = []
for f in files:
    if "payload" in f:
        to_parse.append(f)
    if "." not in f:
        to_parse.append(f)
        
lens = []
details = []
cnt = 0
for s in to_parse:
    if "/prank" in s or "/mobile" in s:
        continue
    #print(to_parse)
    l = parse_script(s)
    #print("%s: %d" % (s, l))
    if l != 0:
        cnt += 1
    if l > 0:
        lens.append(l)
        details.append((l, s))
    
for s in sorted(details):
    print("%5d      %s" % (s[0], s[1]))
print("")

print("Avg: %d, min: %d" % (sum(lens) / len(lens), min(lens)))

if len(sys.argv) >= 2:
    ml = int(sys.argv[1])
    works = 0
    noworks = 0
    for l in lens:
        if l <= ml:
            works += 1
        else:
            noworks += 1
    print("<= %d: %d / %d (~ %.2f%%)" % (ml, works, cnt, 100.0 * works / cnt))

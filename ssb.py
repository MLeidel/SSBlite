# ssb.py
# Lite_Site Specific Browser
#   with minimal menu based navigation.

# CAUTION: MANY NORMAL BROWSER FEATURES MISSING !!!
# (LIKE: tabs, cookies, sessions, page-search, right-click menu, downloads, and more)

# based on pywebview 4.0.2 & Python 3..
# Use:
# $ python3 ssb.py {title | "no"} {app URL}
#   "no" means the URL will be in the window caption
#   otherwise title will be in the window caption

import sys, os
import webview
import webview.menu as wm

# initialize window metrics
top = 50
left = 50
win_width = 600
win_height = 600
lst = []

if len(sys.argv) < 3:
    print("Missing args: {title | \"no\"} {URL}")
    sys.exit()

URL = sys.argv[2]
TITLE = sys.argv[1]

# change working directory to path of program
p = os.path.realpath(__file__)
os.chdir(os.path.dirname(p))

# read windows metrics
with open('ssb_winfo', 'r') as f:
    line = f.readline().strip()
    lst = line.split(',')
    lst = [int(num) for num in lst]
    top = lst[0]
    left = lst[1]
    win_width = lst[2]
    win_height = lst[3]

# ---------------------------------------------------------------

def on_closed():
    ''' write window metrics '''
    global top, left, win_width, win_height
    with open("ssb_winfo", "w") as f:
        f.write(",".join( (str(top),
                           str(left),
                           str(win_width),
                           str(win_height)
                          )))

def on_loaded():
    ''' Put the page URL in the title for every new page '''
    active_window = webview.active_window()
    if TITLE != "no":
        return
    else:
        if active_window:
            active_window.set_title(active_window.get_current_url())
    # active_window.get_cookies()

def home_ssb():
    win.load_url(URL)

def back_ssb():
    # win.evaluate_js("history.back()")
    active_window = webview.active_window()
    if active_window:
        active_window.evaluate_js("history.back()")

def forward_ssb():
    win.evaluate_js("history.forward()")

def reload_ssb():
     win.evaluate_js("location.reload()")

def exit_ssb():
    win.destroy()

def search_ssb():
    ''' new search text or URL '''
    js = '''
    let txt = prompt("Enter URL or Search Prompt", "")
    if (txt != null) {
        if (txt.startsWith("http")) {
            location = txt;
        } else {
            location = "https://search.google.com/search?q=" + txt;
        }
    }
    '''
    active_window = webview.active_window()
    if active_window:
        active_window.evaluate_js(js)

def on_resized():
    global top, left, win_width, win_height
    left, top = win.x, win.y
    win_width, win_height = win.width, win.height


# create browser window with title and url
win = webview.create_window(TITLE,
                            url=URL,
                            width=win_width,
                            height=win_height,
                            x=left,
                            y=top)
win.events.resized += on_resized
win.events.loaded += on_loaded
win.events.closed += on_closed


menu_items = [
    wm.Menu(
        '«=»',
        [
            wm.MenuAction('Back', back_ssb),
            wm.MenuAction('Forward', forward_ssb),
            wm.MenuAction('Search or URL', search_ssb),
            wm.MenuAction('Home', home_ssb),
            wm.MenuAction('Reload', reload_ssb),
            wm.MenuAction('Exit', exit_ssb),
        ],
    )
]

webview.start(menu=menu_items)

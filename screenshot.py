import os
from subprocess import Popen, PIPE
from selenium import webdriver

abspath = lambda *p: os.path.abspath(os.path.join(*p))
ROOT = abspath(os.path.dirname(__file__))

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE).stdout.read()
    if len(result) > 0 and not result.isspace():
        raise Exception(result)


def do_screen_capturing(url, screen_path, width, height):
    print "Capturing screen.."
    driver = webdriver.PhantomJS()
    # it save service log file in same directory
    # if you want to have log file stored else where
    # initialize the webdriver.PhantomJS() as
    # driver = webdriver.PhantomJS(service_log_path='/var/log/phantomjs/ghostdriver.log')
    driver.set_script_timeout(30)
    if width and height:
        driver.set_window_size(width, height)
    driver.get(url)
    driver.execute_script("$('.follow-bar').hide()")
    driver.execute_script("$('.permalink-tweet-container .content .dropdown').hide()")
    driver.execute_script("$('.permalink-tweet-container .tweet-stats-container').hide()")
    driver.execute_script("$('.permalink-tweet-container .stream-item-footer').hide()")
    
    driver.save_screenshot(screen_path)

    element = driver.find_element_by_class_name('permalink-tweet-container')
    location = element.location
    size = element.size

    return size, location


def do_crop(params):
    print "Croping captured image.."
    command = [
        'mogrify',
        '-crop', '%sx%s+%s+%s' % (params['width'], params['height'], params['x'], params['y']),
        params['screen_path']
    ]
    execute_command(' '.join(command))

def get_screen_shot(**kwargs):
    url = kwargs['url']
    
    filename = kwargs.get('filename', 'screen.png') # file name e.g. screen.png
    path = kwargs.get('path', ROOT) # directory path to store screen
    screen_path = abspath(path, filename)

    size, location = do_screen_capturing(url, screen_path, 1024, 768)

    params = {
        'width': size['width'], 'height': size['height'],
        'x': location['x'], 'y': location['y'],
        'screen_path': screen_path}
    do_crop(params)

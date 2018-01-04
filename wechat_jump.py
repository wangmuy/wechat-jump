import subprocess
import math
import time
import cv2 as cv
import numpy as np

def adb_cmd(cmd):
    try:
        subprocess.check_call("adb "+cmd, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print("error:", e)
    return False

def adb_shell(cmd):
    return adb_cmd("shell "+cmd)

def press(x, y):
    print("press: ", x, y)
    return adb_shell("input touchscreen tap "+str(x)+" "+str(y))

def long_press(millis):
    print "long_press", millis
    return adb_shell("input touchscreen swipe 540 960 540 960 "+str(millis))

def get_screencap():
    ret = False
    filename = None
    defname = "wechat-jump-sc.png"
    ret = adb_shell("screencap -p /data/local/tmp/"+defname)
    if(ret == False):
        return ret,filename
    ret = adb_cmd("pull /data/local/tmp/"+defname)
    if(ret == False):
        return ret, filename
    filename = defname
    return ret, filename

def find_pattern(img, pattern, threshold):
    res = cv.matchTemplate(img, pattern, cv.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    pt_dict = zip(*loc[::-1])
    return pt_dict

def find_pattern_max(img, pattern, method=cv.TM_CCOEFF_NORMED):
    try:
        res = cv.matchTemplate(img, pattern, method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        confidence = max_val
    except Exception as e:
        # print("Exception: ", e)
        top_left = (0,0)
        confidence = 0.0
    return top_left, confidence
    
    
def imread(filename):
    img = cv.imread(filename)
    return img
    
def imtransform(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    canny = cv.Canny(gray, 10, 30)
    del img
    del gray
    return canny

class Pattern:
    filename = None
    img = None
    w = 0
    h = 0

    def __init__(self, filename, isTransform=True):
        self.filename = filename
        if isTransform == True:
            self.img = imtransform(imread(filename))
        else:
            self.img = imread(filename)
        self.h, self.w = self.img.shape[:2]


# global vars
droid = Pattern("wechat_jump_body.png", isTransform=False)
ui_ret = Pattern("wechat_jump_return.png", isTransform=False)
ui_retry = Pattern("wechat_jump_retry.png", isTransform=False)

def jump_alg_top_edge(screencap):
    """ return: jumped?
    """
    global droid
    droid_h, droid_w = droid.h, droid.w
    
    # find droid
    droid_topleft, _ = find_pattern_max(screencap, droid.img)
    droid_loc = (droid_topleft[0]+droid_w/2.0, droid_topleft[1]+droid_h*1.0)
    print("droid loc=", droid_loc[0], droid_loc[1])

    # transform screencap
    screencap_orig = screencap
    screencap = imtransform(screencap)
    
    # get edge top y coord
    border_top_y = 500
    max_i = None
    for i in screencap[border_top_y:]:
        if np.max(i):
            print("### border_top_y=", border_top_y)
            max_i = i
            break
        border_top_y += 1
    border_top_x = np.argmax(max_i)
    
    offset = 90
    found_ptrn_loc = (border_top_x, border_top_y+offset)
    ptrn_topleft = (found_ptrn_loc[0]-25, found_ptrn_loc[1]-25)
    found_ptrn_w = 50
    found_ptrn_h = 50
    
    cv.rectangle(screencap_orig, droid_topleft, (droid_topleft[0]+droid_w, droid_topleft[1]+droid_h), (0,255,0), 10)
    cv.rectangle(screencap_orig, tuple(ptrn_topleft), (ptrn_topleft[0]+found_ptrn_w, ptrn_topleft[1]+found_ptrn_h), (0,0,255), 20)
    cv.imwrite("wechat-jump-ptrn_rec.png", screencap_orig)
    cv.imwrite("wechat-jump-sc-crop.png", screencap)
    
    dist = math.sqrt(
        (found_ptrn_loc[0]-droid_loc[0])**2 + (found_ptrn_loc[1]-droid_loc[1])**2)

    time = int(dist*1.35)
    dir = "no_care"
    print("found_ptrn_rectangle=", ptrn_topleft, (ptrn_topleft[0]+found_ptrn_w, ptrn_topleft[1]+found_ptrn_h),
        "found_ptrn_loc=", found_ptrn_loc, ", dist=", dist, "dir=", dir, ", time=", time)
    
    long_press(time)
    return True

def jump_alg_pattern_match(screencap):
    """return: jumped?
    """
    global droid
    droid_h, droid_w = droid.h, droid.w

    ptrn_files = [
        "wechat-ptrn_01.png", "wechat-ptrn_02.png", "wechat-ptrn_03.png",
        "wechat-ptrn_04.png", "wechat-ptrn_05.png", "wechat-ptrn_06.png",
        "wechat-ptrn_07.png", "wechat-ptrn_08.png", "wechat-ptrn_09.png",
        "wechat-ptrn_10.png", "wechat-ptrn_11.png", "wechat-ptrn_12.png",
        "wechat-ptrn_13.png", "wechat-ptrn_14.png", "wechat-ptrn_15.png",
        "wechat-ptrn_16.png", "wechat-ptrn_17.png", "wechat-ptrn_18.png",
        "wechat-ptrn_19.png", "wechat-ptrn_20.png", "wechat-ptrn_21.png",
        "wechat-ptrn_22.png", "wechat-ptrn_23.png", "wechat-ptrn_24.png",
        "wechat-ptrn_25.png", "wechat-ptrn_26.png", "wechat-ptrn_27.png",
        "wechat-ptrn_28.png", "wechat-ptrn_29.png", "wechat-ptrn_30.png",
        "wechat-ptrn_31.png", "wechat-ptrn_32.png", "wechat-ptrn_33.png",
        "wechat-ptrn_34.png", "wechat-ptrn_35.png", "wechat-ptrn_36.png",
        "wechat-ptrn_37.png", "wechat-ptrn_38.png", "wechat-ptrn_39.png",
        "wechat-ptrn_40.png", "wechat-ptrn_41.png", "wechat-ptrn_42.png",
        "wechat-ptrn_43.png", "wechat-ptrn_44.png", "wechat-ptrn_45.png",
        "wechat-ptrn_46.png", "wechat-ptrn_47.png", "wechat-ptrn_48.png",
        "wechat-ptrn_49.png", "wechat-ptrn_50.png", "wechat-ptrn_51.png",
        "wechat-ptrn_52.png", "wechat-ptrn_53.png", "wechat-ptrn_54.png",
        "wechat-ptrn_55.png", "wechat-ptrn_56.png", "wechat-ptrn_57.png",
        "wechat-ptrn_58.png",
    ]
    ptrn_list = []
    for f in ptrn_files:
        ptrn = Pattern(f)
        ptrn_list.append(ptrn)
        
    # find droid
    droid_topleft, _ = find_pattern_max(screencap, droid.img)
    droid_loc = (droid_topleft[0]+droid_w/2.0, droid_topleft[1]+droid_h*1.0)
    print("droid loc=", droid_loc[0], droid_loc[1])

    # crop screencap and to gray
    screencap_orig = screencap
    screencap = screencap[0:int(droid_loc[1])+50, 0:1080]
    screencap = imtransform(screencap)

    # find pattrn
    found_ptrn = None
    found_ptrn_loc = None
    topleft_list = []
    confidence_list = []
    conf_max = 0
    conf_max_idx = None
    for i, ptrn in enumerate(ptrn_list):
        ptrn_topleft, confidence = find_pattern_max(screencap, ptrn.img)
        topleft_list.append(ptrn_topleft)
        confidence_list.append(confidence)
        if confidence > conf_max:
            conf_max_idx = i
            conf_max = confidence

    found_ptrn = ptrn_list[conf_max_idx]
    ptrn_topleft = list(topleft_list[conf_max_idx])
    ptrn_topleft[1] += border_y_top

    ptrn_loc = (ptrn_topleft[0]+found_ptrn.w/2.0, ptrn_topleft[1]+found_ptrn.h/2.0)
    print("found_ptrn=", ptrn.filename, ", loc=", ptrn_loc[0], ptrn_loc[1], "confidence=", conf_max)
    found_ptrn_loc = ptrn_loc

    cv.rectangle(screencap_orig, droid_topleft, (droid_topleft[0]+droid_w, droid_topleft[1]+droid_h), (0,255,0), 10)
    cv.rectangle(screencap_orig, tuple(ptrn_topleft), (ptrn_topleft[0]+found_ptrn_w, ptrn_topleft[1]+found_ptrn_h), (0,0,255), 20)
    cv.imwrite("wechat-jump-ptrn_rec.png", screencap_orig)
    cv.imwrite("wechat-jump-ptrn.png", found_ptrn.img)
    cv.imwrite("wechat-jump-sc-crop.png", screencap)
    dist = math.sqrt(
        (found_ptrn_loc[0]-droid_loc[0])**2 + (found_ptrn_loc[1]-droid_loc[1])**2)

    if found_ptrn_loc[0] < droid_loc[0]:
        dir = "left"
        time = int(dist*1.3)
    else:
        dir = "right"
        time = int(dist*1.4)
    found_ptrn_w = found_ptrn.w
    found_ptrn_h = found_ptrn.h
    print("found_ptrn_rectangle=", ptrn_topleft, (ptrn_topleft[0]+found_ptrn_w, ptrn_topleft[1]+found_ptrn_h),
        "found_ptrn_loc=", found_ptrn_loc, ", dist=", dist, "dir=", dir, ", time=", time)
    
    if conf_max > 0:
        long_press(time)
        return True
    else:
        print("confidence too low, quit")
    return False

def jump():
    global droid
    global ui_ret
    global ui_retry
    droid_h, droid_w = droid.h, droid.w

    # screencap
    ret, filename = get_screencap()
    if(ret == False):
        print("screencap failed")
        return False
    screencap = imread(filename)
    
    # return?
    rb_h, rb_w = ui_ret.h, ui_ret.w
    rb_topleft, rb_confidence = find_pattern_max(screencap, ui_ret.img)
    print("find return?", rb_topleft, rb_h, rb_w, rb_confidence)
    if rb_confidence > 0.8:
        print(">>> RETURN press...")
        press(int(rb_topleft[0]+rb_w/2.0), int(rb_topleft[1]+rb_h/2.0))
        return True

    # retry?
    retry_h, retry_w = ui_retry.h, ui_retry.w
    retry_topleft, retry_confidence = find_pattern_max(screencap, ui_retry.img)
    print("find retry?", retry_topleft, retry_h, retry_w, retry_confidence)
    if retry_confidence > 0.8:
        print(">>> RETRY press...")
        press(int(retry_topleft[0]+retry_w/2.0), int(retry_topleft[1]+retry_h/2.0))
        return True

    return jump_alg_top_edge(screencap)

def auto_jump():
    count = 1
    while True:
        print(">>>>>  JUMP #", count)
        ret = jump()
        if ret == False:
            break
        count += 1
        time.sleep(1.5)
        

if __name__ == '__main__':
    auto_jump()
    #jump()

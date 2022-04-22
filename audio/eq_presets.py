active_set = []

def apply_vintage(slider_list):
    global active_set
    preset = [-4,-3,-1,0,0,0,0,0,+1,+1,+2,0,0,0,0,0,0,0]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset


def apply_eguitar(slider_list):
    global active_set
    preset = [-8, -5, -2, -1, 0, 0, 0, 0, -1, -1, -2, 0, 0, 0, 1, 2, 4, -1]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset

def apply_aguitar(slider_list):
    global active_set
    preset = [-12, -6, -3, -2, -1, 0, 0, 0, -1, -1.5, -2, 0, 0, 1, 2, 2, 4, -1]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset

def apply_piano(slider_list):
    global active_set
    preset = [+3, +2, +1, +0.5, 0, 0, 0, 1, 2, 3, 2, 1, 0, 0, -1, -1, -2, -4]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset

def apply_vocals(slider_list):
    global active_set
    preset = [-3, -2, -1, -0.5, 0, 0, 0, 1, 1, 2, 3, 2, 0, 1, 2, 4, 4, +1]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset


def apply_bassy(slider_list):
    global active_set
    preset = [+12, +8, +5, +3, +2, +0.5, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -4, -8]
    index_count = 0
    for slider in slider_list:
        slider.set(-preset[index_count])
        index_count += 1
    active_set = preset
from tkinter.font import Font


# Program info
window_title = "Sallust"
version = 0.12
screen_height = 1000
screen_width = 500
# Colors
light_color = "#3c4b5c"
selected_button_color = "#21293c"
button_color = "#303e58"
medium_color = "#303e58"
dark_color = "#21293c"
text_color = "white"
dark_red_color = "#6f2121"
red_color = "#922e2e"
light_red_color = "#bd3838"
green_color = "#22863a"
light_green_color = "#2cb44d"
ultra_light_color = "#5c7490"
white = "#ffffff"
blue_color = "#0b5cb5"
code_character_color = "#e7791e"
string_character_color = "#94ce15"
error_line = "#6b3329"
purple = "#15ceb6"

# IMAGES
image_icon = None
image_fail = None
image_ok = None
image_skip = None
image_ok_test = None
image_fail_test = None
image_run_test = None
image_run = None
image_running = None
image_save = None
image_xml = None
image_load = None
image_collapse = None
image_collapse_off = None
image_hide_ok = None
image_hide_error = None
image_hide_ok_off = None
image_hide_error_off = None
icon = None
steps_icon = None
graphs_icon = None
current_xml = None


# Fonts


def title_font():
    return Font(family="Verdana", size=12,)


def text_font(size=12, weight="normal", family="Verdana"):
    return Font(family=family, size=size, weight=weight)

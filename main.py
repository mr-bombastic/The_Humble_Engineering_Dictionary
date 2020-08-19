from tkinter import *
import time
from threading import Thread
from PIL import Image
import tkinter.font as tkfont
from tkinter import messagebox
from tkinter import simpledialog
from Classes.logic import Logic
from Classes.variable import Variable
from Classes.constant import Constant
from Classes.equation import Equation
from Classes.method import Method
from matplotlib import *
from matplotlib import figure

use('TkAgg')    # something for matplotlib to display equations, not quite sure what it does

# colors and other variables
color_dark = "#2b2b2b"          # background color
color_mid = "#383838"           # button background color
color_light = "#404040"         # frame color
color_highlight = "#214283"     # highlight text color
accent_dark = "#323232"         # accent color dark
accent_light = '#949596'        # accent color light
text_color = "#eaeaea"          # color for text
relief_style = 'flat'           # type of relief (flat, groove, raised, ridge, solid, sunken)

spacing_out_x = 10
spacing_out_y = 5
spacing_in = 2
fontsize = 11
left_side_thickness = 400
right_side_thickness = 150

# stuff that transcends various dimensions
previously_altered_widgets = []
step_num = 0
search_results = []  # create an array of the results

# main window stuff
window = Tk()  # creates the window
window.title("My Engineering Glossary")
window.state('normal')  # "zoomed" for full screen
window.configure(background=color_dark)

# set default font size
default_font = tkfont.Font(size=fontsize)
window.option_add("*Font", default_font)

# measure the length of m to get an idea of the number of pixels a character is
m_len = default_font.measure('m')

# set these items default font style and size
window.option_add("*Labelframe.Font", "Arial " + str(fontsize) + " bold italic")

# sets the default colors for various activities
window.tk_setPalette(background=color_light, foreground=text_color, activeBackground=color_dark,
                     activeForeground=text_color, selectColor=color_dark)

# set these items default background to color_mid
window.option_add("*Button.Background", color_mid)
window.option_add("*Radiobutton.Background", color_mid)
window.option_add("*Canvas.Background", color_mid)
window.option_add("*Canvas.highlightBackground", color_mid)
window.option_add("*Canvas.highlightColor", color_mid)
window.option_add("*Text.Background", color_mid)
window.option_add("*Text.selectBackground", color_highlight)
window.option_add("*Text.selectForeground", text_color)
window.option_add("*Entry.Background", color_mid)
window.option_add("*Entry.readonlyBackground", color_light)
window.option_add("*Entry.selectBackground", color_highlight)
window.option_add("*Entry.selectForeground", text_color)

window.option_add("*Label.Anchor", "w")  # default label anchor

window.option_add("*relief", 'flat')
window.option_add("*Button.relief", 'ridge')
window.option_add("*selectBorderwidth", 0)
window.option_add("*highlightthickness", 1)
window.option_add("*Canvas.highlightthickness", 0)
window.option_add("*Text.highlightthickness", 0)
window.option_add("*Listbox.highlightthickness", 0)

window.option_add("*Text.Wrap", "word")
window.option_add("*Text.width", 30)
window.option_add("*Text.height", 5)


# this stuff is for sorting out the resizing of the right column and lower row
window.grid_columnconfigure(1, weight=1)
window.grid_rowconfigure(1, weight=1)

# items for the checkboxes, will save 0 or 1 if it has not or has been checked
search_variables = IntVar(value=1)
search_constants = IntVar(value=1)
search_equations = IntVar(value=1)
search_logic = IntVar(value=1)
search_methods = IntVar(value=1)
search_names = IntVar(value=1)
search_description = IntVar(value=1)
search_symbol = IntVar(value=1)
search_value = IntVar(value=1)
search_units = IntVar(value=1)
search_field = IntVar(value=1)
item_type_to_add_or_edit = StringVar()  # this is for adding/editing items. Let it be
field_selected = StringVar()  # create the item type in this fancy way I don't understand


# used to alert the user of their actions and asks them if they want to continue or not
def alert_user(display_string, get_input):
    if get_input:
        return messagebox.askyesno(title="Warning", message=str(display_string))
    else:
        messagebox.showinfo(title="Warning", message=str(display_string))


# print every saved item that is selected in the checkboxes
def print_all():
    destroy_all_result_stuff()  # will delete all the old search results

    search_results.clear()  # removes all items from search results

    if search_variables.get() == 1:  # when the user whats to search through variables
        search_results.extend(string_to_item(get_file_lines("Dictionary/variables.txt"), "Variable"))
    if search_constants.get() == 1:  # when the user whats to search through constants
        search_results.extend(string_to_item(get_file_lines("Dictionary/constants.txt"), "Constant"))
    if search_equations.get() == 1:  # when the user whats to search through equations
        search_results.extend(string_to_item(get_file_lines("Dictionary/equations.txt"), "Equation"))
    if search_logic.get() == 1:  # when the user whats to search through logic
        search_results.extend(string_to_item(get_file_lines("Dictionary/logic.txt"), "Logic"))
    if search_methods.get() == 1:  # when the user whats to search through all_images
        search_results.extend(string_to_item(get_file_lines("Dictionary/methods.txt"), "Method"))

    Thread(target=print_results).start()


# Will search though the database and fill the array to ultimately have it printed
def search():
    destroy_all_result_stuff()  # will delete all the old search results

    if txt_search.get() != '':
        search_results.clear()  # removes all items from search results

        if search_variables.get() == 1:  # when the user whats to search through variables
            search_results.extend(string_to_item(get_file_lines("Dictionary/variables.txt"), "Variable"))
        if search_constants.get() == 1:  # when the user whats to search through constants
            search_results.extend(string_to_item(get_file_lines("Dictionary/constants.txt"), "Constant"))
        if search_equations.get() == 1:  # when the user whats to search through equations
            search_results.extend(string_to_item(get_file_lines("Dictionary/equations.txt"), "Equation"))
        if search_logic.get() == 1:  # when the user whats to search through logic
            search_results.extend(string_to_item(get_file_lines("Dictionary/logic.txt"), "Logic"))
        if search_methods.get() == 1:  # when the user whats to search through all_images
            search_results.extend(string_to_item(get_file_lines("Dictionary/methods.txt"), "Method"))

        search_in_list(txt_search.get(), search_results)

        # check to see if there are any results
        if search_results:
            Thread(target=print_results).start()
        else:  # if there are not results let the user know there was nothing found
            Label(frm_results_inner, text="No results fit your search criteria.\nPlease try different criteria.").grid()


# will use the given text to search through the search_results list and will weed out anything that doesn't match
def search_in_list(search_text, list_to_search):
    i = 0
    while i < len(list_to_search):
        remove = 0
        remove_value = 0

        # when the user whats to search through names
        if search_names.get() == 1:
            # if the users text is nowhere to be found. Just leave it be if its somewhere in there
            if search_text not in list_to_search[i].get_name():
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # when the user whats to search through descriptions
        if search_description.get() == 1:
            # if the users text is nowhere to be found. Just leave it be if its somewhere in there
            if search_text not in list_to_search[i].get_description():
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # checks to make sure one can search within these categories by checking to see what type of item it is
        if get_item_type(list_to_search[i]) == "Variable" or get_item_type(list_to_search[i]) == "Constant":
            # when the user whats to search through symbols
            if search_symbol.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_symbol():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

            # when the user whats to search through values
            if search_value.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_value():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

            # when the user whats to search through units
            if search_units.get() == 1:
                # if the users text is nowhere to be found. Just leave it be if its somewhere in there
                if search_text not in list_to_search[i].get_units():
                    remove += 1
                remove_value += 1  # incremented to understand the number of parameters that will be considered

            # when the user whats to search through items applicable field
            if search_field.get() == 1:
                pass

        # when searching though an equation one must also look into the variables/constants within
        elif get_item_type(list_to_search[i]) == "Equation":

            # get the list of variables/constants and search though them and save the result
            equ_search_list = search_in_list(search_text, list_to_search[i].get_all_variables())

            # if there is nothing in the resulting list then nothing relevant was found
            if len(equ_search_list) == 0:
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # when searching though a method one must also look into the steps within
        elif get_item_type(list_to_search[i]) == "Method":

            # get the list of steps and search though them and save the result
            equ_search_list = search_in_list(search_text, list_to_search[i].get_steps())

            # if there is nothing in the resulting list then nothing relevant was found
            if len(equ_search_list) == 0:
                remove += 1
            remove_value += 1  # incremented to understand the number of parameters that will be considered

        # checks to see if a search result should be removed
        if remove == remove_value:  # if the item has no relevance to the searched text and limiters
            del list_to_search[i]
        else:  # if it should stay
            i += 1

    return list_to_search


# destroys all previous search results to allow new ones to be printed. also deletes stored widgets
def destroy_all_result_stuff():
    # reset selected item to nothing
    global selected_item
    selected_item = ""

    btn_delete_item.configure(state="disabled")  # disable delete btn as it won't work correctly with nothing selected

    destroy_search_results()

    # required since the widgets in here no longer exist
    global previously_altered_widgets
    previously_altered_widgets = ""


# destroys all widgets in the search results frame
def destroy_search_results():
    for widget in frm_results_inner.winfo_children():
        widget.destroy()


# destroys anything that was in the display_info frame before
def destroy_item_info():
    for widget in frm_info_inner.winfo_children():
        widget.destroy()


# called when a search result is clicked to get the widget's row. From there display_info can display correct item
def callback_get_widget_row(event):
    global previously_altered_widgets  # required for the bit where this variable needs to be set to this

    caller = event.widget  # get the widget that corresponds to the event
    r = caller.grid_info()['row']  # get the row of the widget

    # if something was clicked before this will reset the colors so its not highlighted
    if previously_altered_widgets != "":
        for widget in previously_altered_widgets:
            if widget.winfo_class() != "Canvas":
                widget.configure(activebackground=color_mid, selectcolor=color_mid)
            else:
                widget.configure(bg=color_mid, highlightbackground=color_mid)
                # display_info_expression_update_color(widget)

    # saves an array of all the widgets in the row
    widgets_to_alter = frm_results_inner.grid_slaves(row=r)
    for widget in widgets_to_alter:
        if widget.winfo_class() != "Canvas":
            widget.configure(activebackground=color_dark, selectcolor=color_dark)  # changes widget color to highlight
        else:
            widget.configure(bg=color_dark, highlightbackground=color_dark)
            # display_info_expression_update_color(widget)

    previously_altered_widgets = widgets_to_alter  # saves array of widgets for if statement seen above

    Thread(target=lambda: display_info(r)).start()      # display item corresponding to clicked row


# will print the results into the results box
def print_results():
    global search_results
    r = 0  # used to increment rows to allow for a list to be displayed
    last_result_type = ""

    # will loop through everything in search results to add the banner items
    i = 0
    while i < len(search_results):  # need to use while because the length of search_results will change
        current_item_type = get_item_type(search_results[i])

        # if the type of item has changed
        if current_item_type != last_result_type:
            search_results.insert(i, current_item_type+"s:")
            last_result_type = current_item_type

        i += 1

    # loop that will print every result into radiobuttons that can be pressed to select item
    for result in search_results:

        result_type = get_item_type(result)

        if result_type:
            radb_name = Radiobutton(frm_results_inner, text=result.get_name(), activebackground=color_mid,
                                    activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                    indicatoron=False)
            radb_name.bind("<Button-1>", callback_get_widget_row)
            radb_name.grid(sticky="n, s, e, w", row=r, column=0)

            # will set the specific formatting based on the item type
            if result_type == "Variable" or result_type == "Constant":  # when displaying info about a variable/constant
                canv_equ = create_latex_widget(result.get_symbol(), frm_results_inner, color_mid)
                canv_equ.bind("<Button-1>", callback_get_widget_row)
                canv_equ.grid(sticky="n, s, e, w", row=r, column=1)

                canv_equ = create_latex_widget(result.get_units(), frm_results_inner, color_mid)
                canv_equ.bind("<Button-1>", callback_get_widget_row)

                if result_type == "Constant":
                    radb_val = Radiobutton(frm_results_inner, text=str(result.get_value()), activebackground=color_mid,
                                           activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                           indicatoron=False)
                    radb_val.bind("<Button-1>", callback_get_widget_row)
                    radb_val.grid(sticky="n, s, e, w", row=r, column=2)

                    canv_equ.grid(sticky="n, s, e, w", row=r, column=3)

                else:
                    canv_equ.grid(sticky="n, s, e, w", row=r, column=2, columnspan=2)

            elif result_type == "Equation":  # when displaying info about an equation
                canv_equ = create_latex_widget(result.get_expression(), frm_results_inner, color_mid)
                canv_equ.bind("<Button-1>", callback_get_widget_row)
                canv_equ.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            elif result_type == "Method":  # when displaying info about a method
                radb_descr = Radiobutton(frm_results_inner, text="Number of steps:" + result.get_num_steps(),
                                         activebackground=color_mid, activeforeground=text_color, borderwidth=0,
                                         selectcolor=color_mid, indicatoron=False)
                radb_descr.bind("<Button-1>", callback_get_widget_row)
                radb_descr.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            elif result_type == "Logic":  # when displaying logic info
                radb_log = Radiobutton(frm_results_inner, text="Click for more info", activebackground=color_mid,
                                       activeforeground=text_color, borderwidth=0, selectcolor=color_mid,
                                       indicatoron=False)
                radb_log.bind("<Button-1>", callback_get_widget_row)
                radb_log.grid(sticky="n, s, e, w", row=r, column=1, columnspan=3)

            r += 1  # increment rows so that items will not overlap
        else:
            if result != 0:
                Label(frm_results_inner, text=result, bg=color_mid, anchor="center",
                      font=("TkDefaultFont", fontsize + 2, "bold"))\
                    .grid(sticky="n, s, e, w", row=r, column=0, columnspan=4)
                r += 1


# will display a selected item's info in the display area
def display_info(r):
    # destroys anything that was in the display_info frame before
    destroy_item_info()

    btn_delete_item.configure(state="active")   # activate the delete button as an item would have been selected

    global selected_item
    selected_item = search_results[r]  # get the search_result from the corresponding row

    # Name of the item
    msg_name = Message(frm_info_inner, text=str(selected_item.get_name()), bg=color_light, anchor='center',
                       width=m_len*30, font=("TkDefaultFont", fontsize + 10, "bold"))
    msg_name.bind("<Button-1>", lambda e: copy_to_clipboard(selected_item.get_name(), msg_name))
    msg_name.grid(row=0, rowspan=2, column=0, columnspan=2, padx=spacing_out_y, pady=spacing_out_y, sticky="n, s, w, e")

    # Button to edit item
    Button(frm_info_inner, text="Edit Item", command=lambda: add_edit_item_window(True),
           activeforeground=text_color).grid(row=0, column=2, padx=spacing_out_y, pady=spacing_out_y, sticky="e")

    item_type = get_item_type(selected_item)  # get the type of item being displayed

    if selected_item.get_image_location() != "No image association":
        canv_image = Canvas(frm_info_inner, bg=color_light)
        canv_image.create_image(0, 0, anchor="nw", image=selected_item.get_image())
        canv_image.image = selected_item.get_image()
        canv_image.grid(row=2, column=0, columnspan=4, padx=spacing_out_y, pady=spacing_out_y, sticky="n, s, e, w")
        canv_image.configure(width=selected_item.get_image().width(), height=selected_item.get_image().height())

        # trying to fix the width of the canvas so that the images will fit properly

    r = 3  # set the row to an initial value

    if item_type == "Logic":  # when displaying info about logic
        Label(frm_info_inner, text="Logic").grid(padx=spacing_out_x * 2, sticky="e", row=1, column=2)

        display_info_description(selected_item, r)
        r += 1

    elif item_type == "Variable":  # when displaying info about a variable
        Label(frm_info_inner, text="Variable").grid(padx=spacing_out_x * 1.1, sticky="e", row=1, column=2)
        display_info_var_const(selected_item, r)
        r += 1

        display_info_description(selected_item, r)
        r += 1

    elif item_type == "Constant":  # when displaying info about a constant
        Label(frm_info_inner, text="Constant").grid(padx=spacing_out_x * 0.9, sticky="e", row=1, column=2)
        display_info_var_const(selected_item, r)
        r += 1

        display_info_description(selected_item, r)
        r += 1

    elif item_type == "Equation":  # when displaying info about a equation
        Label(frm_info_inner, text="Equation").grid(padx=spacing_out_x * 0.9, sticky="e", row=1, column=2)
        r += 1

        display_info_description(selected_item, r)
        r += 1

        r = display_info_equ(selected_item, r)

    elif item_type == "Method":  # when displaying info about a method
        Label(frm_info_inner, text="Method").grid(padx=spacing_out_x * 1.4, pady=spacing_out_y, sticky="e", row=1,
                                                  column=2)

        display_info_description(selected_item, r)
        r += 1  # set starting row

        # loops through each step and displays the steps information
        for s in range(0, selected_item.get_num_steps()):
            # add step title with items name in it
            Label(frm_info_inner, text="Step " + str(s + 1) + ": " + selected_item.get_step(s).get_name(),
                  font=("TkDefaultFont", fontsize + 6, "bold", "italic", "underline")) \
                .grid(row=r, column=0, columnspan=4, sticky="n, s, e, w", pady=spacing_out_y)
            r += 1

            i_t = get_item_type(selected_item.get_step(s))
            if i_t == "Variable" or i_t == "Constant":  # variable/constant step
                display_info_var_const(selected_item.get_step(s), r)
                r += 1

            elif i_t == "Equation":  # equation step
                r = display_info_equ(selected_item.get_step(s), r)
                r += 1

            display_info_description(selected_item.get_step(s), r)
            r += 1

    field_list = selected_item.get_fields()

    Label(frm_info_inner, text="Associated Fields",
          font=("TkDefaultFont", fontsize + 3, "italic", "underline")) \
        .grid(row=r, column=0, columnspan=3)

    r += 1

    lst_fields = Listbox(frm_info_inner, selectmode="multiple", height=len(field_list))

    # to indicate to user there is nothing to show
    if len(field_list) == 1 and field_list == [""]:
        lst_fields.insert("end", "No accociated fields")

    else:   # if there is something to show
        for field in field_list:
            lst_fields.insert("end", field)

    lst_fields.grid(column=0, columnspan=3, row=r, sticky="n, s, e, w")


# will create and print a text widget with the description of the given item printed in it
def display_info_description(item, r):
    if item.get_description() != "":
        txt_descr = Text(frm_info_inner, bg=color_light, width=35)
        txt_descr.insert("insert", item.get_description())

        num_of_lines = int(len(item.get_description())/35)+1

        txt_descr.configure(state="disabled", height=num_of_lines)
        txt_descr.grid(row=r, column=0, columnspan=4, sticky="n, s, e, w")


# used to display information for equations. was taken out just to reduce repetition
# does NOT display the name or description of the equation
def display_info_equ(equ, row):
    create_latex_widget(equ.get_expression(), frm_info_inner, frm_info_inner.cget("bg"))\
        .grid(row=row, column=0, columnspan=3, pady=spacing_out_y)

    row += 1

    # header for list of variables/constants
    Label(frm_info_inner, text="Featured variables/constants:",
          font=("TkDefaultFont", fontsize + 3, "italic", "underline"))\
        .grid(row=row, column=0, columnspan=3)

    row += 1

    # loop thorough each variable/constant and display each one's info
    for variable in equ.get_all_variables():
        # this is purely for spacing purposes
        Label(frm_info_inner, text="", fg=color_mid, font=("TkDefaultFont", 1)).grid(row=row, column=0)
        row += 1

        Label(frm_info_inner, text=str(variable.get_name()), font=("TkDefaultFont", fontsize, "underline")) \
            .grid(row=row, column=0)
        row += 1

        display_info_description(variable, row)
        row += 1

        display_info_var_const(variable, row)
        row += 1

    return row  # return the row so the above code knows where to start up again


# returns a canvas with the desired image within it
# it will create and save an image if one has not previously been saved
def create_latex_widget(string, container_widget, widget_color):
    # this check is necessary. If you don't check and there is nothing, the code will break
    if string != "":
        latex_text = "$"+string+"$"   # reformat the text so it has the correct syntax
        file_name = "Dictionary/all_latex_images/" + remove_bad_chars(string) + '.png'

        if not os.path.isfile(file_name):   # when a file hasn't already been created
            fig = figure.Figure(dpi=120)    # create the figure
            fig.text(0, 0.5, latex_text, color=text_color)  # (x coordinat, y coordinat, text, font size)
            fig.savefig(file_name, bbox_inches='tight', transparent=True)
            fig.clf()

            im = Image.open(file_name)

            # Size of the image in pixels. Return tuple
            width, height = im.size

            crop_top = 0
            crop_bot = 0
            crop_left = 0
            crop_right = 0

            # these loops will filter though the image to find when a pixel has some color in it
            # this will help to define how the image will be cropped to be as small as possible
            for w in range(0, width):
                for h in range(0, height):
                    if im.getpixel((w, h)) != (255, 255, 255, 0):
                        crop_left = w-1
                        break
                else:
                    continue
                break
            for w in range(width - 1, 0, -1):
                for h in range(height - 1, 0, -1):
                    if im.getpixel((w, h)) != (255, 255, 255, 0):
                        crop_right = w + 2
                        break
                else:
                    continue
                break
            for h in range(0, height):
                for w in range(0, width):
                    if im.getpixel((w, h)) != (255, 255, 255, 0):
                        crop_top = h-1
                        break
                else:
                    continue
                break
            for h in range(height - 1, 0, -1):
                for w in range(width - 1, 0, -1):
                    if im.getpixel((w, h)) != (255, 255, 255, 0):
                        crop_bot = h + 2
                        break
                else:
                    continue
                break

            # crop the image based on the dimensions decided above
            im_crop = im.crop((crop_left, crop_top, crop_right, crop_bot))
            im_crop.save(file_name)  # overwrite previous image

        image = PhotoImage(file=file_name)

    else:   # in the case where something bad is sent
        image = PhotoImage(file="error.png")
        string = "Error copying text"

    canv_image = Canvas(container_widget, width=image.width(), height=image.height(),
                        bg=widget_color, highlightbackground=widget_color)
    canv_image.create_image(2, 2, anchor="nw", image=image)
    canv_image.image = image        # this is necessary cause tkinter handling of images is a bit shit
    canv_image.bind("<Button-1>", lambda e: copy_to_clipboard(string, canv_image))

    return canv_image


# will copy a given string to the clipboard
def copy_to_clipboard(string, widget):
    window.clipboard_clear()    # this is done so that the item to add will not be added to the end of the previous item
    window.clipboard_append(string)

    # this will use a different thread to do this task meaning the program will not freeze whilst the button is flashing
    Thread(target=lambda: flash_widget(widget)).start()


# will flash the given widget to indicate something happened
def flash_widget(widget):
    og_color = widget.cget("bg")
    widget.configure(bg=color_highlight)
    time.sleep(0.75)
    widget.configure(bg=og_color)


# will remove any characters that are not allowed to be in a name
def remove_bad_chars(string):
    bad_chars = '\/:*?"<>|'

    for char in bad_chars:
        string = string.replace(char, '')

    return string


# used to display information for variables and constants. was taken out just to reduce repetition
# does NOT display names or descriptions
def display_info_var_const(var_or_const, row):
    frm_attribute = LabelFrame(frm_info_inner, text="click item to copy to clipboard", relief="ridge",
                               labelanchor="se", font=("TkDefaultFont", fontsize - 3, "italic"))
    frm_attribute.grid(row=row, column=0, columnspan=3, sticky="n, s, e, w")
    frm_attribute.grid_columnconfigure(1, weight=1)
    frm_attribute.grid_columnconfigure(3, weight=1)
    frm_attribute.grid_columnconfigure(5, weight=1)

    Label(frm_attribute, text="Symbol: ").grid(row=0, column=0, sticky="e")
    create_latex_widget(var_or_const.get_symbol(), frm_attribute, color_light).grid(row=0, column=1, sticky="w")

    if get_item_type(var_or_const) == "Constant":       # for a constant specifically
        Label(frm_attribute, text="Value: ").grid(row=0, column=2, sticky="e")
        ety_value = Entry(frm_attribute)
        ety_value.insert(0, var_or_const.get_value())
        ety_value.configure(state="readonly", width=len(var_or_const.get_value()))
        ety_value.grid(row=0, column=3)

    Label(frm_attribute, text="Units: ").grid(row=0, column=4, sticky="e")
    create_latex_widget(var_or_const.get_units(), frm_attribute, color_light).grid(row=0, column=5, sticky="e")


# get the corresponding string of each item type
def item_to_string(item):
    item_type = get_item_type(item)

    item_string = str(str(item.get_name()) + '&' + str(item.get_description()) + '&' +
                      str(item.get_image_location()) + '&')

    if item.get_fields() == ():   # when nothing has been entered
        item_string += ''

    else:   # when something has been entered
        for field in item.get_fields():
            item_string += str(field) + ','
        item_string = item_string[:-1]  # used to get rid of the last comma since it's not necessary

    if item_type == "Variable":  # when displaying info about a variable
        item_string += str('&' + str(item.get_symbol()) + '&' + str(item.get_units()))

    elif item_type == "Constant":  # when displaying info about a constant
        item_string += str('&' + str(item.get_symbol()) + '&' + str(item.get_value()) + '&' + str(item.get_units()))

    elif item_type == "Equation":  # when displaying info about a equation
        item_string += str('&' + str(item.get_expression()))

        for var in item.get_all_variables():
            item_string += "&type:" + str(get_item_type(var)) + '&' + item_to_string(var).replace("\n", "")

        item_string += "&end:Equation"

    elif item_type == "Method":  # when displaying info about a method
        for step in item.get_steps():
            item_string += "&type:" + str(get_item_type(step)) + '&' + item_to_string(step).replace("\n", "")

        item_string += "&end:Method"

    item_string = item_string.replace("\\", "§")

    return item_string


# will return a filled out list of items. Checks if its given multiple lines of strings or just one line
def string_to_item(lines, item_type):
    items = []
    if isinstance(lines, str):
        items = string_to_item_conversion_logic(lines, item_type)
    else:  # when an array is passed
        for li in lines:
            result = string_to_item_conversion_logic(li, item_type)
            if result:
                items.append(result)

    return items  # return the list of items


# will return a filled out item based on the string given. Shouldn't be used on its own
def string_to_item_conversion_logic(archived_line, item_type):
    item = False  # just in case nothing is written to this it will return a 'False' error message

    # splits the string and removes \n and puts this array into split_string
    split_line = str(archived_line).replace("§", "\\")
    split_line = split_line.replace("\n", "")
    split_line = split_line.split('&')

    # checks to make sure not to run the first line with description info through the item creator
    if split_line[0] != "_=^=_" and split_line[0] != "":

        # will decide and create the correct item type
        # len() portion ensures split_line array is the correct length which would indicate correct storage formatting
        if item_type == "Logic" and len(split_line) == 4:  # when displaying logic info
            item = Logic(split_line[0], split_line[1], split_line[2], split_line[3].split(','))

        elif item_type == "Variable" and len(split_line) == 6:  # when displaying info about a variable
            item = Variable(split_line[0], split_line[1], split_line[2], split_line[3].split(','),
                            split_line[4], split_line[5])

        elif item_type == "Constant" and len(split_line) == 7:  # when displaying info about a constant
            item = Constant(split_line[0], split_line[1], split_line[2], split_line[3].split(','),
                            split_line[4], split_line[5], split_line[6])

        # >= 12 because name, description, image, field, expression, type identifier,
        # and 1 variable (shorter than constants)
        elif item_type == "Equation" and len(split_line) >= 12:  # when displaying info about a equation
            list_of_var_con = []  # will hold the list of variables and constants the equation will have

            # will look at whether there are variables/constants in the string
            # if there are it will create and add them to a list of variables/constants list_of_var_con
            for i in range(0, len(split_line) - 1):
                if split_line[i] == "type:Variable":  # when there its a variable
                    list_of_var_con.append(Variable(split_line[i + 1], split_line[i + 2], split_line[i + 3],
                                                    split_line[i + 4].split(','), split_line[i + 5], split_line[i + 6]))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                elif split_line[i] == "type:Constant":  # when there its a constant
                    list_of_var_con.append(Constant(split_line[i + 1], split_line[i + 2], split_line[i + 3],
                                                    split_line[i + 4].split(','), split_line[i + 5], split_line[i + 6],
                                                    split_line[i + 7]))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ""

            # will create a new equation and add it to the list of items
            item = Equation(split_line[0], split_line[1], split_line[2], split_line[3].split(','),
                            split_line[4], list_of_var_con)

        # >= 9 because name, description, image, field, type identifier, and 1 logic (shortest item type)
        elif item_type == "Method" and len(split_line) >= 9:  # when displaying info about a method
            list_of_steps = []
            for i in range(0, len(split_line)):
                inner_string = ""
                if split_line[i] == "type:Variable":
                    for s in range(1, 7):  # loop through each piece that corresponds to variables
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a variable
                    list_of_steps.append(string_to_item(inner_string, "Variable"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                if split_line[i] == "type:Constant":
                    for s in range(1, 8):  # loop through each piece that corresponds to constants
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a constant
                    list_of_steps.append(string_to_item(inner_string, "Constant"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

                if split_line[i] == "type:Equation":
                    end = 0  # used to save when the end occurs

                    # find "end:Equation" to figure when the equation ends
                    for e in range(i, len(split_line)):
                        if split_line[e] == "end:Equation":
                            end = e  # save the block when "end:Equation" occurs
                            break  # stop the loop

                    for s in range(i + 1, end):  # loop through each piece that corresponds to equation
                        inner_string += split_line[s] + '&'  # puts them all into one string

                    # pass the string to convert it into an equation
                    list_of_steps.append(string_to_item(inner_string, "Equation"))

                    # will remove all item flags in already considered area
                    for s in range(i, end):  # loop through each piece that corresponds to method
                        if split_line[s] == "type:Variable" or split_line[s] == "type:Constant" or \
                                split_line[s] == "type:Equation" or split_line[s] == "type:Logic" or \
                                split_line[s] == "type:Method":
                            split_line[s] = ''

                if split_line[i] == "type:Method":
                    end = 0  # used to save when the end occurs

                    # find "end:Method" to figure when the method ends
                    for e in range(i, len(split_line)):
                        if split_line[e] == "end:Method":
                            end = e  # save the block when "end:Method" occurs
                            break  # stop the loop

                    for s in range(i + 1, end):  # loop through each piece that corresponds to method
                        inner_string += split_line[s] + '&'  # puts them all into one string

                    # pass the string to convert it into a method
                    list_of_steps.append(string_to_item(inner_string, "Method"))

                    # will remove all item flags in already considered area
                    for s in range(i, end):  # loop through each piece that corresponds to method
                        if split_line[s] == "type:Variable" or split_line[s] == "type:Constant" or \
                                split_line[s] == "type:Equation" or split_line[s] == "type:Logic" or \
                                split_line[s] == "type:Method":
                            split_line[s] = ''

                if split_line[i] == "type:Logic":
                    for s in range(1, 5):  # loop through each piece that corresponds to logic
                        inner_string += split_line[i + s] + '&'  # puts them all into one string

                    # pass the string to convert it into a logic
                    list_of_steps.append(string_to_item(inner_string, "Logic"))

                    # will remove the flag item so that it doesn't get reintroduced
                    split_line[i] = ''

            # will combine everything together into a method item and add it to the list
            item = Method(split_line[0], split_line[1], split_line[2], split_line[3].split(','), list_of_steps)

    return item  # return the item


# get correct file directory for item
def get_item_file_directory(item):
    item_type = get_item_type(item)

    # will decide the correct file directory for the item
    if item_type == "Variable":  # when displaying info about a variable
        file_directory = "Dictionary/variables.txt"
    elif item_type == "Constant":  # when displaying info about a constant
        file_directory = "Dictionary/constants.txt"
    elif item_type == "Equation":  # when displaying info about a equation
        file_directory = "Dictionary/equations.txt"
    elif item_type == "Method":  # when displaying info about a method
        file_directory = "Dictionary/methods.txt"
    elif item_type == "Logic":  # when displaying logic info
        file_directory = "Dictionary/logic.txt"
    else:
        file_directory = "Dictionary/lost_or_deleted_items/lost_or_deleted_items.txt"
    return file_directory


# will save item ALPHABETICALLY into respective files within the dictionary directory
def save_item(item):
    directory = get_item_file_directory(item)

    all_lines = get_file_lines(directory)
    all_lines.append(item_to_string(item))

    lines = all_lines[1:]
    lines.sort()

    file = open(directory, 'w')     # open the corresponding file
    file.write(all_lines[0].rstrip())        # write title line

    # removes any random or bad lines and writes all the remaining lines
    i = 0
    while i < len(lines):
        if lines[i].find('&') == -1 or lines[i].rstrip() == "":
            lines.pop(i)
        else:
            file.write("\n" + lines[i].rstrip())
            i += 1

    file.close()  # close the file


# saves all the lines of a target_file
def get_file_lines(target_file):
    file_existence_filter(target_file)

    file = open(target_file, 'r')  # open file
    lines = file.readlines()  # save the lines
    file.close()  # close the file

    return lines


# will filter the target file to make sure it exists. if it doesn't it will create it
def file_existence_filter(target_file):
    try:
        file = open(target_file, 'r')  # open file
        file.close()  # close the file
    except FileNotFoundError:
        file = open(target_file, 'w')  # open file

        if target_file == "Dictionary/logic.txt":  # when writing info for a logic
            file.write("_=^=_& name & description & image name")
        elif target_file == "Dictionary/variables.txt":  # when writing info for a variable
            file.write("_=^=_& name & description & image name & symbol & units")
        elif target_file == "Dictionary/constants.txt":  # when writing info for a constant
            file.write("_=^=_& name & description & image name & symbol & value & units")
        elif target_file == "Dictionary/equations.txt":  # when writing info for a equation
            file.write("_=^=_& name & description & image name & expression & list of accompanying variables/constants")
        elif target_file == "Dictionary/methods.txt":  # when writing info for method
            file.write("_=^=_& name & description & image name & list of accompanying steps")
        elif target_file == "Dictionary/saved_fields.txt":  # when writing info for method
            file.write("_=^=_& Stores all fields so user can select them")
        else:
            file.write("_=^=_& Lost items are found here")
        file.close()  # close the file


# will return a letter based on the type of item
def get_item_type(item):
    if isinstance(item, Constant):  # when displaying info about a constant
        item_type = "Constant"
    elif isinstance(item, Variable):  # when displaying info about a variable
        item_type = "Variable"
    elif isinstance(item, Equation):  # when displaying info about a equation
        item_type = "Equation"
    elif isinstance(item, Method):  # when displaying info about a method
        item_type = "Method"
    elif isinstance(item, Logic):  # when displaying logic info
        item_type = "Logic"
    else:
        item_type = False
    return item_type


# used to create the add/edit item window
def add_edit_item_window(to_edit):
    # stuff for creating the pop-up window
    small_win = Toplevel()
    small_win.configure(background=color_dark)
    small_win.grid_rowconfigure(0, weight=1)
    small_win.grid_columnconfigure(0, weight=1)

    small_win.grab_set()  # stops the user from interacting with the main window

    # the frame that will hold the canvas and all the other scrolling shite
    frm_add_edit_scroll_wrapper = Frame(small_win, highlightthickness=1, highlightbackground=accent_light)
    # reveals the frame holding the scrollbar, canvas, and wrapping frame
    frm_add_edit_scroll_wrapper.grid(column=0, row=0, sticky="n, s, e, w")
    # configures the row with the canvas to be able to expand
    frm_add_edit_scroll_wrapper.grid_rowconfigure(0, weight=1)
    frm_add_edit_scroll_wrapper.grid_columnconfigure(0, weight=1)

    # the canvas that will enable the possibility to scroll through the various search results
    canv_add_edit = Canvas(frm_add_edit_scroll_wrapper)
    # frame in which the results will be listed
    frm_add_edit_inner = Frame(canv_add_edit, bg=color_mid)
    # scroll bar that will can scroll through results shown in frm_results_inner on the canvas
    srlb_add_edit = Scrollbar(frm_add_edit_scroll_wrapper, orient="vertical", command=canv_add_edit.yview)

    # configures the canvas to include a scrolling command linked to the scrollbar
    canv_add_edit.configure(yscrollcommand=srlb_add_edit.set)

    # write out everything for the search results. They won't show up because
    canv_add_edit.grid(column=0, row=0, sticky="n, s, e, w")
    srlb_add_edit.grid(column=1, row=0, sticky="n, s, e, w")

    # creates a window in which the frame is placed. This allows the frame to be scrolled through
    canv_add_edit.create_window((0, 0), window=frm_add_edit_inner, anchor='nw')

    # calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
    frm_add_edit_inner.bind("<Configure>", lambda e: canv_add_edit.configure(scrollregion=canv_add_edit.bbox("all")))

    # configures the row with the canvas to be able to expand
    frm_add_edit_inner.grid_columnconfigure(1, weight=1)

    # drop down for adding items, "e" will give the option that was clicked on
    opm_type = OptionMenu(frm_add_edit_inner, item_type_to_add_or_edit,
                          "Logic", "Constant", "Variable", "Equation", "Method",
                          command=lambda e: add_edit_item_option_display(e, frm_add_edit_inner, False))
    opm_type.grid(column=0, columnspan=2, row=0, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    Button(frm_add_edit_inner, text="Submit Item",
           command=lambda: item_submit(frm_add_edit_inner, to_edit, small_win)) \
        .grid(column=2, row=0, sticky="n, s, e, w")

    lab_name = Label(frm_add_edit_inner, text="Name:", highlightthickness=1, highlightbackground=accent_light)
    lab_name.grid(column=0, row=1, sticky="n, s, e, w")
    txt_name = Entry(frm_add_edit_inner, highlightthickness=1, highlightbackground=accent_light)
    txt_name.grid(column=1, columnspan=2, row=1, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    lab_def = Label(frm_add_edit_inner, text="Description:", highlightthickness=1, highlightbackground=accent_light)
    lab_def.grid(column=0, row=2, sticky="n, s, e, w")
    txt_def = Text(frm_add_edit_inner, highlightthickness=1, highlightbackground=accent_light)
    txt_def.grid(column=1, columnspan=2, row=2, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    lab_img = Label(frm_add_edit_inner, text="Image name:", highlightthickness=1, highlightbackground=accent_light)
    lab_img.grid(column=0, row=3, sticky="n, s, e, w")
    txt_img = Entry(frm_add_edit_inner, highlightthickness=1, highlightbackground=accent_light)
    txt_img.grid(column=1, columnspan=2, row=3, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    add_edit_field(frm_add_edit_inner, 4, selected_item, to_edit)

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_name.insert(0, selected_item.get_name())
        txt_def.insert("insert", selected_item.get_description())
        txt_img.insert(0, selected_item.get_image_location())

    # will set the initial value of the option menu to the correct item type
    if to_edit:
        opm_type.configure(state="disabled")
        it = get_item_type(selected_item)
        small_win.title("Edit " + it + " " + selected_item.get_name())

        if it == "Variable":
            item_type_to_add_or_edit.set("Variable")
            add_edit_item_option_display("Variable", frm_add_edit_inner, to_edit)
        elif it == "Constant":
            item_type_to_add_or_edit.set("Constant")
            add_edit_item_option_display("Constant", frm_add_edit_inner, to_edit)
        elif it == "Equation":
            item_type_to_add_or_edit.set("Equation")
            add_edit_item_option_display("Equation", frm_add_edit_inner, to_edit)
        elif it == "Method":
            item_type_to_add_or_edit.set("Method")
            add_edit_item_option_display("Method", frm_add_edit_inner, to_edit)
        elif it == "Logic":
            item_type_to_add_or_edit.set("Logic")

    else:
        small_win.title("Add new item")
        item_type_to_add_or_edit.set("Logic")

    small_win.mainloop()


# displays the correct input criteria for each of the item types
def add_edit_item_option_display(type_to_display, container_widget, to_edit):
    # saves all the widgets after the first 8 which are always gonna be there
    widgets = container_widget.winfo_children()[11:]

    # deletes those widgets to remove remnants
    for w in widgets:
        w.destroy()

    # reset this value as something different is being added
    global step_num
    step_num = 0

    # will decide what needs to be displayed depending on the type of item
    if type_to_display == "Variable" or type_to_display == "Constant":  # when displaying info about a variable/constant
        add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, selected_item)

    elif type_to_display == "Equation":  # when displaying info about a equation
        add_edit_item_equation_display(container_widget, to_edit, selected_item)

    elif type_to_display == "Method":  # when displaying info about a method
        selected_item_to_add = StringVar()  # create the item type in this fancy way I don't understand
        selected_item_to_add.set("Select an item to add")  # will set the initial value

        opm_type = OptionMenu(container_widget, selected_item_to_add,
                              "Logic", "Constant", "Variable", "Equation")
        opm_type.grid(column=1, columnspan=2, row=4, sticky="n, s, e, w")

        Button(container_widget, text="Add Step:",
               command=lambda: add_edit_method_step_add(selected_item_to_add.get(), container_widget, to_edit, "")) \
            .grid(column=0, row=4, sticky="n, s, e, w")

        # will automatically display all the steps affiliated with this method when in editing mode
        if to_edit:
            for step in selected_item.get_steps():
                add_edit_method_step_add(get_item_type(step), container_widget, to_edit, step)


# displays the correct input criteria for each of the item types
def add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, e_item):
    r = container_widget.winfo_children()[-1].grid_info()['row'] + 3  # not sure why it always gets 0 but it works

    lab_sym = Label(container_widget, text="Symbol:",
                    relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    lab_sym.grid(column=0, row=r, sticky="n, s, e, w")
    txt_sym = Entry(container_widget,
                    relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    txt_sym.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    r += 1

    if type_to_display == "Constant":  # for the constant specifically
        lab_val = Label(container_widget, text="Value:",
                        relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
        lab_val.grid(column=0, row=r, sticky="n, s, e, w")
        txt_val = Entry(container_widget,
                        relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
        txt_val.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        # will add the edit item's stuff into the entry boxes
        if to_edit:
            txt_val.insert(0, e_item.get_value())

        r += 1

    lab_unit = Label(container_widget, text="Units:",
                     relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    lab_unit.grid(column=0, row=r, sticky="n, s, e, w")
    txt_unit = Entry(container_widget,
                     relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
    txt_unit.grid(column=1, columnspan=2, row=r, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    r += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_sym.insert(0, e_item.get_symbol())
        txt_unit.insert(0, e_item.get_units())

    return r


# displays the correct input criteria for each of the item types
def add_edit_item_equation_display(container_widget, to_edit, equ_to_display):
    start_row = container_widget.winfo_children()[-1].grid_info()['row'] + 3

    lab_equ = Label(container_widget, text="Equation:", highlightthickness=1,
                    highlightbackground=accent_light)
    lab_equ.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_equ = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_equ.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_equ.insert(0, equ_to_display.get_expression())

    frm_equ_holder = Frame(container_widget)
    frm_equ_holder.grid(column=0, columnspan=3, row=start_row, sticky="n, s, e, w")
    frm_equ_holder.columnconfigure(2, weight=1)
    frm_equ_holder.columnconfigure(3, weight=1)

    frm_add_btns_holder = Frame(frm_equ_holder)
    frm_add_btns_holder.grid(column=2, row=1, sticky="n, s, e, w")
    frm_add_btns_holder.columnconfigure(0, weight=1)
    frm_add_btns_holder.columnconfigure(1, weight=1)

    btn_add_var = Button(frm_add_btns_holder, text="Add Variable",
                         command=lambda: add_edit_item_equation_item_add("Variable", frm_equ_holder, False))
    btn_add_var.grid(column=0, row=0, sticky="n, s, e, w")

    btn_add_const = Button(frm_add_btns_holder, text="Add Constant",
                           command=lambda: add_edit_item_equation_item_add("Constant", frm_equ_holder, False))
    btn_add_const.grid(column=1, row=0, sticky="n, s, e, w")

    Label(frm_equ_holder, text="Featured variables/constants:", highlightthickness=1, highlightbackground=accent_light,
          font=("TkDefaultFont", fontsize + 2, "bold", "italic")) \
        .grid(column=0, columnspan=2, row=1, sticky="n, s, e, w")

    # will automatically display all the variables and constants affiliated with this equation when in editing mode
    if to_edit:
        for var_const in equ_to_display.get_all_variables():
            add_edit_item_equation_item_add(var_const, frm_equ_holder, to_edit)


# displays wrapping items then calls add_edit_item_v_or_c_display to display all var/const in/to add to the equation 
def add_edit_item_equation_item_add(item_to_add, container_widget, to_edit):
    if to_edit:
        type_to_display = get_item_type(item_to_add)
    else:
        type_to_display = item_to_add

    start_row = container_widget.winfo_children()[-1].grid_info()['row'] + 1

    if type_to_display == "Variable":
        Label(container_widget, text="Variable:",
              anchor="center", font=("TkDefaultFont", fontsize, "italic", "underline")) \
            .grid(column=0, columnspan=2, row=start_row, sticky="n, s, e, w")

    else:
        Label(container_widget, text="Constant:",
              anchor="center", font=("TkDefaultFont", fontsize, "italic", "underline")) \
            .grid(column=0, columnspan=2, row=start_row, sticky="n, s, e, w")

    btn_equ_item_delete = Button(container_widget, text="Delete this " + type_to_display,
                                 command=lambda: delete_added_item(container_widget, btn_equ_item_delete,
                                                                   type_to_display, False))
    btn_equ_item_delete.grid(column=2, row=start_row, sticky="n, s, e")

    start_row += 1

    lab_name = Label(container_widget, text="Name:", highlightthickness=1, highlightbackground=accent_light)
    lab_name.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_name = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_name.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    lab_def = Label(container_widget, text="Description:", highlightthickness=1, highlightbackground=accent_light)
    lab_def.grid(column=0, row=start_row, sticky="n, s, e, w")
    txt_def = Text(container_widget, highlightthickness=1, highlightbackground=accent_light)
    txt_def.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    start_row += 1

    # will add the edit item's stuff into the entry boxes
    if to_edit:
        txt_name.insert(0, item_to_add.get_name())
        txt_def.insert('insert', item_to_add.get_description())

    add_edit_item_v_or_c_display(type_to_display, container_widget, to_edit, item_to_add)


# displays wrapping items then calls respective item addition to display all items in/to add to the method
def add_edit_method_step_add(type_to_display, container_widget, to_edit, item_to_display):
    global step_num
    step = step_num + 1
    step_num += 1

    # used to check to make sure user selected an actual item
    if type_to_display != "Select an item to add":
        start_row = container_widget.winfo_children()[-1].grid_info()['row'] + 1

        Label(container_widget, highlightthickness=1, text="Step " + str(step) + ": " + str(type_to_display),
              highlightbackground=accent_light, font=("TkDefaultFont", fontsize + 5, "bold", "italic")) \
            .grid(column=0, columnspan=2, row=start_row, sticky="n, s, e, w")

        btn_method_item_delete = Button(container_widget, text="Delete this " + type_to_display,
                                        command=lambda: delete_added_item(container_widget, btn_method_item_delete,
                                                                          type_to_display, True))
        btn_method_item_delete.grid(column=2, row=start_row, sticky="n, s, e, w")

        start_row += 1

        lab_name = Label(container_widget, text="Name:")
        lab_name.grid(column=0, row=start_row, sticky="n, s, e, w")
        txt_name = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
        txt_name.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        start_row += 1

        lab_def = Label(container_widget, text="Description:", highlightthickness=1, highlightbackground=accent_light)
        lab_def.grid(column=0, row=start_row, sticky="n, s, e, w")
        txt_def = Text(container_widget, highlightthickness=1, highlightbackground=accent_light)
        txt_def.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        start_row += 1

        lab_img = Label(container_widget, text="Image name:", highlightthickness=1, highlightbackground=accent_light)
        lab_img.grid(column=0, row=start_row, sticky="n, s, e, w")
        txt_img = Entry(container_widget, highlightthickness=1, highlightbackground=accent_light)
        txt_img.grid(column=1, columnspan=2, row=start_row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

        start_row += 1

        # will add the edit item's stuff into the entry boxes
        if to_edit:
            txt_name.insert(0, item_to_display.get_name())
            txt_def.insert('insert', item_to_display.get_description())

            start_row += 1

            if type_to_display == "Constant":
                add_edit_item_v_or_c_display("Constant", container_widget, to_edit, item_to_display)

            elif type_to_display == "Variable":
                add_edit_item_v_or_c_display("Variable", container_widget, to_edit, item_to_display)

            elif type_to_display == "Equation":
                add_edit_item_equation_display(container_widget, to_edit, item_to_display)

        else:
            if type_to_display == "Constant":
                add_edit_item_v_or_c_display("Constant", container_widget, False, item_to_display)
            elif type_to_display == "Variable":
                add_edit_item_v_or_c_display("Variable", container_widget, False, item_to_display)
            elif type_to_display == "Equation":
                add_edit_item_equation_display(container_widget, False, item_to_display)

    else:
        print("Please select an item pop-up window would occur here")


# this will delete any item that has been idea previously and reconfigure relevant stuff
def delete_added_item(container_widget, button, type_to_delete, in_meth):
    number_of_children = 0

    if type_to_delete == "Logic":
        number_of_children = 6
    elif type_to_delete == "Variable":
        number_of_children = 10
    elif type_to_delete == "Constant":
        number_of_children = 12
    elif type_to_delete == "Equation":
        number_of_children = 9

    all_children = container_widget.winfo_children()

    start_child = 0

    for c in range(0, len(all_children)):
        if all_children[c] == button:
            start_child = c - 1
            break

    children_to_delete = all_children[start_child:start_child + number_of_children]

    # delete the children that are to be deleted
    for child in children_to_delete:
        child.destroy()

    # if the deleting is happening within a method, this will reset the step labels
    if in_meth:
        global step_num
        step_num -= 1
        new_step = 1

        all_children = container_widget.winfo_children()

        for child in all_children:
            if child.winfo_class() == "Label":
                label_text = child.cget("text").rsplit(" ")     # split up label text to better extract different parts

                if label_text[0] == "Step":
                    label_text[1] = str(new_step) + ":"       # change the name of numerical portion of the label text
                    child.configure(text=label_text)
                    new_step += 1


# used to create a region for the user to add fields to their item
def add_edit_field(container_widget, row, item_to_display, to_edit):
    field_selected.set("Select a field tag")  # will set the initial value

    lab_field = Label(container_widget, text="Corresponding Fields:", highlightthickness=1,
                      highlightbackground=accent_light)
    lab_field.grid(column=0, row=row, sticky="n, s, e, w")
    lst_field = Listbox(container_widget, selectmode="multiple")
    lst_field.grid(column=1, row=row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    if to_edit and item_to_display.get_fields() != ():
        for field in item_to_display.get_fields():
            lst_field.insert("end", field)

    height = lst_field.size()
    if height == 0:
        height = 1
    lst_field.configure(height=height)

    # the *list_of_fields will break list_of_fields into individual pieces which will then be sent to OptionMenu
    opm_field = OptionMenu(container_widget, field_selected, *list_of_fields, "-New Field-",
                           command=lambda e: add_edit_field_logic(e, lst_field, opm_field, container_widget, row))
    opm_field.grid(column=2, row=row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)

    return row + 1


# will chose to either add item to field list or bring up a field creation window
def add_edit_field_logic(choice, lst, opm, container_widget, row):
    already_in_list = lst.get(0, "end")
    no_repeat = True

    for f in already_in_list:
        if choice == f:
            alert_user("This field is already in the list.", False)
            no_repeat = False
            break

    if no_repeat:
        if choice != "-New Field-":
            lst.insert("end", choice)

        else:
            while True:     # will keep going until the user inputs acceptable values
                # in case the user cancels the input window which would then return NoneType
                try:
                    field = simpledialog.askstring(title="New Field", prompt="Enter new field name").rstrip()

                except AttributeError:  # if the user cancels it wont do anything
                    break

                # used to re-grab the toplevel with the editing stuff so that things to mess up
                lst.master.master.master.master.grab_set()

                not_in_master_list = True

                if field != "":
                    # will look through fields archive to ensure new field is not already in there
                    for f in list_of_fields:
                        if field == f or field == "":
                            alert_user("This field already exists in the data base. It will not be re-added.", False)
                            not_in_master_list = False
                            break

                    # when the field isn't alread in there
                    if not_in_master_list:
                        if ',' in field or '&' in field or '§' in field:
                            alert_user("You have entered a coma, '&', or '§' somewhere in the name of the new field.\n"
                                       "None of these characters are allowed, please try again.", False)
                        else:
                            list_of_fields.append(field)
                            lst.insert("end", field)

                            # gotta destroy and make a new optionmenu cause you can't really update what is in the menu
                            opm.destroy()
                            opm_field = OptionMenu(container_widget, field_selected, *list_of_fields, "-New Field-",
                                                   command=lambda e: add_edit_field_logic(e, lst, opm_field,
                                                                                          container_widget, row))
                            opm_field.grid(column=2, row=row, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)
                            break

                    else:   # when there is already a field in the data base the loop will stop
                        break

                else:   # when the user enters nothing
                    alert_user("You have not entered anything. Please enter a word.", False)

        height = lst.size()
        if height == 0:
            height = 1
        lst.configure(height=height)


# will add or edit the item the user has given
def item_submit(container_widget, to_edit, top_level_window):
    list_of_widgets = container_widget.winfo_children()
    item_type_selected = item_type_to_add_or_edit.get()
    fields_selected = ""

    item_to_save = ""
    outer_list_of_txt_input = []
    full_list_of_txt_input = []     # used for checking all text input for irregularities

    # collect all the text boxes into a list
    for item in list_of_widgets:
        if item.winfo_class() == "Entry":
            outer_list_of_txt_input.append(item.get().rstrip())
            full_list_of_txt_input.append(item.get().rstrip())

        elif item.winfo_class() == "Text":
            outer_list_of_txt_input.append(item.get(1.0, "end").rstrip())
            full_list_of_txt_input.append(item.get(1.0, "end").rstrip())

        elif item.winfo_class() == "Listbox":
            fields_selected = item.get(0, "end")

        elif item.winfo_class() == "Frame":
            list_of_frame_widgets = item.winfo_children()
            for inner_item in list_of_frame_widgets:
                if inner_item.winfo_class() == "Entry":
                    full_list_of_txt_input.append(inner_item.get().rstrip())

                elif inner_item.winfo_class() == "Text":
                    full_list_of_txt_input.append(inner_item.get(1.0, "end").rstrip())

    is_special_char_present = False

    for user_input in full_list_of_txt_input:
        if '&' in user_input or '§' in user_input:       # will look out for the use of the special character '&'
            is_special_char_present = True

    if full_list_of_txt_input[0] == '':     # if no name has been given to the item
        alert_user("You have not filled out all the fields for this item. Please enter something into every text box",
                   False)

    elif is_special_char_present:
        alert_user("In one of the fields you have used either the character '&' or '§'. These are not allowed. "
                   "Please change them.", False)

    else:
        # will start the save logic corresponding to what the user wants to save
        if item_type_selected == "Logic":
            item_to_save = item_submit_log_var_const(outer_list_of_txt_input, fields_selected)

        elif item_type_selected == "Variable":
            item_to_save = item_submit_log_var_const(outer_list_of_txt_input, fields_selected)

        elif item_type_selected == "Constant":
            item_to_save = item_submit_log_var_const(outer_list_of_txt_input, fields_selected)

        elif item_type_selected == "Equation":
            item_to_save = item_submit_equ(outer_list_of_txt_input, fields_selected,
                                           list_of_widgets[-1].winfo_children())

        elif item_type_selected == "Method":
            last_child = LabelFrame()
            list_of_steps = []
            list_of_frames = []
            i_entry = 3
            i_frame = 0

            # get all frames in the list_of_widgets. Used only for equations
            for item in list_of_widgets:
                if item.winfo_class() == "Frame":
                    list_of_frames.append(item)

            for child in list_of_widgets:
                if last_child.winfo_class() == "Label" and child.winfo_class() == "Button":
                    # will keep characters after the ":" then remove the space just before the actual word
                    text = last_child.cget("text").rsplit(":", 1)[1]
                    check_text = text[1:]

                    if check_text == "Variable":
                        list_of_steps.append(
                            item_submit_log_var_const(outer_list_of_txt_input[i_entry:i_entry + 4], fields_selected))
                        i_entry += 4

                    elif check_text == "Constant":
                        list_of_steps.append(
                            item_submit_log_var_const(outer_list_of_txt_input[i_entry:i_entry + 5], fields_selected))
                        i_entry += 5

                    elif check_text == "Logic":
                        # logic_text is stop gap until logic images are implemented
                        logic_text = outer_list_of_txt_input[i_entry:i_entry + 3]

                        list_of_steps.append(item_submit_log_var_const(logic_text, fields_selected))
                        i_entry += 2

                    elif check_text == "Equation":
                        list_of_steps.append(
                            item_submit_equ(outer_list_of_txt_input[i_entry:i_entry + 3], fields_selected,
                                            list_of_frames[i_frame].winfo_children()))
                        i_frame += 1
                        i_entry += 3

                last_child = child

            item_to_save = Method(outer_list_of_txt_input[0], outer_list_of_txt_input[1], outer_list_of_txt_input[2],
                                  fields_selected, list_of_steps)

        # checks to see if there is a repeat of the item
        if check_for_repeats(item_to_save):
            alert_user("There is an item already in the dictionary that matches what you just entered.\n"
                       "This repeated item will not be added to the dictionary.", False)

        else:   # if there is no repeat then the item will be saved
            # if the user wants to edit an item then the old item is moved to the trash
            if to_edit:
                move_item_to_trash(selected_item)

            save_item(item_to_save)
            save_list_of_fields()       # done now so that if previous addition was canceled it would not be saved
            top_level_window.destroy()  # close the toplevel window so the user can go back to what they where doing


# will return a logic, variable, or constant depending on the length of list given
def item_submit_log_var_const(text_list, fields):
    if len(text_list) < 5:
        return Logic(text_list[0], text_list[1], text_list[2], fields)

    elif len(text_list) == 5:
        return Variable(text_list[0], text_list[1], text_list[2], fields, text_list[3], text_list[4])

    else:
        return Constant(text_list[0], text_list[1], text_list[2], fields, text_list[3], text_list[4], text_list[5])


# will return a equation filled out equation
def item_submit_equ(outer_text_list, fields, equ_frame_children):
    equ_frame_txt_box_text = []

    # get list of entry boxes inside the equation frame
    for item in equ_frame_children:
        if item.winfo_class() == "Entry":
            equ_frame_txt_box_text.append(item.get().rstrip())

        elif item.winfo_class() == "Text":
            equ_frame_txt_box_text.append(item.get(1.0, "end").rstrip())

    equ_last_frame_child = Radiobutton()
    list_of_variables = []
    i_entry = 0

    for child in equ_frame_children:
        if equ_last_frame_child.winfo_class() == "Label" and child.winfo_class() == "Button":
            if equ_last_frame_child.cget("text") == "Variable:":
                text_list = equ_frame_txt_box_text[i_entry:i_entry + 4]
                text_list.insert(2, None)
                list_of_variables.append(item_submit_log_var_const(text_list, fields))
                i_entry += 4

            elif equ_last_frame_child.cget("text") == "Constant:":
                text_list = equ_frame_txt_box_text[i_entry:i_entry + 5]
                text_list.insert(2, None)
                list_of_variables.append(item_submit_log_var_const(text_list, fields))
                i_entry += 5

        equ_last_frame_child = child

    return Equation(outer_text_list[0], outer_text_list[1], outer_text_list[2], fields,
                    outer_text_list[3], list_of_variables)


# asks the user if they do wish to delete their selected item before doing so
def item_delete_ask_user():
    if alert_user("Do you wish to delete the selected item?", True):
        move_item_to_trash(selected_item)


# used to move any item to the trash document
def move_item_to_trash(item):
    # save necessary info about selected_item
    selected_item_save_location = get_item_file_directory(item)
    selected_item_file_lines = get_file_lines(selected_item_save_location)
    selected_item_as_string = item_to_string(item)

    # open the old file location in write mode deleting everything from it
    start_file = open(selected_item_save_location, 'w')

    # look at each line to determine if there is a match
    for ln in selected_item_file_lines:
        if ln.strip("\n") != selected_item_as_string.strip("\n"):     # when there isn't a match write the line
            start_file.write(ln)

    start_file.close()    # close the file

    # check if the lost/deleted file exists
    file_existence_filter("Dictionary/lost_or_deleted_items/lost_or_deleted_items.txt")

    # write the selected_item into the lost/deleted file
    end_file = open("Dictionary/lost_or_deleted_items/lost_or_deleted_items.txt", 'a')  # open file
    end_file.write(selected_item_as_string)
    end_file.close()  # close the file


# looks to see if there is a repeat of the given item. (True = Repeat, False = NO repeat)
def check_for_repeats(item):
    is_there_a_repeat = False

    # save necessary info about selected_item
    save_location = get_item_file_directory(item)
    save_file_lines = get_file_lines(save_location)
    item_as_string = item_to_string(item)

    # open the old file location in write mode deleting everything from it
    file = open(save_location, 'r')

    # look at each line to determine if there is a match
    for fi_l in save_file_lines:
        if fi_l.strip("\n") == item_as_string.strip("\n"):  # when the line matches the item
            is_there_a_repeat = True

    file.close()  # close the file

    return is_there_a_repeat


# is used to archive any user added fields
def save_list_of_fields():
    global list_of_fields
    saved_fields_file = open("Dictionary/saved_fields.txt", 'w')
    saved_fields_file.write("_=^=_& Stores all fields so user can select them")

    list_of_fields.sort()

    # removes any random or bad lines and writes all the remaining lines
    i = 0
    while i < len(list_of_fields):
        if list_of_fields[i].rstrip() == "":
            list_of_fields.pop(i)
        else:
            saved_fields_file.write("\n" + list_of_fields[i].rstrip())
            i += 1

    saved_fields_file.close()


# ======================================================================================================================
# ============================================ NOW THE MAIN CODE BODY BEGINS ===========================================
# ======================================================================================================================


list_of_fields = get_file_lines("Dictionary/saved_fields.txt")  # get all the saved fields and put them into a list
list_of_fields.pop(0)   # removes the first item since that is just a title line explaining the file

fe = 0
for fe in range(0, len(list_of_fields)):
    list_of_fields[fe] = list_of_fields[fe].rstrip()


# ---------------------------big title label---------------------------
lab_title = Label(window, text="Dictionary of the Humble First Class Engineer", bg=color_dark,
                  font=("TkDefaultFont", fontsize * 3), relief="ridge", highlightbackground="red", highlightthickness=5)
lab_title.grid(column=0, columnspan=2, row=0, padx=spacing_out_x, pady=spacing_out_y,
               ipadx=spacing_out_x / 2, ipady=spacing_out_y / 2)


# ---------------------------left side frame stuff---------------------------
frm_left = Frame(window, bg=color_dark)
frm_left.grid(column=0, row=1, sticky="n, s, e, w", padx=spacing_out_x, pady=spacing_out_y)
frm_left.grid_rowconfigure(2, weight=1)


# ---------------------------area for check boxes of what to include in search---------------------------
frm_checkbox_holder = LabelFrame(frm_left, text="What to include in the search?",
                                 highlightthickness=1, highlightbackground=accent_light)
frm_checkbox_holder.grid(column=1, row=0, sticky="n, s, e, w")
frm_checkbox_holder.grid_columnconfigure(0, weight=1)
frm_checkbox_holder.grid_columnconfigure(1, weight=1)

# frame that holds the checkboxes with the types of items to look though along with checkboxes
frm_item_type_checkboxs = LabelFrame(frm_checkbox_holder, text="Item Types:",
                                     highlightthickness=1, highlightbackground=accent_light)
frm_item_type_checkboxs.grid(column=0, row=0, sticky="n, s, e, w", pady=spacing_in * 2, padx=spacing_in * 2)
# checkboxes for the various areas one can search
Checkbutton(frm_item_type_checkboxs, text="Logic", variable=search_logic) \
    .grid(column=0, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Variables", variable=search_variables) \
    .grid(column=1, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Constants", variable=search_constants) \
    .grid(column=2, row=0, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Equations", variable=search_equations) \
    .grid(column=0, row=1, sticky="n, s, e, w")
Checkbutton(frm_item_type_checkboxs, text="Methods", variable=search_methods) \
    .grid(column=2, row=1, sticky="n, s, e, w")

# frame that holds the checkboxes with the places to look though along with checkboxes
frm_places_checkboxs = LabelFrame(frm_checkbox_holder, text="Places to Look:",
                                  relief=relief_style, highlightthickness=1, highlightbackground=accent_light)
frm_places_checkboxs.grid(column=1, row=0, rowspan=2, sticky="n, s, e, w", pady=spacing_in * 2, padx=spacing_in * 2)
# checkboxes for the various areas one can search
Checkbutton(frm_places_checkboxs, text="Name", variable=search_names) \
    .grid(column=0, row=0, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Description", variable=search_description) \
    .grid(column=1, row=0, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Symbol", variable=search_symbol) \
    .grid(column=0, row=1, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Value", variable=search_value) \
    .grid(column=1, row=1, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Units", variable=search_units) \
    .grid(column=0, row=2, sticky="n, s, e, w")
Checkbutton(frm_places_checkboxs, text="Field", variable=search_field) \
    .grid(column=1, row=2, sticky="n, s, e, w")

# button to show everything from the selected item types
btn_search = Button(frm_checkbox_holder, text="Show everything from selected item types.", command=print_all)

btn_search.grid(column=0, row=1, sticky="n, s, e, w", padx=spacing_in * 1.45, pady=spacing_in * 1.45)

# ---------------------------area for text input to search stuff---------------------------
# the frame for the accompanying stuff to go in
frm_input = LabelFrame(frm_left, text="What do you want to search for?",
                       highlightthickness=1, highlightbackground=accent_light, highlightcolor=accent_light)
frm_input.grid(column=1, row=1, sticky="n, s, e, w", pady=spacing_out_y * 2)

# text box to get user input
txt_search = Entry(frm_input, highlightthickness=1, highlightbackground=accent_light)
txt_search.grid(column=0, columnspan=2, row=1, sticky="n, s, e, w", padx=spacing_in, pady=spacing_in)
txt_search.bind("<Return>", lambda x: search())  # allows user to press enter to search

# button to begin searching. Calls the "print_search" function that starts the process of printing results
btn_search = Button(frm_input, text="Search", command=search, activeforeground=text_color)
btn_search.grid(column=1, row=1, sticky="n, s", padx=spacing_in, pady=spacing_in)

# this stuff is for sorting out the resizing of the textbox so that its always as wide as it needs to be
frm_input.grid_columnconfigure(0, weight=1)

# ---------------------------area for search results---------------------------
# wrapper frame for everything going into the search results area
frm_results = LabelFrame(frm_left, text="Search results", highlightthickness=1, highlightbackground=accent_light)
frm_results.grid(column=1, row=2, sticky="n, s, e, w")
# this stuff is for sorting out the resizing of the middle row and frm_results_scroll_wrapper
frm_results.grid_rowconfigure(1, weight=1)

# the frame that will hold the information about the columns
frm_results_titlerow = Frame(frm_results, highlightthickness=1, highlightbackground=accent_light)
frm_results_titlerow.grid(column=0, columnspan=2, row=0, sticky="w")

# the frame that will hold the canvas and all the other scrolling shite
frm_results_scroll_wrapper = Frame(frm_results, highlightthickness=1, highlightbackground=accent_light)
# reveals the frame holding the scrollbar, canvas, and wrapping frame
frm_results_scroll_wrapper.grid(column=0, columnspan=2, row=1, sticky="n, s, e, w")
# configures the row with the canvas to be able to expand
frm_results_scroll_wrapper.grid_rowconfigure(0, weight=1)
frm_results_scroll_wrapper.grid_columnconfigure(0, weight=1)

# the canvas that will enable the possibility to scroll through the various search results
canv_results = Canvas(frm_results_scroll_wrapper)
# frame in which the results will be listed
frm_results_inner = Frame(canv_results, bg=color_mid)
# scroll bar that will can scroll through results shown in frm_results_inner on the canvas
srlb_results = Scrollbar(frm_results_scroll_wrapper, orient="vertical", command=canv_results.yview)

# configures the canvas to include a scrolling command linked to the scrollbar
canv_results.configure(yscrollcommand=srlb_results.set)

# write out everything for the search results. They won't show up because
canv_results.grid(column=0, row=0, sticky="n, s, e, w")
srlb_results.grid(column=1, row=0, sticky="n, s, e, w")

# creates a window in which the frame is placed. This allows the frame to be scrolled through
canv_results.create_window((0, 0), window=frm_results_inner, anchor='nw')

# calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
frm_results_inner.bind("<Configure>", lambda e: canv_results.configure(scrollregion=canv_results.bbox("all")))

# create the button that will be used to add more items
btn_add_item = Button(frm_results, text="Add a new item", command=lambda: add_edit_item_window(False),
                      activeforeground=text_color)
btn_add_item.grid(column=1, row=2, sticky="e")

# create the button that will be used to delete more items
btn_delete_item = Button(frm_results, text="Delete selected item", activeforeground=text_color,
                         command=item_delete_ask_user, state="disabled")
btn_delete_item.grid(column=0, row=2, sticky="w")

# print column titles for easier user understanding
lab_result_name = Label(frm_results_titlerow, bg=color_light, text="Name", anchor="center")
lab_result_name.grid(row=0, column=0, padx=spacing_out_x * 4, sticky="w")
lab_result_info = Label(frm_results_titlerow, bg=color_light, text="Information", anchor="center")
lab_result_info.grid(row=0, column=1, padx=spacing_out_x * 10)
btn_clear_results = Button(frm_results_titlerow, text="Clear Results", anchor="center", command=destroy_search_results)
btn_clear_results.grid(row=0, column=2)

# this is for spacing the titles to fit properly
srlb_results.update()
lab_result_spacing = Label(frm_results_titlerow, text="", width=int(srlb_results.winfo_width() / m_len),
                           background=color_light)
lab_result_spacing.grid(row=0, column=3)


# ---------------------------area to display item information---------------------------
frm_info = Frame(window)    # the frame for the accompanying stuff to go in
frm_info.grid(column=1, row=1, sticky="n, s, e, w", padx=spacing_out_x, pady=spacing_out_y)

# the outer frame that will hold all information stuff
frm_info_scroll_wrapper = Frame(frm_info, bg=color_mid, highlightthickness=1, highlightbackground=accent_light)
# the canvas that will enable the possibility of scrolling through the info
canv_info = Canvas(frm_info_scroll_wrapper)
# frame in which the info will be placed
frm_info_inner = Frame(canv_info)

# scroll bar that will can scroll through the info shown in frm_info_inner on the canvas
srlb_info = Scrollbar(frm_info_scroll_wrapper, orient="vertical", command=canv_info.yview)
# configures the canvas to include a scrolling command linked to the scrollbar
canv_info.configure(yscrollcommand=srlb_info.set)

# display in everything for the search results. They won't show up because frm_info_scroll_wrapper is not displayed yet
canv_info.grid(column=0, row=0, sticky="n, s, e, w")
srlb_info.grid(column=1, row=0, sticky="n, s, e, w")

# creates a window in which the frame is placed. This allows the frame to be scrolled through
canv_info.create_window((0, 0), window=frm_info_inner, anchor='nw')

# calls the function that will actually enable the scrolling. I don't understand why this works so leave it alone
frm_info_inner.bind("<Configure>",
                    lambda e: canv_info.configure(scrollregion=canv_info.bbox("all")))

# this stuff is for sorting out the resizing of the frame holding the scrolling canvas
frm_info.grid_columnconfigure(0, weight=1)
frm_info.grid_rowconfigure(0, weight=1)
frm_info_scroll_wrapper.grid_columnconfigure(0, weight=1)
frm_info_scroll_wrapper.grid_rowconfigure(0, weight=1)
frm_info_inner.grid_columnconfigure(0, weight=1)
frm_info_inner.grid_columnconfigure(1, weight=1)
frm_info_inner.grid_columnconfigure(2, weight=1)


frm_info_scroll_wrapper.grid(column=0, row=0, sticky="n, s, e, w")


selected_item = Method("", "", "", "", [""])


# ---------------------------keeping the window open and some widget sizing stuff---------------------------
window.mainloop()  # keeps the window open

# extra stuff that could come in handy
# frm_info.update()  # need to call this to get the size of the item
# print(str(frm_info.winfo_width()))
# print(str(lab_search.winfo_height()))

####################################################
#                                                  #
# VICS-Gallery-Maker                               #
# A tool to make a gallery from a VICS JSON Export #
#                                                  #
#                                        by Lemmy  #
#                                                  #
####################################################

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image
import webbrowser
import json
import os
import sys

Image.MAX_IMAGE_PIXELS = None

def browse_button():
    file_dialog = filedialog.Open(filetypes=[("JSON Files", "*.json")])
    result = file_dialog.show()
    if result != '':
        count_display_label.config(text="Parsing json... ")
        prop_listbox.delete(0, tk.END)
        selected_file_path = file_dialog.filename
        json_entry.delete(0, tk.END)
        json_entry.insert(0, selected_file_path)
        
        # Process the JSON file
        with open(selected_file_path) as file:
            try:
                json_object = json.load(file)
                unique_count = len(json_object["value"][0]["Media"])
                total_count = sum(len(media["MediaFiles"]) for media in json_object["value"][0]["Media"])
            except (KeyError, json.JSONDecodeError):
                unique_count = 0
                total_count = 0
        if unique_count > 0 and total_count > 0:
            count_display_label.config(text=f"Json seems valid --> {total_count} files - {unique_count} uniques & fields extracted")
            unique_items = []
            unique_set = set()
            for media in json_object["value"][0]["Media"]:
                for key in media.keys():
                    if key not in ["MediaID", "RelativeFilePath", "Exifs", "MediaFiles"] and key not in unique_set:
                        unique_items.append(key)
                        unique_set.add(key)
            for media in json_object["value"][0]["Media"]:
                for key in media.keys():
                    if key in ["Exifs"]:
                        for exif in media["Exifs"]:
                            for key in exif.keys():
                                if (key == "PropertyName") and exif[key] not in unique_set:
                                    unique_items.append(f"_Exif {exif[key]}")
                                    unique_set.add(exif[key])
            for media in json_object["value"][0]["Media"]:
                for key in media.keys():
                    if key in ["MediaFiles"]:
                        for media_file in media["MediaFiles"]:
                            for key in media_file.keys():
                                if key != "MD5" and key not in unique_set:
                                    unique_items.append(f"_MediaFiles {key}")
                                    unique_set.add(key)
            prop_listbox.delete(0, tk.END)
            for item in unique_items:
                prop_listbox.insert(tk.END, item)
            ok_button.config(state=tk.NORMAL)
            select_all_button.config(state=tk.NORMAL)
            select_none_button.config(state=tk.NORMAL)
            select_all_exif_button.config(state=tk.NORMAL)
            select_no_exif_button.config(state=tk.NORMAL)
            select_all_media_button.config(state=tk.NORMAL)
            select_no_media_button.config(state=tk.NORMAL)
        else:
            count_display_label.config(text="Json doesn't seem valid")
            ok_button.config(state=tk.DISABLED)

def cancel_button_click():
    form.destroy()

def ok_button_click():
    selected_file_path = json_entry.get()
    with open(selected_file_path, 'r') as json_file:
        json_content = json_file.read()
        json_object = json.loads(json_content)
    html_file_path = selected_file_path.rsplit( ".", 1 )[ 0 ] + ".html"
    td_width = 100 // int(column_nb_entry.get())

    write_html_header(html_file_path)

    with open(html_file_path, 'a', encoding="utf-8") as file:
        file.write('<table border="1" cellpadding="5" cellspacing="0" width="100%">\n')
        is_first_exif = True
        is_first_media = True
        is_first_media_property = True
        i = 1
        file.write('<tr>')
        for obj in json_object['value'][0]['Media']:
            file.write(f'<td width="{td_width}%" valign="top" class="wrap">')
            file.write(f'<b>#{obj["MediaID"]}</b><br>\n')
            if obj["MimeType"].startswith("image"):
                image = Image.open(os.path.dirname(selected_file_path) + "/" + obj["RelativeFilePath"])
                w, h = image.size
                if (w > int(pic_max_size_entry.get()) or h > int(pic_max_size_entry.get())):
                    image.thumbnail((int(pic_max_size_entry.get()), int(pic_max_size_entry.get())))
                    image.save(os.path.dirname(selected_file_path)  + "/" + obj["RelativeFilePath"].rsplit( ".", 1 )[ 0 ] + ".thumb.jpg")
                    file.write(f'<a href="{obj["RelativeFilePath"]}" target="_blank"><img src="{obj["RelativeFilePath"].rsplit( ".", 1 )[ 0 ] + ".thumb.jpg"}" border=1></a><br>\n')
                else:
                    file.write(f'<a href="{obj["RelativeFilePath"]}" target="_blank"><img src="{obj["RelativeFilePath"]}" border=1></a><br>\n')
            else:
                file.write(f'<a href="{obj["RelativeFilePath"]}">Link</a><br>\n')
            selected_items = prop_listbox.curselection()
            selected_items_text = []
            for item in selected_items:
                selected_items_text.append(prop_listbox.get(item))
            for item in selected_items_text:
                if item in obj and obj[item]:
                    file.write(f"- {item}: {obj[item]}<br>\n")
                if item.startswith("_Exif "):
                    exif_property = item[6:]
                    if "Exifs" in obj:
                        for exif in obj["Exifs"]:
                            if exif["PropertyName"] == exif_property:
                                if is_first_exif:
                                    file.write("- Exif(s):<br>\n")
                                    is_first_exif = False
                                if (exif_property == "GPS Longitude"):
                                    longitude = exif['PropertyValue']
                                if (exif_property == "GPS Latitude" and"_Exif GPS Longitude" in selected_items_text):
                                    latitude = exif['PropertyValue']
                                    file.write(f'&nbsp;&nbsp;&nbsp;&nbsp;- {exif_property}: {exif["PropertyValue"]} (<a href="http://www.openstreetmap.org/?mlat={latitude}&mlon={longitude}" target="_blank">osm link</a> - <a href="https://google.com/maps?q=loc:{latitude},{longitude}" target="_blank">gmaps link</a>)<br>\n')
                                else:
                                    file.write(f'&nbsp;&nbsp;&nbsp;&nbsp;- {exif_property}: {exif["PropertyValue"]}<br>\n')
            j = 0
            for obj in obj["MediaFiles"]:
                for item in selected_items_text:
                    if item.startswith("_MediaFiles "):
                        item = item[12:]
                        if is_first_media:
                            if all_files_Checkbutton_state.get():
                                file.write("- File(s):<br>\n")
                            else:
                                file.write("- File:<br>\n")
                            is_first_media = False
                        if (all_files_Checkbutton_state.get() and is_first_media_property):
                            file.write(f"&nbsp;&nbsp;&nbsp;&nbsp;- File #{j}:<br>\n")
                            is_first_media_property = False
                        if item in obj:
                            if all_files_Checkbutton_state.get():
                                file.write("&nbsp;&nbsp;&nbsp;&nbsp;")
                            file.write(f"&nbsp;&nbsp;&nbsp;&nbsp;- {item}: {obj[item]}<br>\n")
                if not all_files_Checkbutton_state.get():
                    break
                is_first_media_property = True
                j += 1
            is_first_exif = True
            is_first_media = True
            file.write("</td>\n")
            if i % int(column_nb_entry.get()) == 0:
                file.write("</tr><tr>\n")
            i += 1
        file.write('</tr>\n')
        file.write('</table>\n')
    write_html_footer(html_file_path)
    http_callback(html_file_path)
    form.destroy()

def write_html_header(html_file_path):
    with open(html_file_path, 'w', encoding="utf-8") as file:
        file.write("<html><head>\n")
        file.write("<title>Report</title>\n")
        file.write('<meta name="GENERATOR" content="VICS-Gallery-Maker">\n')
        file.write('<style type="text/css">td {font-size: ' + font_size_entry.get() + 'px;font-weight: lighter;} img {max-width: ' + pic_max_size_entry.get() +'; max-height: '+ pic_max_size_entry.get() + ';} .wrap {word-wrap:break-word;max-width:250px}</style>\n')
        file.write("</head><body>\n")

def write_html_footer(html_file_path):
    with open(html_file_path, 'a', encoding="utf-8") as file:
        file.write("</body>\n</html>")

def http_callback(url):
    webbrowser.open_new(url)

def select_all():
    prop_listbox.select_set(0, tk.END)

def select_none():
    prop_listbox.select_clear(0, tk.END)

def select_all_exif():
    values = prop_listbox.get(0, tk.END)
    i = 0
    for value in values:
        if value.startswith("_Exif "):
            prop_listbox.select_set(i)
        i += 1

def select_no_exif():
    values = prop_listbox.get(0, tk.END)
    i = 0
    for value in values:
        if value.startswith("_Exif "):
            prop_listbox.select_clear(i)
        i += 1

def select_all_media():
    values = prop_listbox.get(0, tk.END)
    i = 0
    for value in values:
        if value.startswith("_MediaFiles "):
            prop_listbox.select_set(i)
        i += 1

def select_no_media():
    values = prop_listbox.get(0, tk.END)
    i = 0
    for value in values:
        if value.startswith("_MediaFiles "):
            prop_listbox.select_clear(i)
        i += 1


# Create the main window
form = tk.Tk()
form.title("VICS-Gallery-Maker")
form.geometry("350x485")
form.resizable(False, False)

input_labelframe = tk.LabelFrame(form, text="Input")
input_labelframe.pack(side=tk.TOP,padx=5, pady=2, fill="x")
count_display_label = tk.Label(input_labelframe, anchor="w", text="N/A files - N/A uniques (open the json first)")
count_display_label.pack(side=tk.BOTTOM,padx=5, pady=2, fill="x")
json_label = tk.Label(input_labelframe, text="Json file:")
json_label.pack(side=tk.LEFT, padx=5, pady=2)
json_entry = tk.Entry(input_labelframe,width=37)
json_entry.pack(side=tk.LEFT,padx=5, pady=2)
browse_button = tk.Button(input_labelframe, text="...", width=3, height=1, command=browse_button)
browse_button.pack(side=tk.RIGHT,padx=5, pady=2)

param_labelframe = tk.LabelFrame(form, text="Param")
param_labelframe.pack(padx=5, pady=2, fill="x")
param_frame1 = tk.LabelFrame(param_labelframe,borderwidth = 0, highlightthickness = 0)
param_frame1.pack(side=tk.TOP,padx=5, pady=2, fill="x")
param_frame2 = tk.LabelFrame(param_labelframe,borderwidth = 0, highlightthickness = 0)
param_frame2.pack(padx=5, pady=2, fill="x")
param_frame3 = tk.LabelFrame(param_labelframe,borderwidth = 0, highlightthickness = 0)
param_frame3.pack(side=tk.BOTTOM,padx=5, pady=2, fill="x")

column_nb_entry = tk.Entry(param_frame1, width=2 )
column_nb_entry.insert(tk.END, "3")
column_nb_entry.pack(side=tk.LEFT,padx=5, pady=2)
files_per_line_label = tk.Label(param_frame1,text="files per line")
files_per_line_label.pack(side=tk.LEFT,padx=5, pady=2)
font_size_entry = tk.Entry(param_frame1, width=2)
font_size_entry.insert(tk.END, "12")
font_size_entry.pack(side=tk.RIGHT,padx=5, pady=2)
font_size_label = tk.Label(param_frame1, anchor="e", text="Font size:")
font_size_label.pack(side=tk.RIGHT,padx=5, pady=2)

pic_dim_label = tk.Label(param_frame2, text="Max dimension of pictures:")
pic_dim_label.pack(side=tk.LEFT,padx=5, pady=2)
pic_max_size_entry = tk.Entry(param_frame2, width=4)
pic_max_size_entry.insert(tk.END, "250")
pic_max_size_entry.pack(side=tk.LEFT,padx=5, pady=2)
pixels_label = tk.Label(param_frame2, anchor="w", text="pixels")
pixels_label.pack(side=tk.LEFT,padx=5, pady=2)
all_files_Checkbutton_state = tk.BooleanVar()
all_files_Checkbutton = tk.Checkbutton(param_frame3, anchor="w", text="Output all files (not only the first one)",variable=all_files_Checkbutton_state)
all_files_Checkbutton.select()
all_files_Checkbutton.pack(side=tk.TOP,padx=5, pady=2, fill="x")
fields_label = tk.Label(param_frame3,anchor="w", text="Fields to Output:")
fields_label.pack(side=tk.TOP,padx=5, pady=2, fill="x")
prop_listbox = tk.Listbox(param_frame3, selectmode=tk.MULTIPLE, width=35, height=11)
prop_listbox.pack(side=tk.LEFT,padx=5, pady=2, fill="x")
select_all_button = tk.Button(param_frame3, text="Select all", command=select_all, state=tk.DISABLED)
select_all_button.pack(padx=5, pady=2, fill="x")
select_none_button = tk.Button(param_frame3, text="Select none", command=select_none, state=tk.DISABLED)
select_none_button.pack(padx=5, pady=2, fill="x")
select_all_exif_button = tk.Button(param_frame3, text="Select all exif", command=select_all_exif, state=tk.DISABLED)
select_all_exif_button.pack(padx=5, pady=2, fill="x")
select_no_exif_button = tk.Button(param_frame3, text="Select no exif", command=select_no_exif, state=tk.DISABLED)
select_no_exif_button.pack(padx=5, pady=2, fill="x")
select_all_media_button = tk.Button(param_frame3, text="Select all media", command=select_all_media, state=tk.DISABLED)
select_all_media_button.pack(padx=5, pady=2, fill="x")
select_no_media_button = tk.Button(param_frame3, text="Select no media", command=select_no_media, state=tk.DISABLED)
select_no_media_button.pack(padx=5, pady=2, fill="x")

button_frame = tk.Frame(form)
button_frame.pack(side=tk.BOTTOM,padx=5, pady=2)
cancelButton = tk.Button(button_frame, text="Cancel", width=7, command=cancel_button_click)
cancelButton.pack(side=tk.LEFT,padx=5, pady=2)
ok_button = tk.Button(button_frame, text="OK", width=7, command=ok_button_click, state=tk.DISABLED)
ok_button.pack(side=tk.RIGHT,padx=5, pady=2)

info_labelframe = tk.LabelFrame(form, text="Infos & docs")
info_labelframe.pack(side=tk.BOTTOM,padx=5, pady=2, fill="x")
link_label = tk.Label(info_labelframe,anchor="w", text="https://github.com/lemnet/VICS-Gallery-Maker", width=52,fg="blue", cursor="hand2")
link_label.pack(padx=5, pady=2, fill="x")
link_label.bind("<Button-1>", lambda e: http_callback("https://github.com/lemnet/VICS-Gallery-Maker"))


form.iconbitmap(sys.executable)
form.mainloop()
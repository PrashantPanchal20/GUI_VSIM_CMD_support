import sys
sys.path.append( ' ...../.local/lib/python2.7/site-packages' )

import pandas as pd

import tkinter
from tkinter import ttk
# import read_file as rd
#=================================================Read files path =============================================
from os.path import isdir, join , isfile
from os import listdir
import autocompletecombobox as autocomp
import confluence_page as con_page
from confluence_page import confluence_data
import os,time, glob
import sys
import re

addition_def = []
addition_arg = []
opset = ""

def function_TB():
    tb = []
    mypath = "..............#dir path"
    tbs = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    for dir in tbs:
        extentions = "verilog.e5ca."
        if dir.startswith(extentions):
            tb.append(dir)
    return tb

# def _regs_list():
#     data = []
#     var1 = open("#path.run","r").readlines()
#     for line in var1:
#         data.append(line)
#     # var1 = "...................."
#     # data = [f for f in listdir(var1) if isfile(join(var1, f))]
#     return data

def _regs_list():
    regs = []
    regs_dir = ["#regpath", "select_options"]
    for items in regs_dir:
        for subdir, dirs, files in os.walk(items):
            for file in files:
                extentions = ".run"
                if file.endswith(extentions):
                    regs.append(file.strip(".run"))
    return regs
#======================================CMD Exicutions and database =========================================
def get_netlist():
    global netlist__, netlist1
    netlist1 = list()
    selection = netlist_list.curselection()
    for i in selection:
        entrada = netlist_list.get(i)
        netlist1.append(entrada)
    for netlist2 in netlist1:
        netlist2 = ','.join(netlist1)
        netlist__ = f'-S Netlist/{netlist2}'

def dir_prefix():
    global dir_set, reg, dir_, dir_name 
    dir_set = ""
    reg = regression_combobox.get()
    dir_= dirpath_entry.get()
    # date = time.strftime("%b_%d")
    # netlist1 = '............'
    netlist_src = re.compile(r'.*(TT|JFF|JSS|JSF|JFS).*(M10C|110C).*(B9b5aF|e5caF).*_([a-zA-Z]+\d+)_.*')
    str_change = f'{netlist1}'

    corner = netlist_src.search(str_change).group(1)
    temp = netlist_src.search(str_change).group(2)
    # proj = netlist_src.search(str_change).group(3)
    n_date = netlist_src.search(str_change).group(4)

    dir_set = corner+"_"+temp+"_"+n_date
    dir_name = f'{dir_}/log_{dir_set}_{reg}'

opset_list = ""
def opset_conf():
    global opset_list
    mode_value = mode_select_combobox.get()
    config = config_combobox.get()

    if (mode_value == "DA1500"):
        config_subsed = "ALL"

    elif (config == "x64_if") or (config == "x64_daprb") or (config == "x64_if_hd"):
        config_subsed = "IF"

    elif (config == "x64_core") or (config == "x64_core_hd"):
        config_subsed = "CUBE CORE"

    else:
        config_subsed = "CUBE"

    table_opset = con_page.table_opset_dataframe
    opts = pd.DataFrame(table_opset)
    conf_mode = opts.values.tolist()

    for item in conf_mode:
        if(mode_value.lower() in item[0].lower()) and (config_subsed.lower() in item[1].lower()):
            opset_list = item[2]

def mode_select_trigg(event):
    global opset_txt, txtbox_opset
    txtbox_opset = f'{event.widget.get()}'
    opset_conf()
    opset_txt.delete(1.0,'end')
    opset_txt.insert('1.0',f'{opset_list}') 
    

def Generate_CMD():
    get_netlist()
    def_arg_opset()
    dir_prefix()

    global depth, user_cmd, config_ ,VSIM_CMD, netlist_
 
    config_ = config_combobox.get()
    depth = depth_combobox.get()

    addition_arg_ = " +".join([str(number) for number in addition_arg])
    if(addition_arg_ != ""):
        add_arg = f'-o "+{addition_arg_}"'
    else:  add_arg = ''

    addition_def_ = "+".join([str(number) for number in addition_def])
    if(addition_def_ != ""):
        add_def = f' -o "+define+{addition_def_}"'
    else:  add_def = ''

    if(addition_def == "NO_CHIP"):
        netlist_ = ''
    else:
        netlist_ = netlist__

    # op_set = (f"   #opset")
    VSIM_CMD = (f'vsim_snap -r {reg.strip()} -x {config_.strip()} -l {dir_name.strip()} -Y {depth.strip()} -o "{opset_list.strip()}" {add_arg.strip()}{add_def} {netlist_}')

    cmd_info.insert('1.0',f'{VSIM_CMD}')
    cmd_info.config(state='disable')
    tb_entry.set("")
    regression_combobox.set("")
    list_arg.delete(0,tkinter.END)
    depth_combobox.set("")
    dirpath_entry.delete(0,'end')
    config_combobox.set("")
    list_def.delete(0,tkinter.END)

def netlist_callbackfunc(event):

    global tb_, netlist_list
    tb_ = f'{event.widget.get()}'
    onlyfiles = []
    mypath = f".....#...TBpath/{tb_}/Netlist/"
    # print("tb_ inside function netlist = %s"%(tb_))
    onlyfiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    netlist_list.delete(0, tkinter.END)
    for onlyfile in onlyfiles:
        netlist_list.insert(tkinter.END,onlyfile)

def def_arg_opset():
    global addition_arg, addition_def

    for idx in list_arg.curselection():
        addition_arg.append(list_arg.get(idx))
        # print(list_arg.get(idx))
    
    for idx in list_def.curselection():
        addition_def.append(list_def.get(idx))
        # print(addition_def)

def Config_opset_function(event):
    global config, mat
    config = f'{event.widget.get()}'
    update_opts_box(config)

conf_mode_sublist = []
def update_opts_box(config):
    global conf_mode_sublist, mode_select_combobox, conf_mode

    if (config == "x64_if") or (config == "x64_daprb") or (config == "x64_if_hd"):
        config_subsed = "IF"

    elif (config == "x64_core") or (config == "x64_core_hd"):
        config_subsed = "CUBE CORE"

    else:
        config_subsed = "CUBE"

    table_opset = con_page.table_opset_dataframe
    opts = pd.DataFrame(table_opset)
    conf_mode = opts.values.tolist()
    conf_mode_sublist.clear()

    for item in conf_mode:
        if (config_subsed.lower() in item[1].lower()) or (item[1].lower() == "all"):
            conf_mode_sublist.append(item[0])     

def run_cmd():
    global change_tb
    change_tb = f'#tb_path/{tb_}' 
    os.chdir(change_tb) 
    x = f'{os.chdir(change_tb)}'
    os.system(x)  
    os.system(VSIM_CMD)
    sys.exit()
#======================================================================= Design ==================================================
window = tkinter.Tk()
window.title("Vsim CMD Support")
window.geometry("1250x900")
# window.resizable(0,0)

note = ttk.LabelFrame(window,text = "Please Enter All Details [ Note :: Terminal should be updated ]",height=20)
note.pack(fill="both",pady=10,anchor='center')

user_info_frame = tkinter.Frame(window)
user_info_frame.pack(fill="both",pady=25,anchor='center')

select_tb = ttk.Label(user_info_frame, text="Please select your TB here *:: ")
select_tb.grid(row=0, column=0, padx=30, pady=5)

tb_entry = autocomp.AutocompleteCombobox(user_info_frame, completevalues=function_TB())
tb_entry.grid(row=1, column=0)
tb_entry.current()
tb_entry.bind("<<ComboboxSelected>>", netlist_callbackfunc)


regression_name = ttk.Label(user_info_frame, text="Regression * :: ")
regression_name.grid(row=0, column=1)
# regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, values=function1())
regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, completevalues=_regs_list())
regression_combobox.grid(row=1, column=1, padx=20, pady=5)

config_label = tkinter.Label(user_info_frame, text="Configuration *:: ")
config_label.grid(row=0, column=2)

config_combobox = ttk.Combobox(user_info_frame, values=("x64_if","x64_core","x64_4h","x64_8h","x64_if_hd","x64_core_hd","x64_4h_hd","x64_4ha","x64_4ha_hd","x64_4he","x64_4he_hd","x64_8h_hd","x64_12h","x64_12h_hd","x64_16h","x64_16h_hd","x64_daprb"))
config_combobox.grid(row=1, column=2, padx=20, pady=5)
config_combobox.bind("<<ComboboxSelected>>", Config_opset_function)

depth = tkinter.Label(user_info_frame, text="Depth :: ")
depth.grid(row=0, column=3)

depth_combobox = ttk.Combobox(user_info_frame, values=("99999","19999","19995"))
depth_combobox.grid(row=1, column=3, padx=20, pady=5)
depth_combobox.set('99999')

mode_select = tkinter.Label(user_info_frame, text="Confirem Mode :: ")
mode_select.grid(row=0, column=4, padx=20, pady=5)
mode_select_combobox = ttk.Combobox(user_info_frame,values=conf_mode_sublist,postcommand=lambda: mode_select_combobox.configure(values=conf_mode_sublist))
mode_select_combobox.grid(row=1, column=4, padx=20, pady=5)
mode_select_combobox.bind("<<ComboboxSelected>>", mode_select_trigg)

dir_path = tkinter.Label(user_info_frame, text="Enter Log Dir Name Here *:: ")
dir_path.grid(row=0, column=5, padx=20, pady=5)

dirpath_entry = tkinter.Entry(user_info_frame,textvariable="")
dirpath_entry.grid(row=1, column=5, padx=20, pady=5)


# ========================================================= define and args list boxes  =========================================

user_select_frame = ttk.LabelFrame(window, text="Select +defines and +args ::",padding=10)
user_select_frame.pack(fill="x")

user_def_frame = ttk.LabelFrame(user_select_frame, text="+def ::")
user_def_frame.pack(side = "left",fill="x",expand=True)

yscrollbar_def = ttk.Scrollbar(user_def_frame)
yscrollbar_def.pack(side = "right", fill = "y")
listdef_ = tkinter.StringVar(value=con_page.defines)
list_def = tkinter.Listbox(user_def_frame,listvariable = listdef_, background="black", foreground="cyan",height=15, selectmode = tkinter.MULTIPLE,yscrollcommand = yscrollbar_def.set)
list_def.pack(padx = 1, pady = 1, expand = 'yes', fill = "both",anchor="w")
yscrollbar_def.config(command = list_def.yview)
list_def.configure(exportselection=False)

user_args_frame = ttk.LabelFrame(user_select_frame, text="+args ::")
user_args_frame.pack(side = "right",fill="x",expand=True)
yscrollbar_arg = ttk.Scrollbar(user_args_frame)
yscrollbar_arg.pack(side = "right", fill = "y")
listargs_ = tkinter.StringVar(value=con_page.args)
list_arg = tkinter.Listbox(user_args_frame,listvariable=listargs_,background="black", foreground="cyan",height=15, selectmode = tkinter.MULTIPLE,yscrollcommand = yscrollbar_arg.set)
list_arg.pack(padx = 1, pady = 1, expand = 'yes', fill = "both",anchor="center")
yscrollbar_arg.config(command = list_arg.yview)
list_arg.configure(exportselection=False)

opset_frame = tkinter.LabelFrame(window, text="Selected +op_set is:: ")
opset_frame.pack(fill="x",expand=True, pady=1,side="top",anchor="n",padx=1)
opset_txt = tkinter.Text(opset_frame, height=5 , font="Arial 14")
opset_txt.pack(side="top",fill="x")
# ==================================================================== Netlist box =================================
netlist_frame = tkinter.LabelFrame(window, text="Netlist :: ")
netlist_frame.pack(fill="x",expand=True, pady=1,side="top",anchor="n",padx=1)

netlist_scroller = ttk.Scrollbar(netlist_frame)
netlist_scroller.pack(side = "right", fill = "y")

netlist_list = tkinter.Listbox(netlist_frame, listvariable = netlist_callbackfunc,background="black", foreground="cyan",selectmode = tkinter.MULTIPLE,yscrollcommand = netlist_scroller.set, height=6, width=97)
# netlist_combopicker.grid(row=0,column=0, padx=5, pady=5, columnspan = 3)
netlist_list.pack(padx = 1, pady = 1, expand = 'yes', fill = "x")
netlist_scroller.config(command= netlist_list.yview)

# ----------------------------------------------------------------------generate button ------------------------------------------------------------
button_frame = tkinter.Frame(window)
button_frame.pack(fill="both")
button = tkinter.Button(button_frame, text="Generate Command",command=Generate_CMD, width=97,bg='#F0F8FF', activeforeground='red')
button.pack(side="top",fill="x",anchor="n")
#-------------------------------------------------------- Lounch CMD =============================================

user = tkinter.LabelFrame(window,text = "CMD is ::")
user.pack(side="top",fill="x")

cmd_info = tkinter.Text(user, height=6)
cmd_info.pack(side="top",fill="x")
cmd_info.xview_scroll(1, 'units')

button_frame = tkinter.Frame(window)
button_frame.pack(fill="x")
button1 = tkinter.Button(button_frame, text="Launch CMD",command=run_cmd, width=97,bg='#F0F8FF', activeforeground='red')
button1.pack(side="top",fill="x",anchor="ne")

window.mainloop()


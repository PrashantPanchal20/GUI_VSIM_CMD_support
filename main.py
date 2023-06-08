import tkinter
from tkinter import ttk
# import read_file as rd
#=================================================Read files path =============================================
from os.path import isdir, join , isfile
from os import listdir
import autocompletecombobox as autocomp
import multiselectoption as msop
import os
import sys


def function_TB():
    tb = ''
    mypath = "/runs/simrun_tav/e5ca/REV/ppanchal/"
    tb = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    return tb

def function1():
    data = []
    var1 = open("/runs/simrun_tav/e5ca/REV/TAV/verilog.e5ca.IF_Apr21/E5CA/HBM3/Regressions/VE2VA/extended_moura_long.run","r").readlines()
    for line in var1:
        data.append(line)
    # var1 = "/runs/simrun_tav/e5ca/REV/TAV/verilog.e5ca.IF_Apr21/E5CA/HBM3/Regressions/VE2VA/"
    # data = [f for f in listdir(var1) if isfile(join(var1, f))]
    return data

#======================================CMD Exicutions and database =========================================

def register():
    global reg, arg, dir_, depth, user_cmd, config_ ,VSIM_CMD, addition
 
    reg = regression_combobox.get()
    config_ = config_combobox.get()
    dir_= dirpath_entry.get()
    depth = depth_combobox.get()
    arg = arg_combobox.get()
    addition = additional_combobox.get()

    if(arg != ""):
        dep = f'-o "+{arg}"'
    else:  dep = ''

    if(addition != ""):
        add = f'+{addition}'
    else:  add = ''

    op_set = (f"+define+DAL+FORCE_PPR_RATE+DISCONNECT_UBUMP+CHANS_DISABLED{add} +skip_serial_scan +ignore_precon_data +zero_init2 +speed_grades=2400 +chan_pincomp_delta=100 +rd_post_ui=3 +relax_tXP +set_tIS=100")
    VSIM_CMD = (f'vsim_snap -r {reg.strip()} -x {config_.strip()} -l {dir_.strip()} -Y {depth.strip()} -o "{op_set.strip()}" {dep.strip()}')
    # print(VSIM_CMD)

    cmd_info.insert('1.0',f'{VSIM_CMD}')
    cmd_info.config(state='disable')
    tb_entry.set("")
    regression_combobox.set("")
    arg_combobox.set("")
    depth_combobox.set("")
    dirpath_entry.delete(0,'end')
    config_combobox.set("")
    additional_combobox.set("")

# def get_netlist(event):
#     global net, netlist__
#     net = event.widget.get()
#     netlist__ = f'-S Netlist/{net}'   #use only for at choosen one netlist at combobox

def get_netlist():
    global netlist__
    netlist1 = list()
    selection = netlist_combopicker.curselection()
    for i in selection:
        entrada = netlist_combopicker.get(i)
        netlist1.append(entrada)
    for netlist2 in netlist1:
        netlist2 = ','.join(netlist1)
        netlist__ = f'-S Netlist/{netlist2}'
        # print(netlist__)

def callbackfunc(event):
    global tb_, netlist_combopicker
    tb_ = f'{event.widget.get()}'

    onlyfiles = ""
    # onlyfiles_set = list()
    mypath = f"/runs/simrun_tav/e5ca/REV/ppanchal/{tb_}/Netlist/"
    # print("tb_ inside function netlist = %s"%(tb_))
    onlyfiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]

    # netlist_combopicker = ttk.Combobox(user, values = onlyfiles)
    # # netlist_combopicker = msop.Combopicker(user, values = var_)
    # netlist_combopicker.place(width=400, x=150, y=100)
    # netlist_combopicker.current()
    # netlist_combopicker.bind("<<ComboboxSelected>>", get_netlist)

    onlyfiles_ = tkinter.StringVar(value=onlyfiles)

    netlist_combopicker = tkinter.Listbox(user, listvariable = onlyfiles_, selectmode = tkinter.MULTIPLE, width=20, height=3)
    # netlist_combopicker.bind("<<ListboxSelect>>", get_netlist)
    netlist_combopicker.place(width=400, x=150, y=100)

def run_cmd():
    get_netlist()
    global vsim_net, change_tb, netlist_

    if(addition == "NO_CHIP"):
        netlist_ = ''
    else:
        netlist_ = netlist__
    
    vsim_net = ("{} {}".format(VSIM_CMD, netlist_))
    change_tb = f'/runs/simrun_tav/e5ca/REV/ppanchal/{tb_}'  

    os.chdir(change_tb)
    x = f'{os.chdir(change_tb)}'

    os.system(x)  
    print(vsim_net)
    os.system(vsim_net)
    sys.exit()

#==========================================design==================================================
window = tkinter.Tk()
window.title("Vsim CMD Support")
window.geometry("800x600")
window.resizable(0,0)
frame = tkinter.Frame(window)
frame.pack()

user_info_frame = ttk.LabelFrame(frame,text = "Please Enter All Details Correctly")
user_info_frame.grid(row=0, column=0,padx=20, pady=10)

select_tb = ttk.Label(user_info_frame, text="Please select your TB here *:: ")
select_tb.grid(row=0, column=0, padx=30, pady=5)
 
tb_entry = autocomp.AutocompleteCombobox(user_info_frame, completevalues=function_TB())
tb_entry.grid(row=1, column=0)
tb_entry.current()
tb_entry.bind("<<ComboboxSelected>>", callbackfunc)


regression_name = ttk.Label(user_info_frame, text="Regression * :: ")
regression_name.grid(row=0, column=1)
# regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, values=function1())
regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, completevalues=function1())
regression_combobox.grid(row=1, column=1, padx=20, pady=5)

args = tkinter.Label(user_info_frame, text="New +Args :: ")
args.grid(row=0, column=2)

arg_combobox = ttk.Combobox(user_info_frame, values=function1())
arg_combobox.grid(row=1, column=2, padx=20, pady=5)

dir_path = tkinter.Label(user_info_frame, text="Enter Log Dir Name Here *:: ")
dir_path.grid(row=3, column=0, padx=20, pady=5)

dirpath_entry = tkinter.Entry(user_info_frame,textvariable="")
dirpath_entry.grid(row=4, column=0, padx=20, pady=5)

config_label = tkinter.Label(user_info_frame, text="Configuration *:: ")
config_label.grid(row=3, column=1)

config_combobox = ttk.Combobox(user_info_frame, values=("x64_if","x64_core","x64_4h","x64_8h","x64_if_hd","x64_core_hd","x64_4h_hd","x64_4ha","x64_4ha_hd","x64_4he","x64_4he_hd","x64_8h_hd","x64_12h","x64_12h_hd","x64_16h","x64_16h_hd","x64_daprb"))
config_combobox.grid(row=4, column=1, padx=20, pady=5)
# config_combobox.current()

depth = tkinter.Label(user_info_frame, text="Depth :: ")
depth.grid(row=3, column=2, padx=20, pady=5)

depth_combobox = ttk.Combobox(user_info_frame, values=("99999","19999","19995"))
depth_combobox.grid(row=4, column=2, padx=20, pady=5)
depth_combobox.set('99999')

additional = tkinter.Label(user_info_frame, text="Additional Defines : ")
additional.grid(row=5, column=0, padx=20, pady=5)

additional_combobox = ttk.Combobox(user_info_frame, values=("NO_CHIP","RNX"))
additional_combobox.grid(row=5, column=1, padx=20, pady=5)

button = tkinter.Button(user_info_frame, text="All Done",command=register)
button.grid(row=5, column=2, pady=5)
#--------------------------------------------------------------------------------------

frame1 = tkinter.Frame(window)
frame1.pack()

user = tkinter.LabelFrame(frame1,text = "CMD is ::")
user.grid(row=1, column=0,padx=0, pady=10)

cmd_info = tkinter.Text(user, height=6, width=87)
cmd_info.grid(row=3,column=0, padx=5, pady=5, columnspan = 3)
# cmd_info.config(state='disable')
cmd_info.xview_scroll(1, 'units')

netlist = tkinter.Label(user, text="Netlist :: ")
netlist.grid(row=4, column=0,padx=5, pady=5 )

# print(callbackfunc)
# netlist_combopicker = ttk.Combobox(user, values = callbackfunc)
# netlist_combopicker.bind("<<ComboboxSelected>>", callbackfunc)
# netlist_combopicker = msop.Combopicker(user, values = function_netlist())
# netlist_combopicker.grid(row=4,column=1, pady=5 ,columnspan = 1)
# netlist_combopicker.place(width=400, x=150, y=150)

button1 = tkinter.Button(user, text="RUN",command=run_cmd)
button1.grid(row=6, column=1, pady=10)


window.mainloop()

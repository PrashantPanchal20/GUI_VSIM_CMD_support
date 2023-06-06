import tkinter
from tkinter import ttk
# import read_file as rd
#=================================================Read files path =============================================
from os.path import isdir, join , isfile
from os import listdir
import autocompletecombobox as autocomp
import multiselectoption as msop
import os

def function_TB():
    tb = ''
    mypath = "/runs/simrun_tav/e5ca/REV/TAV/"
    tb = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    return tb

def function1():
    data = []
    # var1 = open("/runs/simrun_tav/e5ca/REV/TAV/verilog.e5ca.IF_Apr21/E5CA/HBM3/Regressions/VE2VA/extended_moura_long.run","r").readlines()
    # for line in var1:
    #     data.append(line)
    var1 = "/runs/simrun_tav/e5ca/REV/TAV/verilog.e5ca.IF_Apr21/E5CA/HBM3/Regressions/VE2VA/"
    data = [f for f in listdir(var1) if isfile(join(var1, f))]
    return data

def function_netlist():
    onlyfiles = []
    mypath = "/runs/simrun_tav/e5ca/REV/TAV/verilog.e5ca.AOCV_Apr21/Netlist"
    onlyfiles = [f for f in listdir(mypath) if isdir(join(mypath, f))]
    return onlyfiles

#======================================CMD Exicutions and database =========================================
def register():
    global tb, reg, arg, dir_, depth, user_cmd, config_ ,VSIM_CMD, addition
    tb = tb_entry.get()
    reg = regression_combobox.get()
    arg = arg_combobox.get()
    depth = depth_combobox.get()
    dir_= dirpath_entry.get()
    config_ = config_combobox.get()
    addition = additional_combobox.get()
    
    if(arg != ""):
        dep = f'-o "+{arg}"'
    else:  dep = ''

    if(addition != ""):
        add = f'+{addition}'
    else:  add = ''

    op_set = (f"+define+DAL+FORCE_PPR_RATE+DISCONNECT_UBUMP+CHANS_DISABLED{add} +skip_serial_scan +ignore_precon_data +zero_init2 +speed_grades=2400 +chan_pincomp_delta=100 +rd_post_ui=3 +relax_tXP +set_tIS=100")
    VSIM_CMD = (f'vsim -s -r {reg} -x {config_} -l {dir_} -Y {depth} -o "{op_set}" {dep}')
    # print(VSIM_CMD)

    user_info_entry1.insert('1.0',f'{VSIM_CMD}')
    tb_entry.set("")
    regression_combobox.set("")
    arg_combobox.set("")
    depth_combobox.set("")
    dirpath_entry.delete(0,'end')
    config_combobox.set("")
    additional_combobox.set("")

def run_cmd():
    global st, reg, vsim_net, netlist_

    if(addition == "NO_CHIP"):
        netlist_ = ''
    else:
        if(addition == ""):
            netlist_ = ""
        else:  
            netlist_ = f'-S {netlist_combopicker.get()}'
    vsim_net = ("{}{}".format(VSIM_CMD, netlist_))

    print(vsim_net)

#==========================================design==================================================
window = tkinter.Tk()
window.title("Vsim CMD Support")
window.geometry("700x500")
window.resizable(0,0)
frame = tkinter.Frame(window)
# frame.pack()
frame.grid(row=0, column=0)
user_info_frame = ttk.LabelFrame(frame,text = "Please Enter All Details Correctly")
user_info_frame.grid(row=0, column=0,padx=20, pady=10)

select_tb = ttk.Label(user_info_frame, text="Please select your TB here :: ")
select_tb.grid(row=0, column=0, padx=30, pady=5)

tb_entry = autocomp.AutocompleteCombobox(user_info_frame, completevalues=function_TB())
tb_entry.grid(row=1, column=0)

regression_name = ttk.Label(user_info_frame, text="Regression :: ")
regression_name.grid(row=0, column=1)
# regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, values=function1())
regression_combobox = autocomp.AutocompleteCombobox(user_info_frame, completevalues=function1())
regression_combobox.grid(row=1, column=1, padx=20, pady=5)

args = tkinter.Label(user_info_frame, text="New +Args :: ")
args.grid(row=0, column=2)

arg_combobox = ttk.Combobox(user_info_frame, values=function1())
arg_combobox.grid(row=1, column=2, padx=20, pady=5)

dir_path = tkinter.Label(user_info_frame, text="Enter PATH Name Here :: ")
dir_path.grid(row=3, column=0, padx=20, pady=5)

dirpath_entry = tkinter.Entry(user_info_frame,textvariable="")
dirpath_entry.grid(row=4, column=0, padx=20, pady=5)

config_label = tkinter.Label(user_info_frame, text="Configuration :: ")
config_label.grid(row=3, column=1)

values_ = "x64_if","x64_core","x64_4h","x64_8h","x64_if_hd","x64_core_hd","x64_4h_hd","x64_4ha","x64_4ha_hd","x64_4he","x64_4he_hd","x64_8h_hd","x64_12h","x64_12h_hd","x64_16h","x64_16h_hd","x64_daprb"
config_combobox = ttk.Combobox(user_info_frame, values=values_)
config_combobox.grid(row=4, column=1, padx=20, pady=5)

depth = tkinter.Label(user_info_frame, text="Depth :: ")
depth.grid(row=3, column=2, padx=20, pady=5)

depth_combobox = ttk.Combobox(user_info_frame, values=("99999","19999","19995"))
depth_combobox.grid(row=4, column=2, padx=20, pady=5)

additional = tkinter.Label(user_info_frame, text="Additional Defines : ")
additional.grid(row=5, column=0, padx=20, pady=5)

additional_combobox = ttk.Combobox(user_info_frame, values=("NO_CHIP","RNX"))
additional_combobox.grid(row=5, column=1, padx=20, pady=5)

button = tkinter.Button(user_info_frame, text="All Done",command=register)
button.grid(row=5, column=2, pady=5)
#--------------------------------------------------------------------------------------

frame1 = tkinter.Frame(window)
# frame1.pack()
frame1.grid(row=1,column=0)

user = tkinter.LabelFrame(frame1,text = "CMD is ::")
user.grid(row=1, column=0,padx=0, pady=10)

user_info_entry1 = tkinter.Text(user,height=10)
user_info_entry1.grid(row=3,column=0,padx=5, pady=5,columnspan = 3)
# user_info_entry1.config(state='disabled')
user_info_entry1.xview_scroll(1, 'units')

netlist = tkinter.Label(user, text="Netlist :: ")
netlist.grid(row=4, column=0,padx=5, pady=5 )
# netlist_combobox = ttk.Combobox(user, values=function_netlist())
netlist_combopicker = msop.Combopicker(user, values = function_netlist())
netlist_combopicker.grid(row=4,column=1, pady=5 ,columnspan = 1)

button1 = tkinter.Button(user, text="RUN",command=run_cmd)
button1.grid(row=5, column=1, pady=10)


window.mainloop()

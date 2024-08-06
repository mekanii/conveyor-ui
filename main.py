from pathlib import Path
from PIL import Image
Image.CUBIC = Image.BICUBIC

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter as tk

PATH = Path(__file__).parent / 'assets'

class Main(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack(expand=True, fill=BOTH)

        self.images = [
            ttk.PhotoImage(
                name='package-36',
                file=PATH / 'icons/package-36.png'),
            ttk.PhotoImage(
                name='device-36',
                file=PATH / 'icons/device-36.png'),
            ttk.PhotoImage(
                name='cog-36',
                file=PATH / 'icons/cog-36.png')
        ]

        style = ttk.Style()

        style.configure('Secondary.TLabelframe', background=style.colors.secondary)
        style.configure('Secondary.TLabel', background=style.colors.secondary)
        style.configure('Padx.TEntry', padding=(10, 0))
        style.configure('Padding.TCombobox', padding=(10, 15))
        
        self.menu_selected = tk.StringVar(value='main')
        self.setpoint_speed1 = tk.IntVar(value=50)
        self.setpoint_speed2 = tk.IntVar(value=85)
        self.setpoint_part_qty = tk.IntVar(value=200)
        self.setpoint_bucket_qty = tk.IntVar(value=1900)

        self.status_run = tk.BooleanVar(value=True)
        self.status_run_text = tk.StringVar(value='STOP')
        self.status_run_bootstyle = 'square-toggle-danger'

        v_numeric_cmd = (self.register(self.validate_numeric_input), '%d', '%P', '%S')

        # menu buttons
        menu_frame = ttk.Frame(self, bootstyle=SECONDARY)
        menu_frame.grid(row=0, column=0, sticky=NS)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        menu_main_btn = ttk.Radiobutton(
            master=menu_frame,
            image='package-36',
            text='MAIN',
            value='main',
            variable=self.menu_selected,
            compound=TOP,
            bootstyle=TOOLBUTTON,
            command=lambda: self.change_menu('main')
        )
        menu_main_btn.pack(side=TOP, fill=BOTH, ipady=10)

        menu_parts_btn = ttk.Radiobutton(
            master=menu_frame,
            image='device-36',
            text='PARTS',
            value='parts',
            variable=self.menu_selected,
            compound=TOP,
            bootstyle=TOOLBUTTON,
            command=lambda: self.change_menu('parts')
        )
        menu_parts_btn.pack(side=TOP, fill=BOTH, ipady=10)

        menu_setting_btn = ttk.Radiobutton(
            master=menu_frame,
            image='cog-36',
            text='SETTINGS',
            value='settings',
            variable=self.menu_selected,
            compound=TOP,
            bootstyle=TOOLBUTTON,
            command=lambda: self.change_menu('settings')
        )
        menu_setting_btn.pack(side=TOP, fill=BOTH, ipady=10)

        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
        content_frame.grid_rowconfigure(0, weight=0)
        content_frame.grid_rowconfigure(1, weight=0)
        content_frame.grid_rowconfigure(2, weight=0)
        content_frame.grid_rowconfigure(3, weight=1)
        content_frame.grid_rowconfigure(4, weight=1)
        content_frame.grid_columnconfigure(0, weight=0)
        content_frame.grid_columnconfigure(1, weight=0)
        content_frame.grid_columnconfigure(2, weight=1)
        content_frame.grid_columnconfigure(3, weight=1)
        content_frame.grid_columnconfigure(4, weight=1)

        # Create the popup window but keep it hidden initially
        self.popup = None

        self.select_part_combobox = ttk.Menubutton(
            master=content_frame,
            text="SELECT PART",
            bootstyle=SECONDARY,
            state="readonly",
        )
        self.select_part_combobox.grid(row=0, column=0, columnspan=2, sticky=NSEW, ipady=10, padx=5, pady=5)
        self.select_part_combobox.bind('<Button-1>', self.toggle_popup)
        
        self.create_popup()

        qty_label = ttk.Label(
            master=content_frame,
            text='PART QTY',
            padding=(10,15),
            style='Secondary.TLabel',
            bootstyle=LIGHT
        )
        qty_label.grid(row=1, column=0, sticky=NSEW, padx=(5, 0), pady=5)

        part_qty_entry = ttk.Entry(
            master=content_frame,
            justify='right',
            validate='key',
            validatecommand=v_numeric_cmd,
            style='Padx.TEntry',
            bootstyle=SECONDARY,
            textvariable=self.setpoint_part_qty
        )
        part_qty_entry.grid(row=1, column=1, sticky=NSEW, padx=(0, 5), pady=5)

        bucket_label = ttk.Label(
            master=content_frame,
            text='BUCKET QTY',
            padding=(10,15),
            style='Secondary.TLabel',
            bootstyle=LIGHT
        )
        bucket_label.grid(row=2, column=0, sticky=NSEW, padx=(5, 0), pady=5)

        bucket_qty_entry = ttk.Entry(
            master=content_frame,
            justify='right',
            validate='key',
            validatecommand=v_numeric_cmd,
            style='Padx.TEntry',
            bootstyle=SECONDARY,
            textvariable=self.setpoint_bucket_qty
        )
        bucket_qty_entry.grid(row=2, column=1, sticky=NSEW, padx=(0, 5), pady=5)

        status_labelframe = ttk.Labelframe(content_frame, text='STATUS')
        status_labelframe.grid(row=0, column=2, columnspan=3, sticky=NSEW, padx=5, pady=5)

        start_button = ttk.Button(
            master=content_frame,
            text='START',
            bootstyle=SUCCESS
        )
        start_button.grid(row=1, column=2, rowspan=2, sticky=NSEW, padx=5, pady=5)

        pause_button = ttk.Button(
            master=content_frame,
            text='PAUSE',
            bootstyle=INFO
        )
        pause_button.grid(row=1, column=3, rowspan=2, sticky=NSEW, padx=5, pady=5)

        stop_button = ttk.Button(
            master=content_frame,
            text='STOP',
            bootstyle=DANGER
        )
        stop_button.grid(row=1, column=4, rowspan=2, sticky=NSEW, padx=5, pady=5)

        control_frame = ttk.Frame(content_frame)
        control_frame.grid(row=3, column=0, columnspan=5, sticky=NSEW, padx=5, pady=5)
        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_rowconfigure(1, weight=1)
        control_frame.grid_columnconfigure(0, weight=0)
        control_frame.grid_columnconfigure(1, weight=0)
        control_frame.grid_columnconfigure(2, weight=1)

        self.speed1_meter = ttk.Meter(
            master=control_frame,
            bootstyle=WARNING,
            interactive=True,
            amounttotal= 100,
            metersize= 280,
            meterthickness= 28,
            metertype=SEMI,
            textfont= '-size 42 -weight bold',
            subtext='SPEED 1',
            textright='%',
            subtextfont= '-size 16',
            subtextstyle= 'bold'
        )
        self.speed1_meter.grid(row=0, column=0, sticky=NSEW, padx=(5, 20), pady=10)

        self.speed2_meter = ttk.Meter(
            master=control_frame,
            bootstyle=WARNING,
            interactive=True,
            amounttotal= 100,
            metersize= 280,
            meterthickness= 28,
            metertype=SEMI,
            textfont= '-size 42 -weight bold',
            subtext='SPEED 2',
            textright='%',
            subtextfont= '-size 16',
            subtextstyle= 'bold'
        )
        self.speed2_meter.grid(row=0, column=1, sticky=NSEW, padx=(20, 5), pady=10)

        self.counter_part_meter = ttk.Meter(
            master=control_frame,
            bootstyle=INFO,
            amounttotal= self.setpoint_part_qty.get(),
            metersize= 280,
            meterthickness= 28,
            metertype=SEMI,
            textfont= '-size 42 -weight bold',
            subtext='PART',
            textright='pcs',
            subtextfont= '-size 16',
            subtextstyle= 'bold'
        )
        self.counter_part_meter.grid(row=1, column=0, sticky=NSEW, padx=(5, 20), pady=10)

        self.counter_bucket_meter = ttk.Meter(
            master=control_frame,
            bootstyle=DANGER,
            amounttotal= self.setpoint_bucket_qty.get(),
            metersize= 280,
            meterthickness= 28,
            metertype=SEMI,
            textfont= '-size 42 -weight bold',
            subtext='BUCKET',
            subtextfont= '-size 16',
            subtextstyle= 'bold'
        )
        self.counter_bucket_meter.grid(row=1, column=1, sticky=NSEW, padx=(20, 5), pady=10)

        self.speed1_meter.amountusedvar.trace('w', lambda *args:self.get_meter_amount_used(self.speed1_meter, self.setpoint_speed1))
        self.speed2_meter.amountusedvar.trace('w', lambda *args:self.get_meter_amount_used(self.speed2_meter, self.setpoint_speed2))
        part_qty_entry.bind('<FocusOut>', lambda *args:self.set_meter_amount_total(self.counter_part_meter, self.setpoint_part_qty))
        bucket_qty_entry.bind('<FocusOut>', lambda *args:self.set_meter_amount_total(self.counter_bucket_meter, self.setpoint_bucket_qty))

    def change_menu(self, value):
        self.menu_selected.set(value)

    def set_meter_amount_total(self, meter, variable, *args):
        try:
            if variable.get() < meter['amountused']:
                if meter['amountused'] > 0:
                    variable.set(meter['amountused'])
                else:
                    variable.set(1)

        except:
            if meter['amountused'] > 0:
                variable.set(meter['amountused'])
            else:
                variable.set(1)

        meter.configure(amounttotal=variable.get())

    def set_meter_amount_used(self, meter, variable, *args):
        meter.configure(amountused=variable.get())
    
    def get_meter_amount_used(self, meter, variable, *args):
        variable.set(meter['amountused'])

    def create_popup(self):
        if self.popup is not None:
            self.popup.destroy()

        self.popup = tk.Toplevel(self)
        self.popup.title('Part List')
        self.popup.withdraw()
        
        x = self.select_part_combobox.winfo_rootx()
        y = self.select_part_combobox.winfo_rooty() + self.select_part_combobox.winfo_height()
        self.popup.geometry(f"+{x}+{y}")
        self.popup.bind('<FocusOut>', self.hide_popup)
        
        self.popup_frame = ScrolledFrame(self.popup)
        self.popup_frame.pack(fill=tk.BOTH, expand=True, ipadx=5)

        self.create_popup_options()

    def create_popup_options(self):
        select_part_options = [
            'Part 01',
            'Part 02',
            'Part 03',
            'Part 04',
            'Part 05',
            'Part 06',
            'Part 07',
            'Part 08',
            'Part 09',
            'Part 10'
        ]

        for option in select_part_options:
            button = ttk.Button(
                self.popup_frame,
                text=option,
                bootstyle=SECONDARY,
                command=lambda opt=option: self.select_part(opt)
            )
            button.pack(fill=tk.X, ipady=8, pady=5)

    def toggle_popup(self, event=None):
        if self.popup is None or not self.popup.winfo_exists():
            self.create_popup()

        if self.popup.winfo_viewable():
            self.popup.withdraw()
        else:
            x = self.select_part_combobox.winfo_rootx()
            y = self.select_part_combobox.winfo_rooty() + self.select_part_combobox.winfo_height() + 10
            self.popup.geometry(f"+{x}+{y}")

            self.popup.deiconify()
            self.popup.lift()
            self.popup.focus_set()

    def hide_popup(self, event=None):
        self.popup.destroy()

    def select_part(self, option):
        self.select_part_combobox.config(text=option)
        self.popup.destroy()

    def validate_numeric_input(self, action, value_if_allowed, text):
        if action == '1':
            return text.isdigit() and int(value_if_allowed) > 0
        return True

if __name__ == "__main__":
    app = ttk.Window("Conveyor", "darkly")
    app.geometry("800x600") 
    Main(app)
    app.mainloop()
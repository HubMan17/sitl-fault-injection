import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pymavlink import mavutil


# ═══════════════════════════════════════════════════════════════
#  Localization
# ═══════════════════════════════════════════════════════════════
STRINGS = {
    "en": {
        "title": "SITL Fault Injection",
        "connection": "Connection",
        "address": "Address:",
        "connect": "Connect",
        "disconnect": "Disconnect",
        "connected": "Connected",
        "disconnected": "Disconnected",
        "connecting": "Connecting...",
        "failed": "Connection failed",
        "lang_btn": "RU",
        "not_connected": "Not connected",
        "not_connected_msg": "Connect to SITL first.",
        "conn_error": "Connection error",
        "error": "Error",
        "conn_hint": "SITL exposes several TCP ports: 5760, 5762, 5763.\n"
                     "If Mission Planner uses 5760, connect here via 5762 or 5763.",

        "tab_wind": "Wind",
        "tab_gps": "GPS Spoofing",
        "tab_pitot": "Pitot Failure",

        "wind_spd": "Wind speed (m/s)",
        "wind_dir": "Wind direction (deg)",
        "wind_turb": "Turbulence (m/s)",
        "wind_dir_z": "Vertical angle (deg)",
        "apply_wind": "Apply",
        "reset_wind": "Reset",

        "gps_lat": "Latitude offset (deg)",
        "gps_lon": "Longitude offset (deg)",
        "gps_alt": "Altitude offset (m)",
        "gps_jam": "GPS jamming",
        "gps_noise": "GPS noise (m)",
        "apply_gps": "Apply",
        "reset_gps": "Reset",

        "arspd_fail": "Stuck airspeed (m/s)",
        "arspd_failp": "Failure pressure (Pa)",
        "arspd_sign": "Reverse pitot / static",
        "apply_pitot": "Apply",
        "reset_pitot": "Reset",

        # tooltips
        "tip_wind_spd": "Simulated wind speed in m/s.\nSIM_WIND_SPD",
        "tip_wind_dir": "True direction the wind is coming FROM, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Random turbulence amplitude added to base wind.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Vertical wind angle: 0 = horizontal,\n+90 = pure updraft, -90 = pure downdraft.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Latitude glitch offset in degrees.\nPositive = shift north.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Longitude glitch offset in degrees.\nPositive = shift east.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Altitude glitch offset in meters.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Enable GPS signal jamming.\nSensor reports no fix.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Random altitude noise amplitude in meters\nadded to GPS readings.\nSIM_GPS1_NOISE",
        "tip_arspd_fail": "If > 0, airspeed sensor reports this\nfixed value regardless of real airspeed.\n0 = normal operation.\nSIM_ARSPD_FAIL",
        "tip_arspd_failp": "Fixed failure pressure in Pa applied\nto pitot tube. 0 = normal.\nSIM_ARSPD_FAILP",
        "tip_arspd_sign": "Simulate reversed pitot and static\nport connections.\nSIM_ARSPD_SIGN",
        "tip_address": "MAVLink address. SITL creates TCP ports\n5760, 5762, 5763. Use a free one.",
    },
    "ru": {
        "title": "SITL Fault Injection",
        "connection": "Подключение",
        "address": "Адрес:",
        "connect": "Подключить",
        "disconnect": "Отключить",
        "connected": "Подключено",
        "disconnected": "Отключено",
        "connecting": "Подключение...",
        "failed": "Ошибка подключения",
        "lang_btn": "EN",
        "not_connected": "Нет подключения",
        "not_connected_msg": "Сначала подключитесь к SITL.",
        "conn_error": "Ошибка подключения",
        "error": "Ошибка",
        "conn_hint": "SITL создаёт несколько TCP-портов: 5760, 5762, 5763.\n"
                     "Если Mission Planner использует 5760, подключайтесь через 5762 или 5763.",

        "tab_wind": "Ветер",
        "tab_gps": "GPS-спуфинг",
        "tab_pitot": "Отказ ПВД",

        "wind_spd": "Скорость ветра (м/с)",
        "wind_dir": "Направление ветра (град)",
        "wind_turb": "Турбулентность (м/с)",
        "wind_dir_z": "Вертикальный угол (град)",
        "apply_wind": "Применить",
        "reset_wind": "Сброс",

        "gps_lat": "Смещение широты (град)",
        "gps_lon": "Смещение долготы (град)",
        "gps_alt": "Смещение высоты (м)",
        "gps_jam": "Глушение GPS",
        "gps_noise": "Шум GPS (м)",
        "apply_gps": "Применить",
        "reset_gps": "Сброс",

        "arspd_fail": "Залипание скорости (м/с)",
        "arspd_failp": "Давление отказа (Па)",
        "arspd_sign": "Реверс питот / статика",
        "apply_pitot": "Применить",
        "reset_pitot": "Сброс",

        "tip_wind_spd": "Скорость симулируемого ветра в м/с.\nSIM_WIND_SPD",
        "tip_wind_dir": "Истинное направление ОТКУДА дует ветер, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Амплитуда случайной турбулентности\nповерх базового ветра.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Вертикальный угол ветра: 0 = горизонтально,\n+90 = восходящий, -90 = нисходящий.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Смещение широты в градусах.\nПоложительное = сдвиг на север.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Смещение долготы в градусах.\nПоложительное = сдвиг на восток.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Смещение высоты в метрах.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Включить глушение GPS-сигнала.\nДатчик сообщает об отсутствии фикса.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Амплитуда случайного шума высоты\nдобавляемого к показаниям GPS.\nSIM_GPS1_NOISE",
        "tip_arspd_fail": "Если > 0, датчик воздушной скорости\nвсегда показывает это значение.\n0 = нормальная работа.\nSIM_ARSPD_FAIL",
        "tip_arspd_failp": "Фиксированное давление отказа в Па\nна трубке Пито. 0 = норма.\nSIM_ARSPD_FAILP",
        "tip_arspd_sign": "Имитация перепутанного подключения\nпитот и статик портов.\nSIM_ARSPD_SIGN",
        "tip_address": "MAVLink-адрес. SITL создаёт TCP-порты\n5760, 5762, 5763. Используйте свободный.",
    },
}


# ═══════════════════════════════════════════════════════════════
#  Tooltip
# ═══════════════════════════════════════════════════════════════
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tw = None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _event=None):
        if self.tw:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tw = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, justify="left",
            background="#2b2b2b", foreground="#e0e0e0",
            relief="solid", borderwidth=1,
            font=("Segoe UI", 9), padx=8, pady=4,
        )
        label.pack()

    def _hide(self, _event=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None

    def update_text(self, text):
        self.text = text


# ═══════════════════════════════════════════════════════════════
#  MAVLink connection
# ═══════════════════════════════════════════════════════════════
class SITLConnection:
    def __init__(self):
        self.master = None
        self.connected = False

    def connect(self, address):
        try:
            self.master = mavutil.mavlink_connection(address)
            self.master.wait_heartbeat(timeout=5)
            self.connected = True
        except Exception as e:
            self.connected = False
            raise e

    def disconnect(self):
        if self.master:
            self.master.close()
        self.connected = False
        self.master = None

    def set_param(self, name, value):
        if not self.connected:
            raise RuntimeError("Not connected")
        self.master.param_set_send(name, value)
        time.sleep(0.05)


# ═══════════════════════════════════════════════════════════════
#  Main application
# ═══════════════════════════════════════════════════════════════
BG = "#1e1e2e"
BG2 = "#282840"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
GREEN = "#a6e3a1"
RED = "#f38ba8"
YELLOW = "#f9e2af"
SURFACE = "#313244"
ENTRY_BG = "#45475a"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.conn = SITLConnection()
        self.tooltips = []

        self.title("SITL Fault Injection")
        self.geometry("660x560")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._setup_styles()
        self._build_ui()
        self._apply_lang()

    # ── Styles ──────────────────────────────────────────────────
    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")

        s.configure(".", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TLabelframe", background=BG, foreground=ACCENT,
                     font=("Segoe UI", 10, "bold"))
        s.configure("TLabelframe.Label", background=BG, foreground=ACCENT)
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=SURFACE, foreground=FG,
                     padding=(14, 6), font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", ACCENT)],
              foreground=[("selected", "#1e1e2e")])

        s.configure("Accent.TButton", background=ACCENT, foreground="#1e1e2e",
                     font=("Segoe UI", 10, "bold"), padding=(16, 6))
        s.map("Accent.TButton",
              background=[("active", "#b4d0fb"), ("disabled", SURFACE)])

        s.configure("Reset.TButton", background=SURFACE, foreground=YELLOW,
                     font=("Segoe UI", 9), padding=(12, 4))
        s.map("Reset.TButton", background=[("active", ENTRY_BG)])

        s.configure("Lang.TButton", background=SURFACE, foreground=YELLOW,
                     font=("Segoe UI", 9, "bold"), padding=(8, 2))
        s.map("Lang.TButton", background=[("active", ENTRY_BG)])

        s.configure("Status.TLabel", background=BG, font=("Segoe UI", 10, "bold"))

        s.configure("TCheckbutton", background=BG, foreground=FG,
                     font=("Segoe UI", 10))
        s.map("TCheckbutton", background=[("active", BG)])

        s.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG,
                     insertcolor=FG)

    def _make_scale(self, parent, variable, from_, to, resolution):
        s = tk.Scale(
            parent, variable=variable, from_=from_, to=to,
            orient="horizontal", length=320, resolution=resolution,
            bg=BG, fg=FG, troughcolor=SURFACE, activebackground=ACCENT,
            highlightthickness=0, sliderrelief="flat", bd=0,
            font=("Segoe UI", 9),
        )
        return s

    # ── Build UI ────────────────────────────────────────────────
    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=(10, 0))

        self.conn_frame = ttk.LabelFrame(top, text="Connection")
        self.conn_frame.pack(side="left", fill="x", expand=True)

        inner = ttk.Frame(self.conn_frame)
        inner.pack(padx=8, pady=6)

        self.addr_label = ttk.Label(inner, text="Address:")
        self.addr_label.pack(side="left", padx=(0, 6))

        self.addr_var = tk.StringVar(value="tcp:127.0.0.1:5762")
        e = ttk.Entry(inner, textvariable=self.addr_var, width=26)
        e.pack(side="left", padx=(0, 8))
        self._tip(e, "tip_address")

        self.conn_btn = ttk.Button(inner, text="Connect", style="Accent.TButton",
                                   command=self._toggle_connection)
        self.conn_btn.pack(side="left", padx=(0, 10))

        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(inner, textvariable=self.status_var,
                                      style="Status.TLabel", foreground=RED)
        self.status_label.pack(side="left", padx=4)

        self.lang_btn = ttk.Button(top, text="RU", style="Lang.TButton",
                                   command=self._toggle_lang, width=4)
        self.lang_btn.pack(side="right", padx=(10, 0), pady=6)

        # Notebook
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=True, padx=10, pady=10)

        self.wind_tab = self._build_wind_tab(self.nb)
        self.gps_tab = self._build_gps_tab(self.nb)
        self.pitot_tab = self._build_pitot_tab(self.nb)

        self.nb.add(self.wind_tab, text="Wind")
        self.nb.add(self.gps_tab, text="GPS Spoofing")
        self.nb.add(self.pitot_tab, text="Pitot Failure")

    # ── Wind tab ────────────────────────────────────────────────
    def _build_wind_tab(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 6}

        self.wind_spd = tk.DoubleVar(value=0)
        self.wind_dir = tk.DoubleVar(value=180)
        self.wind_turb = tk.DoubleVar(value=0)
        self.wind_dir_z = tk.DoubleVar(value=0)

        r = 0
        self.lbl_wind_spd = ttk.Label(fr, text="Wind speed (m/s)")
        self.lbl_wind_spd.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_spd, 0, 50, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_spd, "tip_wind_spd")
        self._tip(sc, "tip_wind_spd")

        r += 1
        self.lbl_wind_dir = ttk.Label(fr, text="Wind direction (deg)")
        self.lbl_wind_dir.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_dir, 0, 360, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_dir, "tip_wind_dir")
        self._tip(sc, "tip_wind_dir")

        r += 1
        self.lbl_wind_turb = ttk.Label(fr, text="Turbulence (m/s)")
        self.lbl_wind_turb.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_turb, 0, 20, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_turb, "tip_wind_turb")
        self._tip(sc, "tip_wind_turb")

        r += 1
        self.lbl_wind_dir_z = ttk.Label(fr, text="Vertical angle (deg)")
        self.lbl_wind_dir_z.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_dir_z, -90, 90, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_dir_z, "tip_wind_dir_z")
        self._tip(sc, "tip_wind_dir_z")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=14)
        self.btn_apply_wind = ttk.Button(btn_fr, text="Apply", style="Accent.TButton",
                                         command=self._apply_wind)
        self.btn_apply_wind.pack(side="left", padx=8)
        self.btn_reset_wind = ttk.Button(btn_fr, text="Reset", style="Reset.TButton",
                                         command=self._reset_wind)
        self.btn_reset_wind.pack(side="left", padx=8)

        return fr

    def _apply_wind(self):
        self._run_safe(lambda: [
            self.conn.set_param("SIM_WIND_SPD", self.wind_spd.get()),
            self.conn.set_param("SIM_WIND_DIR", self.wind_dir.get()),
            self.conn.set_param("SIM_WIND_TURB", self.wind_turb.get()),
            self.conn.set_param("SIM_WIND_DIR_Z", self.wind_dir_z.get()),
        ])

    def _reset_wind(self):
        self.wind_spd.set(0)
        self.wind_dir.set(180)
        self.wind_turb.set(0)
        self.wind_dir_z.set(0)
        self._apply_wind()

    # ── GPS tab ─────────────────────────────────────────────────
    def _build_gps_tab(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 6}

        self.gps_lat = tk.DoubleVar(value=0)
        self.gps_lon = tk.DoubleVar(value=0)
        self.gps_alt = tk.DoubleVar(value=0)
        self.gps_jam_var = tk.IntVar(value=0)
        self.gps_noise = tk.DoubleVar(value=0)

        r = 0
        self.lbl_gps_lat = ttk.Label(fr, text="Latitude offset (deg)")
        self.lbl_gps_lat.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_lat, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_lat, "tip_gps_lat")
        self._tip(e, "tip_gps_lat")

        r += 1
        self.lbl_gps_lon = ttk.Label(fr, text="Longitude offset (deg)")
        self.lbl_gps_lon.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_lon, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_lon, "tip_gps_lon")
        self._tip(e, "tip_gps_lon")

        r += 1
        self.lbl_gps_alt = ttk.Label(fr, text="Altitude offset (m)")
        self.lbl_gps_alt.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_alt, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_alt, "tip_gps_alt")
        self._tip(e, "tip_gps_alt")

        r += 1
        self.chk_gps_jam = ttk.Checkbutton(fr, text="GPS jamming",
                                            variable=self.gps_jam_var)
        self.chk_gps_jam.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        self._tip(self.chk_gps_jam, "tip_gps_jam")

        r += 1
        self.lbl_gps_noise = ttk.Label(fr, text="GPS noise (m)")
        self.lbl_gps_noise.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.gps_noise, 0, 100, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_gps_noise, "tip_gps_noise")
        self._tip(sc, "tip_gps_noise")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=14)
        self.btn_apply_gps = ttk.Button(btn_fr, text="Apply", style="Accent.TButton",
                                        command=self._apply_gps)
        self.btn_apply_gps.pack(side="left", padx=8)
        self.btn_reset_gps = ttk.Button(btn_fr, text="Reset", style="Reset.TButton",
                                        command=self._reset_gps)
        self.btn_reset_gps.pack(side="left", padx=8)

        return fr

    def _apply_gps(self):
        self._run_safe(lambda: [
            self.conn.set_param("SIM_GPS1_GLTCH_X", self.gps_lat.get()),
            self.conn.set_param("SIM_GPS1_GLTCH_Y", self.gps_lon.get()),
            self.conn.set_param("SIM_GPS1_GLTCH_Z", self.gps_alt.get()),
            self.conn.set_param("SIM_GPS1_JAM", self.gps_jam_var.get()),
            self.conn.set_param("SIM_GPS1_NOISE", self.gps_noise.get()),
        ])

    def _reset_gps(self):
        self.gps_lat.set(0)
        self.gps_lon.set(0)
        self.gps_alt.set(0)
        self.gps_jam_var.set(0)
        self.gps_noise.set(0)
        self._apply_gps()

    # ── Pitot tab ───────────────────────────────────────────────
    def _build_pitot_tab(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 6}

        self.arspd_fail = tk.DoubleVar(value=0)
        self.arspd_failp = tk.DoubleVar(value=0)
        self.arspd_sign_var = tk.IntVar(value=0)

        r = 0
        self.lbl_arspd_fail = ttk.Label(fr, text="Stuck airspeed (m/s)")
        self.lbl_arspd_fail.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.arspd_fail, 0, 80, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_fail, "tip_arspd_fail")
        self._tip(sc, "tip_arspd_fail")

        r += 1
        self.lbl_arspd_failp = ttk.Label(fr, text="Failure pressure (Pa)")
        self.lbl_arspd_failp.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.arspd_failp, 0, 500, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_failp, "tip_arspd_failp")
        self._tip(sc, "tip_arspd_failp")

        r += 1
        self.chk_arspd_sign = ttk.Checkbutton(fr, text="Reverse pitot / static",
                                               variable=self.arspd_sign_var)
        self.chk_arspd_sign.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        self._tip(self.chk_arspd_sign, "tip_arspd_sign")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=14)
        self.btn_apply_pitot = ttk.Button(btn_fr, text="Apply", style="Accent.TButton",
                                          command=self._apply_pitot)
        self.btn_apply_pitot.pack(side="left", padx=8)
        self.btn_reset_pitot = ttk.Button(btn_fr, text="Reset", style="Reset.TButton",
                                          command=self._reset_pitot)
        self.btn_reset_pitot.pack(side="left", padx=8)

        return fr

    def _apply_pitot(self):
        self._run_safe(lambda: [
            self.conn.set_param("SIM_ARSPD_FAIL", self.arspd_fail.get()),
            self.conn.set_param("SIM_ARSPD_FAILP", self.arspd_failp.get()),
            self.conn.set_param("SIM_ARSPD_SIGN", self.arspd_sign_var.get()),
        ])

    def _reset_pitot(self):
        self.arspd_fail.set(0)
        self.arspd_failp.set(0)
        self.arspd_sign_var.set(0)
        self._apply_pitot()

    # ── Connection ──────────────────────────────────────────────
    def _toggle_connection(self):
        if self.conn.connected:
            self.conn.disconnect()
            self.status_var.set(self._s("disconnected"))
            self.status_label.configure(foreground=RED)
            self.conn_btn.configure(text=self._s("connect"))
        else:
            addr = self.addr_var.get().strip()
            self.status_var.set(self._s("connecting"))
            self.status_label.configure(foreground=YELLOW)
            self.update_idletasks()
            threading.Thread(target=self._do_connect, args=(addr,), daemon=True).start()

    def _do_connect(self, addr):
        try:
            self.conn.connect(addr)
            self.after(0, lambda: self.status_var.set(self._s("connected")))
            self.after(0, lambda: self.status_label.configure(foreground=GREEN))
            self.after(0, lambda: self.conn_btn.configure(text=self._s("disconnect")))
        except Exception as e:
            self.after(0, lambda: self.status_var.set(self._s("failed")))
            self.after(0, lambda: self.status_label.configure(foreground=RED))
            self.after(0, lambda: messagebox.showerror(self._s("conn_error"), str(e)))

    # ── Language ────────────────────────────────────────────────
    def _s(self, key):
        return STRINGS[self.lang].get(key, key)

    def _toggle_lang(self):
        self.lang = "ru" if self.lang == "en" else "en"
        self._apply_lang()

    def _apply_lang(self):
        s = STRINGS[self.lang]

        self.title(s["title"])
        self.conn_frame.configure(text=s["connection"])
        self.addr_label.configure(text=s["address"])
        self.lang_btn.configure(text=s["lang_btn"])

        if self.conn.connected:
            self.status_var.set(s["connected"])
            self.conn_btn.configure(text=s["disconnect"])
        else:
            self.status_var.set(s["disconnected"])
            self.conn_btn.configure(text=s["connect"])

        self.nb.tab(0, text=s["tab_wind"])
        self.nb.tab(1, text=s["tab_gps"])
        self.nb.tab(2, text=s["tab_pitot"])

        self.lbl_wind_spd.configure(text=s["wind_spd"])
        self.lbl_wind_dir.configure(text=s["wind_dir"])
        self.lbl_wind_turb.configure(text=s["wind_turb"])
        self.lbl_wind_dir_z.configure(text=s["wind_dir_z"])
        self.btn_apply_wind.configure(text=s["apply_wind"])
        self.btn_reset_wind.configure(text=s["reset_wind"])

        self.lbl_gps_lat.configure(text=s["gps_lat"])
        self.lbl_gps_lon.configure(text=s["gps_lon"])
        self.lbl_gps_alt.configure(text=s["gps_alt"])
        self.chk_gps_jam.configure(text=s["gps_jam"])
        self.lbl_gps_noise.configure(text=s["gps_noise"])
        self.btn_apply_gps.configure(text=s["apply_gps"])
        self.btn_reset_gps.configure(text=s["reset_gps"])

        self.lbl_arspd_fail.configure(text=s["arspd_fail"])
        self.lbl_arspd_failp.configure(text=s["arspd_failp"])
        self.chk_arspd_sign.configure(text=s["arspd_sign"])
        self.btn_apply_pitot.configure(text=s["apply_pitot"])
        self.btn_reset_pitot.configure(text=s["reset_pitot"])

        for tip, key in self.tooltips:
            tip.update_text(s.get(key, key))

    # ── Tooltip helper ──────────────────────────────────────────
    def _tip(self, widget, key):
        t = Tooltip(widget, self._s(key))
        self.tooltips.append((t, key))

    # ── Safe param send ─────────────────────────────────────────
    def _run_safe(self, fn):
        if not self.conn.connected:
            messagebox.showwarning(self._s("not_connected"),
                                   self._s("not_connected_msg"))
            return
        try:
            fn()
        except Exception as e:
            messagebox.showerror(self._s("error"), str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

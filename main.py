import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
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
        "param_sent": "Parameters sent",

        "tab_wind": "Wind",
        "tab_gps": "GPS Spoofing",
        "tab_pitot": "Pitot Failure",

        # wind
        "wind_spd": "Wind speed (m/s)",
        "wind_dir": "Wind direction (deg)",
        "wind_turb": "Turbulence (m/s)",
        "wind_dir_z": "Vertical angle (deg)",
        "apply_wind": "Apply",
        "reset_wind": "Reset",

        # gps manual
        "gps_manual": "Manual",
        "gps_auto": "Auto Spoofing",
        "gps_lat": "Latitude offset (deg)",
        "gps_lon": "Longitude offset (deg)",
        "gps_alt": "Altitude offset (m)",
        "gps_jam": "GPS jamming",
        "gps_noise": "GPS noise (m)",
        "apply_gps": "Apply",
        "reset_gps": "Reset",

        # gps auto
        "gps_preset": "Spoofing intensity:",
        "gps_preset_off": "Off",
        "gps_preset_weak": "Weak (~5 m drift)",
        "gps_preset_medium": "Medium (~50 m drift)",
        "gps_preset_strong": "Strong (~200 m drift)",
        "gps_preset_extreme": "Extreme (~1 km drift)",
        "gps_drift": "Drift simulation",
        "gps_drift_on": "Enable gradual drift",
        "gps_drift_speed": "Drift rate",
        "gps_drift_slow": "Slow",
        "gps_drift_fast": "Fast",
        "gps_start_auto": "Start",
        "gps_stop_auto": "Stop",
        "gps_auto_active": "Active",
        "gps_auto_stopped": "Stopped",

        # pitot
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
        "tip_gps_lat": "Latitude glitch in degrees.\n0.00001 ~ 1.1 m, 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Longitude glitch in degrees.\n0.00001 ~ 1.1 m, 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Altitude glitch in meters.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Enable GPS signal jamming.\nSensor reports no fix.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Random altitude noise in meters\nadded to GPS readings.\nSIM_GPS1_NOISE",
        "tip_arspd_fail": "If > 0, airspeed sensor reports this\nfixed value regardless of real airspeed.\n0 = normal operation.\nSIM_ARSPD_FAIL",
        "tip_arspd_failp": "Fixed failure pressure in Pa applied\nto pitot tube. 0 = normal.\nSIM_ARSPD_FAILP",
        "tip_arspd_sign": "Simulate reversed pitot and static\nport connections.\nSIM_ARSPD_SIGN",
        "tip_address": "MAVLink address. SITL creates TCP ports\n5760, 5762, 5763. Use a free one\nso Mission Planner can use another.",
        "tip_gps_preset": "Quick preset: sets offset, noise, and\njam values to simulate spoofing\nof varying intensity.",
        "tip_gps_drift": "Gradually increases GPS offset over time,\nsimulating a slow spoofing attack.\nThe vehicle drifts without sudden jumps.",
        "tip_gps_drift_speed": "How fast the GPS position drifts.\nSlow: realistic attack.\nFast: aggressive spoofing.",
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
        "param_sent": "Параметры отправлены",

        "tab_wind": "Ветер",
        "tab_gps": "GPS-спуфинг",
        "tab_pitot": "Отказ ПВД",

        "wind_spd": "Скорость ветра (м/с)",
        "wind_dir": "Направление ветра (град)",
        "wind_turb": "Турбулентность (м/с)",
        "wind_dir_z": "Вертикальный угол (град)",
        "apply_wind": "Применить",
        "reset_wind": "Сброс",

        "gps_manual": "Ручное",
        "gps_auto": "Авто-спуфинг",
        "gps_lat": "Смещение широты (град)",
        "gps_lon": "Смещение долготы (град)",
        "gps_alt": "Смещение высоты (м)",
        "gps_jam": "Глушение GPS",
        "gps_noise": "Шум GPS (м)",
        "apply_gps": "Применить",
        "reset_gps": "Сброс",

        "gps_preset": "Интенсивность спуфинга:",
        "gps_preset_off": "Выкл",
        "gps_preset_weak": "Слабый (~5 м сдвиг)",
        "gps_preset_medium": "Средний (~50 м сдвиг)",
        "gps_preset_strong": "Сильный (~200 м сдвиг)",
        "gps_preset_extreme": "Экстремальный (~1 км сдвиг)",
        "gps_drift": "Симуляция дрифта",
        "gps_drift_on": "Включить плавный дрифт",
        "gps_drift_speed": "Скорость дрифта",
        "gps_drift_slow": "Медленно",
        "gps_drift_fast": "Быстро",
        "gps_start_auto": "Старт",
        "gps_stop_auto": "Стоп",
        "gps_auto_active": "Активно",
        "gps_auto_stopped": "Остановлено",

        "arspd_fail": "Залипание скорости (м/с)",
        "arspd_failp": "Давление отказа (Па)",
        "arspd_sign": "Реверс питот / статика",
        "apply_pitot": "Применить",
        "reset_pitot": "Сброс",

        "tip_wind_spd": "Скорость симулируемого ветра в м/с.\nSIM_WIND_SPD",
        "tip_wind_dir": "Истинное направление ОТКУДА дует ветер, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Амплитуда случайной турбулентности\nповерх базового ветра.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Вертикальный угол ветра: 0 = горизонтально,\n+90 = восходящий, -90 = нисходящий.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Смещение широты в градусах.\n0.00001 ~ 1.1 м, 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Смещение долготы в градусах.\n0.00001 ~ 1.1 м, 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Смещение высоты в метрах.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Включить глушение GPS-сигнала.\nДатчик сообщает об отсутствии фикса.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Амплитуда случайного шума высоты\nдобавляемого к показаниям GPS.\nSIM_GPS1_NOISE",
        "tip_arspd_fail": "Если > 0, датчик воздушной скорости\nвсегда показывает это значение.\n0 = нормальная работа.\nSIM_ARSPD_FAIL",
        "tip_arspd_failp": "Фиксированное давление отказа в Па\nна трубке Пито. 0 = норма.\nSIM_ARSPD_FAILP",
        "tip_arspd_sign": "Имитация перепутанного подключения\nпитот и статик портов.\nSIM_ARSPD_SIGN",
        "tip_address": "MAVLink-адрес. SITL создаёт TCP-порты\n5760, 5762, 5763. Используйте свободный,\nчтобы Mission Planner занял другой.",
        "tip_gps_preset": "Быстрый пресет: задаёт смещение, шум\nи глушение для имитации спуфинга\nразной интенсивности.",
        "tip_gps_drift": "Плавно увеличивает GPS-смещение со временем,\nимитируя медленную спуфинг-атаку.\nАппарат дрейфует без резких скачков.",
        "tip_gps_drift_speed": "Как быстро дрейфует GPS-позиция.\nМедленно: реалистичная атака.\nБыстро: агрессивный спуфинг.",
    },
}

# GPS spoofing presets: (lat_offset_deg, lon_offset_deg, alt_m, noise_m, jam)
GPS_PRESETS = {
    "off":     (0.0,      0.0,      0.0,  0, 0),
    "weak":    (0.00002,  0.00003,  2.0,  3, 0),
    "medium":  (0.0002,   0.0003,   10.0, 8, 0),
    "strong":  (0.001,    0.0012,   25.0, 15, 0),
    "extreme": (0.005,    0.006,    50.0, 30, 0),
}

# Drift step sizes per tick (~0.5s): (lat_deg, lon_deg, alt_m) per step
DRIFT_RATES = {
    "slow": (0.0000005, 0.0000006, 0.05),
    "fast": (0.000005,  0.000006,  0.5),
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
        tk.Label(
            tw, text=self.text, justify="left",
            background="#2b2b2b", foreground="#e0e0e0",
            relief="solid", borderwidth=1,
            font=("Segoe UI", 9), padx=8, pady=4,
        ).pack()

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
        self._lock = threading.Lock()

    def connect(self, address):
        self.master = mavutil.mavlink_connection(address)
        self.master.wait_heartbeat(timeout=5)
        self.connected = True

    def disconnect(self):
        if self.master:
            self.master.close()
        self.connected = False
        self.master = None

    def set_param(self, name, value):
        if not self.connected:
            raise RuntimeError("Not connected")
        with self._lock:
            self.master.param_set_send(name, value)
            time.sleep(0.05)


# ═══════════════════════════════════════════════════════════════
#  Theme
# ═══════════════════════════════════════════════════════════════
BG      = "#1e1e2e"
FG      = "#cdd6f4"
ACCENT  = "#89b4fa"
GREEN   = "#a6e3a1"
RED     = "#f38ba8"
YELLOW  = "#f9e2af"
SURFACE = "#313244"
ENTRY_BG = "#45475a"
ORANGE  = "#fab387"


# ═══════════════════════════════════════════════════════════════
#  Application
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.conn = SITLConnection()
        self.tooltips = []

        # drift state
        self._drift_active = False
        self._drift_lat = 0.0
        self._drift_lon = 0.0
        self._drift_alt = 0.0

        self.title("SITL Fault Injection")
        self.geometry("680x600")
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
              background=[("selected", ACCENT)], foreground=[("selected", "#1e1e2e")])
        s.configure("Accent.TButton", background=ACCENT, foreground="#1e1e2e",
                     font=("Segoe UI", 10, "bold"), padding=(16, 6))
        s.map("Accent.TButton",
              background=[("active", "#b4d0fb"), ("disabled", SURFACE)])
        s.configure("Reset.TButton", background=SURFACE, foreground=YELLOW,
                     font=("Segoe UI", 9), padding=(12, 4))
        s.map("Reset.TButton", background=[("active", ENTRY_BG)])
        s.configure("Stop.TButton", background=RED, foreground="#1e1e2e",
                     font=("Segoe UI", 10, "bold"), padding=(16, 6))
        s.map("Stop.TButton", background=[("active", "#f5a0b8")])
        s.configure("Lang.TButton", background=SURFACE, foreground=YELLOW,
                     font=("Segoe UI", 9, "bold"), padding=(8, 2))
        s.map("Lang.TButton", background=[("active", ENTRY_BG)])
        s.configure("Status.TLabel", background=BG, font=("Segoe UI", 10, "bold"))
        s.configure("Info.TLabel", background=BG, foreground=ORANGE,
                     font=("Segoe UI", 9, "italic"))
        s.configure("TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TCheckbutton", background=[("active", BG)])
        s.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG, insertcolor=FG)
        s.configure("TRadiobutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TRadiobutton", background=[("active", BG)])

    def _make_scale(self, parent, variable, from_, to, resolution):
        return tk.Scale(
            parent, variable=variable, from_=from_, to=to,
            orient="horizontal", length=320, resolution=resolution,
            bg=BG, fg=FG, troughcolor=SURFACE, activebackground=ACCENT,
            highlightthickness=0, sliderrelief="flat", bd=0, font=("Segoe UI", 9),
        )

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
        self.lbl_wind_spd = ttk.Label(fr)
        self.lbl_wind_spd.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_spd, 0, 50, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_spd, "tip_wind_spd"); self._tip(sc, "tip_wind_spd")

        r += 1
        self.lbl_wind_dir = ttk.Label(fr)
        self.lbl_wind_dir.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_dir, 0, 360, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_dir, "tip_wind_dir"); self._tip(sc, "tip_wind_dir")

        r += 1
        self.lbl_wind_turb = ttk.Label(fr)
        self.lbl_wind_turb.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_turb, 0, 20, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_turb, "tip_wind_turb"); self._tip(sc, "tip_wind_turb")

        r += 1
        self.lbl_wind_dir_z = ttk.Label(fr)
        self.lbl_wind_dir_z.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.wind_dir_z, -90, 90, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_wind_dir_z, "tip_wind_dir_z"); self._tip(sc, "tip_wind_dir_z")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=14)
        self.btn_apply_wind = ttk.Button(btn_fr, style="Accent.TButton",
                                         command=self._apply_wind)
        self.btn_apply_wind.pack(side="left", padx=8)
        self.btn_reset_wind = ttk.Button(btn_fr, style="Reset.TButton",
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
        self.wind_spd.set(0); self.wind_dir.set(180)
        self.wind_turb.set(0); self.wind_dir_z.set(0)
        self._apply_wind()

    # ── GPS tab ─────────────────────────────────────────────────
    def _build_gps_tab(self, parent):
        fr = ttk.Frame(parent)

        # sub-notebook: Manual / Auto
        self.gps_nb = ttk.Notebook(fr)
        self.gps_nb.pack(fill="both", expand=True, padx=4, pady=4)

        manual_fr = self._build_gps_manual(self.gps_nb)
        auto_fr = self._build_gps_auto(self.gps_nb)

        self.gps_nb.add(manual_fr, text="Manual")
        self.gps_nb.add(auto_fr, text="Auto Spoofing")
        return fr

    def _build_gps_manual(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 5}

        self.gps_lat = tk.DoubleVar(value=0)
        self.gps_lon = tk.DoubleVar(value=0)
        self.gps_alt = tk.DoubleVar(value=0)
        self.gps_jam_var = tk.IntVar(value=0)
        self.gps_noise = tk.DoubleVar(value=0)

        r = 0
        self.lbl_gps_lat = ttk.Label(fr)
        self.lbl_gps_lat.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_lat, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_lat, "tip_gps_lat"); self._tip(e, "tip_gps_lat")

        r += 1
        self.lbl_gps_lon = ttk.Label(fr)
        self.lbl_gps_lon.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_lon, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_lon, "tip_gps_lon"); self._tip(e, "tip_gps_lon")

        r += 1
        self.lbl_gps_alt = ttk.Label(fr)
        self.lbl_gps_alt.grid(row=r, column=0, sticky="w", **pad)
        e = ttk.Entry(fr, textvariable=self.gps_alt, width=14)
        e.grid(row=r, column=1, sticky="w", **pad)
        self._tip(self.lbl_gps_alt, "tip_gps_alt"); self._tip(e, "tip_gps_alt")

        r += 1
        self.chk_gps_jam = ttk.Checkbutton(fr, variable=self.gps_jam_var)
        self.chk_gps_jam.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        self._tip(self.chk_gps_jam, "tip_gps_jam")

        r += 1
        self.lbl_gps_noise = ttk.Label(fr)
        self.lbl_gps_noise.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.gps_noise, 0, 50, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_gps_noise, "tip_gps_noise"); self._tip(sc, "tip_gps_noise")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=10)
        self.btn_apply_gps = ttk.Button(btn_fr, style="Accent.TButton",
                                        command=self._apply_gps)
        self.btn_apply_gps.pack(side="left", padx=8)
        self.btn_reset_gps = ttk.Button(btn_fr, style="Reset.TButton",
                                        command=self._reset_gps)
        self.btn_reset_gps.pack(side="left", padx=8)
        return fr

    def _build_gps_auto(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 5}

        # ── Preset selector ──
        r = 0
        self.lbl_gps_preset = ttk.Label(fr)
        self.lbl_gps_preset.grid(row=r, column=0, sticky="w", **pad)
        self._tip(self.lbl_gps_preset, "tip_gps_preset")

        self.gps_preset_var = tk.StringVar(value="off")
        preset_fr = ttk.Frame(fr)
        preset_fr.grid(row=r, column=1, sticky="w", **pad)

        self.preset_radios = []
        for val in ("off", "weak", "medium", "strong", "extreme"):
            rb = ttk.Radiobutton(preset_fr, variable=self.gps_preset_var, value=val)
            rb.pack(anchor="w")
            self.preset_radios.append((rb, val))
            self._tip(rb, "tip_gps_preset")

        r += 1
        self.btn_apply_preset = ttk.Button(fr, style="Accent.TButton",
                                           command=self._apply_preset)
        self.btn_apply_preset.grid(row=r, column=0, columnspan=2, pady=8)

        # ── Separator ──
        r += 1
        ttk.Separator(fr, orient="horizontal").grid(
            row=r, column=0, columnspan=2, sticky="ew", padx=14, pady=6)

        # ── Drift simulation ──
        r += 1
        self.lbl_gps_drift = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_gps_drift.grid(row=r, column=0, sticky="w", **pad)
        self._tip(self.lbl_gps_drift, "tip_gps_drift")

        r += 1
        self.drift_enabled = tk.IntVar(value=0)
        self.chk_drift = ttk.Checkbutton(fr, variable=self.drift_enabled)
        self.chk_drift.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        self._tip(self.chk_drift, "tip_gps_drift")

        r += 1
        self.lbl_drift_speed = ttk.Label(fr)
        self.lbl_drift_speed.grid(row=r, column=0, sticky="w", **pad)
        self._tip(self.lbl_drift_speed, "tip_gps_drift_speed")

        drift_speed_fr = ttk.Frame(fr)
        drift_speed_fr.grid(row=r, column=1, sticky="w", **pad)
        self.drift_speed_var = tk.StringVar(value="slow")
        self.rb_drift_slow = ttk.Radiobutton(drift_speed_fr, variable=self.drift_speed_var,
                                             value="slow")
        self.rb_drift_slow.pack(side="left", padx=(0, 12))
        self.rb_drift_fast = ttk.Radiobutton(drift_speed_fr, variable=self.drift_speed_var,
                                             value="fast")
        self.rb_drift_fast.pack(side="left")

        r += 1
        drift_btn_fr = ttk.Frame(fr)
        drift_btn_fr.grid(row=r, column=0, columnspan=2, pady=8)
        self.btn_start_drift = ttk.Button(drift_btn_fr, style="Accent.TButton",
                                          command=self._start_drift)
        self.btn_start_drift.pack(side="left", padx=8)
        self.btn_stop_drift = ttk.Button(drift_btn_fr, style="Stop.TButton",
                                         command=self._stop_drift)
        self.btn_stop_drift.pack(side="left", padx=8)

        r += 1
        self.drift_status_var = tk.StringVar(value="Stopped")
        self.drift_status_label = ttk.Label(fr, textvariable=self.drift_status_var,
                                            style="Info.TLabel")
        self.drift_status_label.grid(row=r, column=0, columnspan=2, **pad)

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
        self.gps_lat.set(0); self.gps_lon.set(0); self.gps_alt.set(0)
        self.gps_jam_var.set(0); self.gps_noise.set(0)
        self._apply_gps()

    def _apply_preset(self):
        key = self.gps_preset_var.get()
        lat, lon, alt, noise, jam = GPS_PRESETS[key]
        self._run_safe(lambda: [
            self.conn.set_param("SIM_GPS1_GLTCH_X", lat),
            self.conn.set_param("SIM_GPS1_GLTCH_Y", lon),
            self.conn.set_param("SIM_GPS1_GLTCH_Z", alt),
            self.conn.set_param("SIM_GPS1_NOISE", noise),
            self.conn.set_param("SIM_GPS1_JAM", jam),
        ])

    # ── Drift logic ─────────────────────────────────────────────
    def _start_drift(self):
        if self._drift_active:
            return
        if not self.conn.connected:
            messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg"))
            return
        self._drift_active = True
        self._drift_lat = 0.0
        self._drift_lon = 0.0
        self._drift_alt = 0.0
        self.drift_status_var.set(self._s("gps_auto_active"))
        self.drift_status_label.configure(foreground=GREEN)
        threading.Thread(target=self._drift_loop, daemon=True).start()

    def _stop_drift(self):
        self._drift_active = False
        self.drift_status_var.set(self._s("gps_auto_stopped"))
        self.drift_status_label.configure(foreground=RED)
        # reset glitch to zero
        if self.conn.connected:
            try:
                self.conn.set_param("SIM_GPS1_GLTCH_X", 0)
                self.conn.set_param("SIM_GPS1_GLTCH_Y", 0)
                self.conn.set_param("SIM_GPS1_GLTCH_Z", 0)
                self.conn.set_param("SIM_GPS1_NOISE", 0)
            except Exception:
                pass

    def _drift_loop(self):
        while self._drift_active and self.conn.connected:
            rate_key = self.drift_speed_var.get()
            dlat, dlon, dalt = DRIFT_RATES.get(rate_key, DRIFT_RATES["slow"])

            # add small randomness for realism
            self._drift_lat += dlat * (1 + random.uniform(-0.3, 0.3))
            self._drift_lon += dlon * (1 + random.uniform(-0.3, 0.3))
            self._drift_alt += dalt * (1 + random.uniform(-0.3, 0.3))

            try:
                self.conn.set_param("SIM_GPS1_GLTCH_X", self._drift_lat)
                self.conn.set_param("SIM_GPS1_GLTCH_Y", self._drift_lon)
                self.conn.set_param("SIM_GPS1_GLTCH_Z", self._drift_alt)
            except Exception:
                self._drift_active = False
                self.after(0, lambda: self.drift_status_var.set(self._s("error")))
                break

            time.sleep(0.5)

    # ── Pitot tab ───────────────────────────────────────────────
    def _build_pitot_tab(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 6}

        self.arspd_fail = tk.DoubleVar(value=0)
        self.arspd_failp = tk.DoubleVar(value=0)
        self.arspd_sign_var = tk.IntVar(value=0)

        r = 0
        self.lbl_arspd_fail = ttk.Label(fr)
        self.lbl_arspd_fail.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.arspd_fail, 0, 80, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_fail, "tip_arspd_fail"); self._tip(sc, "tip_arspd_fail")

        r += 1
        self.lbl_arspd_failp = ttk.Label(fr)
        self.lbl_arspd_failp.grid(row=r, column=0, sticky="w", **pad)
        sc = self._make_scale(fr, self.arspd_failp, 0, 500, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_failp, "tip_arspd_failp"); self._tip(sc, "tip_arspd_failp")

        r += 1
        self.chk_arspd_sign = ttk.Checkbutton(fr, variable=self.arspd_sign_var)
        self.chk_arspd_sign.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        self._tip(self.chk_arspd_sign, "tip_arspd_sign")

        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=14)
        self.btn_apply_pitot = ttk.Button(btn_fr, style="Accent.TButton",
                                          command=self._apply_pitot)
        self.btn_apply_pitot.pack(side="left", padx=8)
        self.btn_reset_pitot = ttk.Button(btn_fr, style="Reset.TButton",
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
        self.arspd_fail.set(0); self.arspd_failp.set(0); self.arspd_sign_var.set(0)
        self._apply_pitot()

    # ── Connection ──────────────────────────────────────────────
    def _toggle_connection(self):
        if self.conn.connected:
            self._stop_drift()
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

        # wind
        self.lbl_wind_spd.configure(text=s["wind_spd"])
        self.lbl_wind_dir.configure(text=s["wind_dir"])
        self.lbl_wind_turb.configure(text=s["wind_turb"])
        self.lbl_wind_dir_z.configure(text=s["wind_dir_z"])
        self.btn_apply_wind.configure(text=s["apply_wind"])
        self.btn_reset_wind.configure(text=s["reset_wind"])

        # gps manual
        self.gps_nb.tab(0, text=s["gps_manual"])
        self.gps_nb.tab(1, text=s["gps_auto"])
        self.lbl_gps_lat.configure(text=s["gps_lat"])
        self.lbl_gps_lon.configure(text=s["gps_lon"])
        self.lbl_gps_alt.configure(text=s["gps_alt"])
        self.chk_gps_jam.configure(text=s["gps_jam"])
        self.lbl_gps_noise.configure(text=s["gps_noise"])
        self.btn_apply_gps.configure(text=s["apply_gps"])
        self.btn_reset_gps.configure(text=s["reset_gps"])

        # gps auto
        self.lbl_gps_preset.configure(text=s["gps_preset"])
        preset_keys = ["gps_preset_off", "gps_preset_weak", "gps_preset_medium",
                       "gps_preset_strong", "gps_preset_extreme"]
        for (rb, _val), key in zip(self.preset_radios, preset_keys):
            rb.configure(text=s[key])
        self.btn_apply_preset.configure(text=s["apply_gps"])

        self.lbl_gps_drift.configure(text=s["gps_drift"])
        self.chk_drift.configure(text=s["gps_drift_on"])
        self.lbl_drift_speed.configure(text=s["gps_drift_speed"])
        self.rb_drift_slow.configure(text=s["gps_drift_slow"])
        self.rb_drift_fast.configure(text=s["gps_drift_fast"])
        self.btn_start_drift.configure(text=s["gps_start_auto"])
        self.btn_stop_drift.configure(text=s["gps_stop_auto"])
        if self._drift_active:
            self.drift_status_var.set(s["gps_auto_active"])
        else:
            self.drift_status_var.set(s["gps_auto_stopped"])

        # pitot
        self.lbl_arspd_fail.configure(text=s["arspd_fail"])
        self.lbl_arspd_failp.configure(text=s["arspd_failp"])
        self.chk_arspd_sign.configure(text=s["arspd_sign"])
        self.btn_apply_pitot.configure(text=s["apply_pitot"])
        self.btn_reset_pitot.configure(text=s["reset_pitot"])

        # tooltips
        for tip, key in self.tooltips:
            tip.update_text(s.get(key, key))

    # ── Tooltip helper ──────────────────────────────────────────
    def _tip(self, widget, key):
        t = Tooltip(widget, self._s(key))
        self.tooltips.append((t, key))

    # ── Safe param send ─────────────────────────────────────────
    def _run_safe(self, fn):
        if not self.conn.connected:
            messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg"))
            return
        try:
            fn()
        except Exception as e:
            messagebox.showerror(self._s("error"), str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

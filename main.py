import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
import math
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
        "gps_auto": "Military Spoof",
        "gps_lat": "Latitude offset (deg)",
        "gps_lon": "Longitude offset (deg)",
        "gps_alt": "Altitude offset (m)",
        "gps_jam": "GPS jamming (no fix)",
        "gps_noise": "GPS noise (m)",
        "apply_gps": "Apply",
        "reset_gps": "Reset",

        # gps auto
        "gps_spoof_mode": "Spoofing mode:",
        "gps_mode_hold": "Hold at fake position",
        "gps_mode_drift": "Gradual drift",
        "gps_mode_circle": "Circle pattern",
        "gps_intensity": "Intensity:",
        "gps_int_weak": "Weak (~10 m)",
        "gps_int_medium": "Medium (~100 m)",
        "gps_int_strong": "Strong (~500 m)",
        "gps_int_extreme": "Extreme (~2 km)",
        "gps_speed_label": "Speed:",
        "gps_speed_slow": "Slow",
        "gps_speed_fast": "Fast",
        "gps_add_noise": "Add GPS noise",
        "gps_start_auto": "Start Spoofing",
        "gps_stop_auto": "Stop & Reset",
        "gps_auto_active": "ACTIVE - spoofing",
        "gps_auto_stopped": "Stopped",

        # pitot
        "pitot_mode": "Failure mode:",
        "pitot_blocked": "Blocked pitot tube (frozen reading)",
        "pitot_stuck": "Stuck at specific value",
        "pitot_reversed": "Reversed pitot/static lines",
        "pitot_noise": "Noisy sensor (random)",
        "arspd_fail_val": "Stuck airspeed (m/s)",
        "arspd_failp": "Blocked pressure (Pa)",
        "arspd_noise": "Noise amplitude (Pa)",
        "apply_pitot": "Activate Failure",
        "reset_pitot": "Reset (normal)",
        "pitot_fix_type": "Fix ARSPD_TYPE for SITL",
        "pitot_active": "FAILURE ACTIVE",
        "pitot_normal": "Normal",

        # tooltips
        "tip_wind_spd": "Simulated wind speed in m/s.\nSIM_WIND_SPD",
        "tip_wind_dir": "True direction the wind is coming FROM, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Random turbulence amplitude added to base wind.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Vertical wind angle: 0 = horizontal,\n+90 = pure updraft, -90 = pure downdraft.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Latitude glitch in degrees.\n0.00001 ~ 1.1 m, 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Longitude glitch in degrees.\n0.00001 ~ 1.1 m, 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Altitude glitch in meters.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Enable GPS signal jamming.\nSensor reports no fix at all.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Random altitude noise in meters\nadded to GPS readings.\nSIM_GPS1_NOISE",
        "tip_address": "MAVLink address. SITL creates TCP ports\n5760, 5762, 5763. Use a free one\nso Mission Planner can use another.",
        "tip_gps_mode": "Hold: teleport GPS to fake position and keep it there.\nDrift: slowly move GPS away from real position.\nCircle: GPS traces a circle around fake position.",
        "tip_gps_intensity": "How far from real position the fake GPS reports.\nWeak ~10m, Medium ~100m, Strong ~500m, Extreme ~2km.",
        "tip_pitot_blocked": "Simulates a fully blocked pitot tube.\nPressure freezes at a fixed value.\nTriggers 'Airspeed not healthy' after a few seconds.",
        "tip_pitot_stuck": "Airspeed sensor reports a constant speed\nregardless of actual vehicle speed.\nSIM_ARSPD_FAIL",
        "tip_pitot_reversed": "Simulates swapped pitot and static\nport connections. Airspeed reads\nnegative of actual value.\nSIM_ARSPD_SIGN",
        "tip_pitot_noise": "Adds large random noise to the sensor.\nMakes readings unreliable.\nSIM_ARSPD_RND",
        "tip_pitot_fix_type": "Your params have ARSPD_TYPE=8 (MSP)\nwhich doesn't work in SITL.\nSets ARSPD_TYPE=2 (analog) + ARSPD_PIN=1.\nREQUIRES SITL RESTART to take effect.",
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
        "gps_auto": "Военный спуф",
        "gps_lat": "Смещение широты (град)",
        "gps_lon": "Смещение долготы (град)",
        "gps_alt": "Смещение высоты (м)",
        "gps_jam": "Глушение GPS (нет фикса)",
        "gps_noise": "Шум GPS (м)",
        "apply_gps": "Применить",
        "reset_gps": "Сброс",

        "gps_spoof_mode": "Режим спуфинга:",
        "gps_mode_hold": "Удержание на фейковой позиции",
        "gps_mode_drift": "Плавный увод",
        "gps_mode_circle": "Движение по кругу",
        "gps_intensity": "Интенсивность:",
        "gps_int_weak": "Слабый (~10 м)",
        "gps_int_medium": "Средний (~100 м)",
        "gps_int_strong": "Сильный (~500 м)",
        "gps_int_extreme": "Экстремальный (~2 км)",
        "gps_speed_label": "Скорость:",
        "gps_speed_slow": "Медленно",
        "gps_speed_fast": "Быстро",
        "gps_add_noise": "Добавить GPS шум",
        "gps_start_auto": "Начать спуфинг",
        "gps_stop_auto": "Стоп и сброс",
        "gps_auto_active": "АКТИВНО - спуфинг",
        "gps_auto_stopped": "Остановлено",

        "pitot_mode": "Режим отказа:",
        "pitot_blocked": "Заблокированная трубка Пито (замёрзшие показания)",
        "pitot_stuck": "Залипание на конкретном значении",
        "pitot_reversed": "Перепутаны питот/статика линии",
        "pitot_noise": "Шумный датчик (случайный)",
        "arspd_fail_val": "Залипшая скорость (м/с)",
        "arspd_failp": "Давление блокировки (Па)",
        "arspd_noise": "Амплитуда шума (Па)",
        "apply_pitot": "Активировать отказ",
        "reset_pitot": "Сброс (норма)",
        "pitot_fix_type": "Исправить ARSPD_TYPE для SITL",
        "pitot_active": "ОТКАЗ АКТИВЕН",
        "pitot_normal": "Норма",

        "tip_wind_spd": "Скорость симулируемого ветра в м/с.\nSIM_WIND_SPD",
        "tip_wind_dir": "Истинное направление ОТКУДА дует ветер, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Амплитуда случайной турбулентн��сти\nповерх базового ветра.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Вертикальный угол ветра: 0 = горизонтально,\n+90 = восходящий, -90 = нисходящий.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Смещение широты в градусах.\n0.00001 ~ 1.1 м, 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Смещение долготы в градусах.\n0.00001 ~ 1.1 м, 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Смещение высоты в метрах.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Полное глушение GPS-сигнала.\nДатчик не может получить фикс.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Амплитуда случайного шума высоты\nдобавляемого к показаниям GPS.\nSIM_GPS1_NOISE",
        "tip_address": "MAVLink-адрес. SITL создаёт TCP-порты\n5760, 5762, 5763. Используйте свободный.",
        "tip_gps_mode": "Удержание: телепорт GPS на фейк и удержание.\nДрифт: медленный увод GPS от реальной позиции.\nКруг: GPS рисует круг вокруг фейка.",
        "tip_gps_intensity": "Как далеко от реальной позиции фейковый GPS.\nСлабый ~10м, Средний ~100м, Сильный ~500м, Экстрем ~2км.",
        "tip_pitot_blocked": "Имитация полностью забитой трубки Пито.\nДавление замерзает на фиксированном значении.\nВызывает 'Airspeed not healthy' через несколько секунд.",
        "tip_pitot_stuck": "Датчик скорости показывает постоянное значение\nвне зависимости от реальной скорости.\nSIM_ARSPD_FAIL",
        "tip_pitot_reversed": "Имитация перепутанного подключения\nпитот и статик портов. Скорость читается\nс обратным знаком.\nSIM_ARSPD_SIGN",
        "tip_pitot_noise": "Добавляет большой случайный шум к датчику.\nПоказания становятся ненадёжными.\nSIM_ARSPD_RND",
        "tip_pitot_fix_type": "В ваших параметрах ARSPD_TYPE=8 (MSP)\nкоторый не работает в SITL.\nЭто установит ARSPD_TYPE=0 (аналоговый)\nчтобы симуляция отказов работала.",
    },
}

# GPS intensity presets: (lat_deg, lon_deg, alt_m)
GPS_INTENSITY = {
    "weak":    (0.0001,  0.0001,  5.0),    # ~11 m
    "medium":  (0.001,   0.001,   15.0),   # ~111 m
    "strong":  (0.005,   0.005,   30.0),   # ~555 m
    "extreme": (0.02,    0.02,    50.0),   # ~2.2 km
}


# ═══════════════════════════════════════════════════════════════
#  Tooltip
# ═════════════════════════════════════════════════════════════���═
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
        tk.Label(tw, text=self.text, justify="left",
                 background="#2b2b2b", foreground="#e0e0e0",
                 relief="solid", borderwidth=1,
                 font=("Segoe UI", 9), padx=8, pady=4).pack()

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
BG       = "#1e1e2e"
FG       = "#cdd6f4"
ACCENT   = "#89b4fa"
GREEN    = "#a6e3a1"
RED      = "#f38ba8"
YELLOW   = "#f9e2af"
SURFACE  = "#313244"
ENTRY_BG = "#45475a"
ORANGE   = "#fab387"


# ═══════════════════════════════════════════════════════════════
#  Application
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.conn = SITLConnection()
        self.tooltips = []
        self._spoof_active = False
        self._pitot_fail_active = False

        self.title("SITL Fault Injection")
        self.geometry("700x640")
        self.resizable(False, False)
        self.configure(bg=BG)

        self._setup_styles()
        self._build_ui()
        self._apply_lang()

    def _setup_styles(self):
        s = ttk.Style(self)
        s.theme_use("clam")
        s.configure(".", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TLabelframe", background=BG, foreground=ACCENT, font=("Segoe UI", 10, "bold"))
        s.configure("TLabelframe.Label", background=BG, foreground=ACCENT)
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=SURFACE, foreground=FG, padding=(14, 6), font=("Segoe UI", 10, "bold"))
        s.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "#1e1e2e")])
        s.configure("Accent.TButton", background=ACCENT, foreground="#1e1e2e", font=("Segoe UI", 10, "bold"), padding=(16, 6))
        s.map("Accent.TButton", background=[("active", "#b4d0fb"), ("disabled", SURFACE)])
        s.configure("Reset.TButton", background=SURFACE, foreground=YELLOW, font=("Segoe UI", 9), padding=(12, 4))
        s.map("Reset.TButton", background=[("active", ENTRY_BG)])
        s.configure("Stop.TButton", background=RED, foreground="#1e1e2e", font=("Segoe UI", 10, "bold"), padding=(16, 6))
        s.map("Stop.TButton", background=[("active", "#f5a0b8")])
        s.configure("Warn.TButton", background=ORANGE, foreground="#1e1e2e", font=("Segoe UI", 9, "bold"), padding=(10, 4))
        s.map("Warn.TButton", background=[("active", "#fbc9a0")])
        s.configure("Lang.TButton", background=SURFACE, foreground=YELLOW, font=("Segoe UI", 9, "bold"), padding=(8, 2))
        s.map("Lang.TButton", background=[("active", ENTRY_BG)])
        s.configure("Status.TLabel", background=BG, font=("Segoe UI", 10, "bold"))
        s.configure("Info.TLabel", background=BG, foreground=ORANGE, font=("Segoe UI", 9, "italic"))
        s.configure("Active.TLabel", background=BG, foreground=RED, font=("Segoe UI", 10, "bold"))
        s.configure("TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TCheckbutton", background=[("active", BG)])
        s.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG, insertcolor=FG)
        s.configure("TRadiobutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TRadiobutton", background=[("active", BG)])

    def _make_scale(self, parent, variable, from_, to, resolution):
        return tk.Scale(parent, variable=variable, from_=from_, to=to,
                        orient="horizontal", length=320, resolution=resolution,
                        bg=BG, fg=FG, troughcolor=SURFACE, activebackground=ACCENT,
                        highlightthickness=0, sliderrelief="flat", bd=0, font=("Segoe UI", 9))

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
        self.conn_btn = ttk.Button(inner, text="Connect", style="Accent.TButton", command=self._toggle_connection)
        self.conn_btn.pack(side="left", padx=(0, 10))
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(inner, textvariable=self.status_var, style="Status.TLabel", foreground=RED)
        self.status_label.pack(side="left", padx=4)
        self.lang_btn = ttk.Button(top, text="RU", style="Lang.TButton", command=self._toggle_lang, width=4)
        self.lang_btn.pack(side="right", padx=(10, 0), pady=6)

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
        self.btn_apply_wind = ttk.Button(btn_fr, style="Accent.TButton", command=self._apply_wind)
        self.btn_apply_wind.pack(side="left", padx=8)
        self.btn_reset_wind = ttk.Button(btn_fr, style="Reset.TButton", command=self._reset_wind)
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
        self.wind_spd.set(0); self.wind_dir.set(180); self.wind_turb.set(0); self.wind_dir_z.set(0)
        self._apply_wind()

    # ── GPS tab ───────────────────────────────────────���─────────
    def _build_gps_tab(self, parent):
        fr = ttk.Frame(parent)
        self.gps_nb = ttk.Notebook(fr)
        self.gps_nb.pack(fill="both", expand=True, padx=4, pady=4)
        self.gps_nb.add(self._build_gps_manual(self.gps_nb), text="Manual")
        self.gps_nb.add(self._build_gps_auto(self.gps_nb), text="Military Spoof")
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
        self.btn_apply_gps = ttk.Button(btn_fr, style="Accent.TButton", command=self._apply_gps)
        self.btn_apply_gps.pack(side="left", padx=8)
        self.btn_reset_gps = ttk.Button(btn_fr, style="Reset.TButton", command=self._reset_gps)
        self.btn_reset_gps.pack(side="left", padx=8)
        return fr

    def _build_gps_auto(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 4}

        # mode
        r = 0
        self.lbl_spoof_mode = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_spoof_mode.grid(row=r, column=0, sticky="w", **pad)
        self.spoof_mode_var = tk.StringVar(value="hold")
        mode_fr = ttk.Frame(fr)
        mode_fr.grid(row=r, column=1, sticky="w", **pad)
        self.rb_mode_hold = ttk.Radiobutton(mode_fr, variable=self.spoof_mode_var, value="hold")
        self.rb_mode_hold.pack(anchor="w")
        self.rb_mode_drift = ttk.Radiobutton(mode_fr, variable=self.spoof_mode_var, value="drift")
        self.rb_mode_drift.pack(anchor="w")
        self.rb_mode_circle = ttk.Radiobutton(mode_fr, variable=self.spoof_mode_var, value="circle")
        self.rb_mode_circle.pack(anchor="w")
        self._tip(self.lbl_spoof_mode, "tip_gps_mode")

        # intensity
        r += 1
        self.lbl_intensity = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_intensity.grid(row=r, column=0, sticky="w", **pad)
        self.intensity_var = tk.StringVar(value="medium")
        int_fr = ttk.Frame(fr)
        int_fr.grid(row=r, column=1, sticky="w", **pad)
        self.rb_int = []
        for val in ("weak", "medium", "strong", "extreme"):
            rb = ttk.Radiobutton(int_fr, variable=self.intensity_var, value=val)
            rb.pack(anchor="w")
            self.rb_int.append((rb, val))
        self._tip(self.lbl_intensity, "tip_gps_intensity")

        # speed
        r += 1
        self.lbl_spoof_speed = ttk.Label(fr)
        self.lbl_spoof_speed.grid(row=r, column=0, sticky="w", **pad)
        speed_fr = ttk.Frame(fr)
        speed_fr.grid(row=r, column=1, sticky="w", **pad)
        self.spoof_speed_var = tk.StringVar(value="slow")
        self.rb_spoof_slow = ttk.Radiobutton(speed_fr, variable=self.spoof_speed_var, value="slow")
        self.rb_spoof_slow.pack(side="left", padx=(0, 12))
        self.rb_spoof_fast = ttk.Radiobutton(speed_fr, variable=self.spoof_speed_var, value="fast")
        self.rb_spoof_fast.pack(side="left")

        # noise checkbox
        r += 1
        self.spoof_noise_var = tk.IntVar(value=1)
        self.chk_spoof_noise = ttk.Checkbutton(fr, variable=self.spoof_noise_var)
        self.chk_spoof_noise.grid(row=r, column=0, columnspan=2, sticky="w", **pad)

        # buttons
        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=8)
        self.btn_start_spoof = ttk.Button(btn_fr, style="Accent.TButton", command=self._start_spoof)
        self.btn_start_spoof.pack(side="left", padx=8)
        self.btn_stop_spoof = ttk.Button(btn_fr, style="Stop.TButton", command=self._stop_spoof)
        self.btn_stop_spoof.pack(side="left", padx=8)

        r += 1
        self.spoof_status_var = tk.StringVar(value="Stopped")
        self.spoof_status_label = ttk.Label(fr, textvariable=self.spoof_status_var, style="Info.TLabel")
        self.spoof_status_label.grid(row=r, column=0, columnspan=2, **pad)
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

    # ── Continuous GPS spoofing ───────────────────��─────────────
    def _start_spoof(self):
        if self._spoof_active:
            return
        if not self.conn.connected:
            messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg"))
            return
        self._spoof_active = True
        self.spoof_status_var.set(self._s("gps_auto_active"))
        self.spoof_status_label.configure(foreground=RED)
        threading.Thread(target=self._spoof_loop, daemon=True).start()

    def _stop_spoof(self):
        self._spoof_active = False
        self.spoof_status_var.set(self._s("gps_auto_stopped"))
        self.spoof_status_label.configure(foreground=FG)
        if self.conn.connected:
            try:
                self.conn.set_param("SIM_GPS1_GLTCH_X", 0)
                self.conn.set_param("SIM_GPS1_GLTCH_Y", 0)
                self.conn.set_param("SIM_GPS1_GLTCH_Z", 0)
                self.conn.set_param("SIM_GPS1_NOISE", 0)
            except Exception:
                pass

    def _spoof_loop(self):
        t = 0
        drift_lat = 0.0
        drift_lon = 0.0
        drift_alt = 0.0

        while self._spoof_active and self.conn.connected:
            mode = self.spoof_mode_var.get()
            intensity = self.intensity_var.get()
            speed = self.spoof_speed_var.get()
            add_noise = self.spoof_noise_var.get()

            max_lat, max_lon, max_alt = GPS_INTENSITY.get(intensity, GPS_INTENSITY["medium"])
            rate = 0.02 if speed == "slow" else 0.1  # fraction per tick
            noise_val = 5 if add_noise else 0

            if mode == "hold":
                # instant teleport and hold
                lat = max_lat + random.uniform(-max_lat * 0.05, max_lat * 0.05)
                lon = max_lon + random.uniform(-max_lon * 0.05, max_lon * 0.05)
                alt = max_alt + random.uniform(-1, 1)

            elif mode == "drift":
                # gradually increase offset
                drift_lat += max_lat * rate * (1 + random.uniform(-0.2, 0.2))
                drift_lon += max_lon * rate * (1 + random.uniform(-0.2, 0.2))
                drift_alt += max_alt * rate * 0.5 * (1 + random.uniform(-0.2, 0.2))
                # clamp to max
                drift_lat = min(drift_lat, max_lat * 3)
                drift_lon = min(drift_lon, max_lon * 3)
                drift_alt = min(drift_alt, max_alt * 3)
                lat = drift_lat
                lon = drift_lon
                alt = drift_alt

            elif mode == "circle":
                # trace a circle around the offset
                angular_speed = 0.05 if speed == "slow" else 0.2
                t += angular_speed
                lat = max_lat * math.sin(t) + random.uniform(-max_lat * 0.02, max_lat * 0.02)
                lon = max_lon * math.cos(t) + random.uniform(-max_lon * 0.02, max_lon * 0.02)
                alt = max_alt * 0.5 * math.sin(t * 0.5)
            else:
                lat = lon = alt = 0

            try:
                self.conn.set_param("SIM_GPS1_GLTCH_X", lat)
                self.conn.set_param("SIM_GPS1_GLTCH_Y", lon)
                self.conn.set_param("SIM_GPS1_GLTCH_Z", alt)
                if add_noise:
                    self.conn.set_param("SIM_GPS1_NOISE", noise_val)
            except Exception:
                self._spoof_active = False
                self.after(0, lambda: self.spoof_status_var.set(self._s("error")))
                break

            time.sleep(0.3)

    # ── Pitot tab ───────────────────────────────────────────────
    def _build_pitot_tab(self, parent):
        fr = ttk.Frame(parent)
        pad = {"padx": 14, "pady": 5}

        # Fix ARSPD_TYPE button at top
        r = 0
        self.btn_fix_arspd = ttk.Button(fr, style="Warn.TButton", command=self._fix_arspd_type)
        self.btn_fix_arspd.grid(row=r, column=0, columnspan=2, pady=(8, 4), padx=14, sticky="w")
        self._tip(self.btn_fix_arspd, "tip_pitot_fix_type")

        r += 1
        ttk.Separator(fr, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", padx=14, pady=4)

        # failure mode selector
        r += 1
        self.lbl_pitot_mode = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_pitot_mode.grid(row=r, column=0, sticky="nw", **pad)
        self.pitot_mode_var = tk.StringVar(value="blocked")
        mode_fr = ttk.Frame(fr)
        mode_fr.grid(row=r, column=1, sticky="w", **pad)
        self.rb_pitot_blocked = ttk.Radiobutton(mode_fr, variable=self.pitot_mode_var, value="blocked")
        self.rb_pitot_blocked.pack(anchor="w")
        self._tip(self.rb_pitot_blocked, "tip_pitot_blocked")
        self.rb_pitot_stuck = ttk.Radiobutton(mode_fr, variable=self.pitot_mode_var, value="stuck")
        self.rb_pitot_stuck.pack(anchor="w")
        self._tip(self.rb_pitot_stuck, "tip_pitot_stuck")
        self.rb_pitot_reversed = ttk.Radiobutton(mode_fr, variable=self.pitot_mode_var, value="reversed")
        self.rb_pitot_reversed.pack(anchor="w")
        self._tip(self.rb_pitot_reversed, "tip_pitot_reversed")
        self.rb_pitot_noise = ttk.Radiobutton(mode_fr, variable=self.pitot_mode_var, value="noise")
        self.rb_pitot_noise.pack(anchor="w")
        self._tip(self.rb_pitot_noise, "tip_pitot_noise")

        # stuck value
        r += 1
        self.lbl_arspd_fail_val = ttk.Label(fr)
        self.lbl_arspd_fail_val.grid(row=r, column=0, sticky="w", **pad)
        self.arspd_fail = tk.DoubleVar(value=0)
        sc = self._make_scale(fr, self.arspd_fail, 0, 80, 0.5)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_fail_val, "tip_pitot_stuck"); self._tip(sc, "tip_pitot_stuck")

        # blocked pressure
        r += 1
        self.lbl_arspd_failp = ttk.Label(fr)
        self.lbl_arspd_failp.grid(row=r, column=0, sticky="w", **pad)
        self.arspd_failp = tk.DoubleVar(value=0)
        sc = self._make_scale(fr, self.arspd_failp, 0, 500, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_failp, "tip_pitot_blocked"); self._tip(sc, "tip_pitot_blocked")

        # noise
        r += 1
        self.lbl_arspd_noise = ttk.Label(fr)
        self.lbl_arspd_noise.grid(row=r, column=0, sticky="w", **pad)
        self.arspd_noise = tk.DoubleVar(value=2)
        sc = self._make_scale(fr, self.arspd_noise, 0, 200, 1)
        sc.grid(row=r, column=1, **pad)
        self._tip(self.lbl_arspd_noise, "tip_pitot_noise"); self._tip(sc, "tip_pitot_noise")

        # buttons
        r += 1
        btn_fr = ttk.Frame(fr)
        btn_fr.grid(row=r, column=0, columnspan=2, pady=10)
        self.btn_apply_pitot = ttk.Button(btn_fr, style="Stop.TButton", command=self._apply_pitot)
        self.btn_apply_pitot.pack(side="left", padx=8)
        self.btn_reset_pitot = ttk.Button(btn_fr, style="Reset.TButton", command=self._reset_pitot)
        self.btn_reset_pitot.pack(side="left", padx=8)

        r += 1
        self.pitot_status_var = tk.StringVar(value="Normal")
        self.pitot_status_label = ttk.Label(fr, textvariable=self.pitot_status_var, style="Info.TLabel")
        self.pitot_status_label.grid(row=r, column=0, columnspan=2, **pad)
        return fr

    def _fix_arspd_type(self):
        """Set ARSPD_TYPE=2 (analog), ARSPD_PIN=1 for SITL, then warn about reboot"""
        def do():
            self.conn.set_param("ARSPD_TYPE", 2)
            self.conn.set_param("ARSPD_PIN", 1)
        self._run_safe(do)
        messagebox.showinfo(
            "Reboot required",
            "ARSPD_TYPE and ARSPD_PIN changed.\n\n"
            "You MUST restart SITL for this to take effect.\n"
            "Restart ArduPlane.exe, then reconnect."
        )

    def _apply_pitot(self):
        mode = self.pitot_mode_var.get()

        def do():
            # reset all first
            self.conn.set_param("SIM_ARSPD_FAIL", 0)
            self.conn.set_param("SIM_ARSPD_FAILP", 0)
            self.conn.set_param("SIM_ARSPD_PITOT", 0)
            self.conn.set_param("SIM_ARSPD_SIGN", 0)
            self.conn.set_param("SIM_ARSPD_RND", 2)  # default noise
            time.sleep(0.1)

            if mode == "blocked":
                # Blocked pitot tube: set FAILP equal to current barometric pressure
                # so tube_pressure = |baro - baro + 0| = 0 → airspeed reads ~0
                # SITL code: tube_pressure = abs(FAILP - baro + PITOT)
                # Setting FAILP = baro (~101325) and PITOT = 0 gives tube_pressure ≈ 0
                self.conn.set_param("SIM_ARSPD_FAILP", 101325)
                self.conn.set_param("SIM_ARSPD_PITOT", 0)
            elif mode == "stuck":
                val = self.arspd_fail.get()
                if val < 0.1:
                    val = 0.1  # must be >0 to activate (is_positive check)
                self.conn.set_param("SIM_ARSPD_FAIL", val)
            elif mode == "reversed":
                self.conn.set_param("SIM_ARSPD_SIGN", 1)
            elif mode == "noise":
                self.conn.set_param("SIM_ARSPD_RND", self.arspd_noise.get())

        self._run_safe(do)
        self.pitot_status_var.set(self._s("pitot_active"))
        self.pitot_status_label.configure(foreground=RED)
        self._pitot_fail_active = True

    def _reset_pitot(self):
        self._run_safe(lambda: [
            self.conn.set_param("SIM_ARSPD_FAIL", 0),
            self.conn.set_param("SIM_ARSPD_FAILP", 0),
            self.conn.set_param("SIM_ARSPD_PITOT", 0),
            self.conn.set_param("SIM_ARSPD_SIGN", 0),
            self.conn.set_param("SIM_ARSPD_RND", 2),
        ])
        self.pitot_status_var.set(self._s("pitot_normal"))
        self.pitot_status_label.configure(foreground=GREEN)
        self._pitot_fail_active = False

    # ── Connection ──────────────────────────────────────────────
    def _toggle_connection(self):
        if self.conn.connected:
            self._stop_spoof()
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
            self.status_var.set(s["connected"]); self.conn_btn.configure(text=s["disconnect"])
        else:
            self.status_var.set(s["disconnected"]); self.conn_btn.configure(text=s["connect"])

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
        self.lbl_spoof_mode.configure(text=s["gps_spoof_mode"])
        self.rb_mode_hold.configure(text=s["gps_mode_hold"])
        self.rb_mode_drift.configure(text=s["gps_mode_drift"])
        self.rb_mode_circle.configure(text=s["gps_mode_circle"])
        self.lbl_intensity.configure(text=s["gps_intensity"])
        int_keys = ["gps_int_weak", "gps_int_medium", "gps_int_strong", "gps_int_extreme"]
        for (rb, _), key in zip(self.rb_int, int_keys):
            rb.configure(text=s[key])
        self.lbl_spoof_speed.configure(text=s["gps_speed_label"])
        self.rb_spoof_slow.configure(text=s["gps_speed_slow"])
        self.rb_spoof_fast.configure(text=s["gps_speed_fast"])
        self.chk_spoof_noise.configure(text=s["gps_add_noise"])
        self.btn_start_spoof.configure(text=s["gps_start_auto"])
        self.btn_stop_spoof.configure(text=s["gps_stop_auto"])
        if self._spoof_active:
            self.spoof_status_var.set(s["gps_auto_active"])
        else:
            self.spoof_status_var.set(s["gps_auto_stopped"])

        # pitot
        self.btn_fix_arspd.configure(text=s["pitot_fix_type"])
        self.lbl_pitot_mode.configure(text=s["pitot_mode"])
        self.rb_pitot_blocked.configure(text=s["pitot_blocked"])
        self.rb_pitot_stuck.configure(text=s["pitot_stuck"])
        self.rb_pitot_reversed.configure(text=s["pitot_reversed"])
        self.rb_pitot_noise.configure(text=s["pitot_noise"])
        self.lbl_arspd_fail_val.configure(text=s["arspd_fail_val"])
        self.lbl_arspd_failp.configure(text=s["arspd_failp"])
        self.lbl_arspd_noise.configure(text=s["arspd_noise"])
        self.btn_apply_pitot.configure(text=s["apply_pitot"])
        self.btn_reset_pitot.configure(text=s["reset_pitot"])
        if self._pitot_fail_active:
            self.pitot_status_var.set(s["pitot_active"])
        else:
            self.pitot_status_var.set(s["pitot_normal"])

        for tip, key in self.tooltips:
            tip.update_text(s.get(key, key))

    def _tip(self, widget, key):
        t = Tooltip(widget, self._s(key))
        self.tooltips.append((t, key))

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

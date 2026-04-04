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
        "connection": "Connection", "address": "Address:",
        "connect": "Connect", "disconnect": "Disconnect",
        "connected": "Connected", "disconnected": "Disconnected",
        "connecting": "Connecting...", "failed": "Connection failed",
        "lang_btn": "RU", "not_connected": "Not connected",
        "not_connected_msg": "Connect to SITL first.",
        "conn_error": "Connection error", "error": "Error",

        "tab_wind": "Wind", "tab_gps": "GPS Spoofing",
        "tab_baro": "Baro Spoofing", "tab_pitot": "Pitot Failure",
        "tab_sensors": "Sensors", "tab_complex": "Complex Attack",

        # wind
        "wind_spd": "Wind speed (m/s)", "wind_dir": "Direction (deg)",
        "wind_turb": "Turbulence (m/s)", "wind_dir_z": "Vertical (deg)",
        "apply": "Apply", "reset": "Reset",

        # gps
        "gps_manual": "Manual", "gps_auto": "Military Spoof",
        "gps_lat": "Lat offset (deg)", "gps_lon": "Lon offset (deg)",
        "gps_alt": "Alt offset (m)", "gps_jam": "GPS jamming (no fix)",
        "gps_noise": "GPS noise (m)",
        "gps_vel_n": "Velocity N (m/s)", "gps_vel_e": "Velocity E (m/s)",
        "gps_vel_d": "Velocity D (m/s)", "gps_alt_ofs": "Alt bias (m)",
        "gps_alt_drift": "Alt drift (m/s)", "gps_numsats": "Num satellites",
        "gps_spoof_mode": "Mode:", "gps_mode_hold": "Hold fake position",
        "gps_mode_drift": "Gradual drift", "gps_mode_circle": "Circle pattern",
        "gps_intensity": "Intensity:",
        "gps_int_weak": "Weak (~10 m)", "gps_int_medium": "Medium (~100 m)",
        "gps_int_strong": "Strong (~500 m)", "gps_int_extreme": "Extreme (~2 km)",
        "gps_speed_label": "Speed:", "gps_speed_slow": "Slow", "gps_speed_fast": "Fast",
        "gps_add_noise": "Add GPS noise", "gps_start": "Start Spoofing",
        "gps_stop": "Stop & Reset", "gps_active": "ACTIVE", "gps_stopped": "Stopped",

        # baro
        "baro_glitch": "Altitude glitch (m)", "baro_drift": "Altitude drift (m/s)",
        "baro_freeze": "Freeze barometer", "baro_disable": "Disable barometer",
        "baro_noise": "Noise (m)", "baro_active": "BARO FAULT ACTIVE",
        "baro_normal": "Normal",

        # pitot
        "pitot_mode": "Failure mode:",
        "pitot_blocked": "Blocked pitot (zero airspeed)",
        "pitot_stuck": "Stuck at value", "pitot_reversed": "Reversed lines",
        "pitot_noise": "Noisy sensor",
        "arspd_fail_val": "Stuck speed (m/s)", "arspd_failp": "Block pressure (Pa)",
        "arspd_noise_val": "Noise (Pa)",
        "pitot_fix_type": "Fix ARSPD_TYPE for SITL",
        "pitot_activate": "Activate Failure", "pitot_active": "FAILURE ACTIVE",
        "pitot_normal": "Normal",

        # sensors
        "imu_section": "IMU Failures", "compass_section": "Compass Failures",
        "accel1_fail": "Accel 1 fail", "accel2_fail": "Accel 2 fail",
        "accel3_fail": "Accel 3 fail",
        "mag1_fail": "Compass 1 fail", "mag2_fail": "Compass 2 fail",
        "mag3_fail": "Compass 3 fail",
        "vib_freq_x": "Vibration X (Hz)", "vib_freq_y": "Vibration Y (Hz)",
        "vib_freq_z": "Vibration Z (Hz)",
        "gyro_drift": "Gyro drift (deg/s/min)",

        # complex
        "complex_title": "Complex Attack Scenarios",
        "complex_gps_denied": "GPS Denied Environment",
        "complex_sensor_deg": "Sensor Degradation",
        "complex_full_spoof": "Full Spoofing Attack",
        "complex_icing": "Icing Conditions",
        "complex_start": "Start Scenario", "complex_stop": "Stop All",
        "complex_active": "SCENARIO ACTIVE", "complex_stopped": "Stopped",

        # tooltips
        "tip_wind_spd": "Wind speed in m/s.\nSIM_WIND_SPD",
        "tip_wind_dir": "Direction wind comes FROM, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Random turbulence amplitude.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Vertical angle: 0=horiz, +90=updraft.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Lat glitch (deg). 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Lon glitch (deg). 0.0001 ~ 11 m.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Alt glitch in meters.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Kill GPS signal entirely.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Random altitude noise (m).\nSIM_GPS1_NOISE",
        "tip_gps_vel_n": "GPS velocity error North (m/s).\nSpoofs ground speed.\nSIM_GPS1_VERR_X",
        "tip_gps_vel_e": "GPS velocity error East (m/s).\nSpoofs ground speed.\nSIM_GPS1_VERR_Y",
        "tip_gps_vel_d": "GPS velocity error Down (m/s).\nSpoofs vertical speed.\nSIM_GPS1_VERR_Z",
        "tip_gps_alt_ofs": "Persistent GPS altitude bias (m).\nSIM_GPS1_ALT_OFS",
        "tip_gps_alt_drift": "GPS altitude drift rate (m/s).\nSIM_GPS1_DRFTALT",
        "tip_gps_numsats": "Reported satellite count.\nLow = poor fix quality.\nSIM_GPS1_NUMSATS",
        "tip_baro_glitch": "One-shot altitude error (m).\nSIM_BARO_GLITCH",
        "tip_baro_drift": "Continuous altitude drift (m/s).\nSIM_BARO_DRIFT",
        "tip_baro_freeze": "Freeze baro at last reading.\nSIM_BARO_FREEZE",
        "tip_baro_disable": "Completely disable barometer.\nSIM_BARO_DISABLE",
        "tip_baro_noise": "Random baro noise (m).\nDefault 0.2.\nSIM_BARO_RND",
        "tip_address": "MAVLink address. SITL TCP ports:\n5760, 5762, 5763. Use a free one.",
        "tip_pitot_fix_type": "Sets ARSPD_TYPE=2, ARSPD_PIN=1.\nREQUIRES SITL RESTART.",
        "tip_complex_denied": "GPS jamming + reduced sats + baro drift.\nSimulates flying near GPS jammer.",
        "tip_complex_degrad": "Gradual sensor degradation:\nincreasing noise on all sensors.",
        "tip_complex_spoof": "Full attack: GPS position spoof +\nvelocity spoof + baro manipulation.\nVehicle believes it's somewhere else.",
        "tip_complex_icing": "Pitot tube icing + baro pressure shift +\nincreased vibrations.\nSimulates in-flight icing.",
    },
    "ru": {
        "title": "SITL Fault Injection",
        "connection": "Подключение", "address": "Адрес:",
        "connect": "Подключить", "disconnect": "Отключить",
        "connected": "Подключено", "disconnected": "Отключено",
        "connecting": "Подключение...", "failed": "Ошибка",
        "lang_btn": "EN", "not_connected": "Нет подключения",
        "not_connected_msg": "Сначала подключитесь к SITL.",
        "conn_error": "Ошибка подключения", "error": "Ошибка",

        "tab_wind": "Ветер", "tab_gps": "GPS-спуфинг",
        "tab_baro": "Баро-спуфинг", "tab_pitot": "Отказ ПВД",
        "tab_sensors": "Датчики", "tab_complex": "Комплексная атака",

        "wind_spd": "Скорость ветра (м/с)", "wind_dir": "Направление (град)",
        "wind_turb": "Турбулентность (м/с)", "wind_dir_z": "Верт. угол (град)",
        "apply": "Применить", "reset": "Сброс",

        "gps_manual": "Ручное", "gps_auto": "Военный спуф",
        "gps_lat": "Смещение широты (град)", "gps_lon": "Смещение долготы (град)",
        "gps_alt": "Смещение высоты (м)", "gps_jam": "Глушение GPS (нет фикса)",
        "gps_noise": "Шум GPS (м)",
        "gps_vel_n": "Скорость N (м/с)", "gps_vel_e": "Скорость E (м/с)",
        "gps_vel_d": "Скорость D (м/с)", "gps_alt_ofs": "Смещение высоты (м)",
        "gps_alt_drift": "Дрифт высоты (м/с)", "gps_numsats": "Кол-во спутников",
        "gps_spoof_mode": "Режим:", "gps_mode_hold": "Удержание фейк позиции",
        "gps_mode_drift": "Плавный увод", "gps_mode_circle": "По кругу",
        "gps_intensity": "Интенсивность:",
        "gps_int_weak": "Слабый (~10 м)", "gps_int_medium": "Средний (~100 м)",
        "gps_int_strong": "Сильный (~500 м)", "gps_int_extreme": "Экстрем (~2 км)",
        "gps_speed_label": "Скорость:", "gps_speed_slow": "Медленно", "gps_speed_fast": "Быстро",
        "gps_add_noise": "Добавить GPS шум", "gps_start": "Начать спуфинг",
        "gps_stop": "Стоп и сброс", "gps_active": "АКТИВНО", "gps_stopped": "Остановлено",

        "baro_glitch": "Глитч высоты (м)", "baro_drift": "Дрифт высоты (м/с)",
        "baro_freeze": "Заморозить барометр", "baro_disable": "Отключить барометр",
        "baro_noise": "Шум (м)", "baro_active": "ОТКАЗ БАРО АКТИВЕН",
        "baro_normal": "Норма",

        "pitot_mode": "Режим отказа:",
        "pitot_blocked": "Забитая трубка (нулевая скорость)",
        "pitot_stuck": "Залипание на значении", "pitot_reversed": "Перепутаны линии",
        "pitot_noise": "Шумный датчик",
        "arspd_fail_val": "Залипшая скорость (м/с)", "arspd_failp": "Давление блокировки (Па)",
        "arspd_noise_val": "Шум (Па)",
        "pitot_fix_type": "Исправить ARSPD_TYPE для SITL",
        "pitot_activate": "Активировать отказ", "pitot_active": "ОТКАЗ АКТИВЕН",
        "pitot_normal": "Норма",

        "imu_section": "Отказы IMU", "compass_section": "Отказы компаса",
        "accel1_fail": "Акселерометр 1", "accel2_fail": "Акселерометр 2",
        "accel3_fail": "Акселерометр 3",
        "mag1_fail": "Компас 1", "mag2_fail": "Компас 2", "mag3_fail": "Компас 3",
        "vib_freq_x": "Вибрация X (Гц)", "vib_freq_y": "Вибрация Y (Гц)",
        "vib_freq_z": "Вибрация Z (Гц)",
        "gyro_drift": "Дрифт гиро (град/с/мин)",

        "complex_title": "Комплексные сценарии атак",
        "complex_gps_denied": "GPS-denied среда",
        "complex_sensor_deg": "Деградация датчиков",
        "complex_full_spoof": "Полная спуфинг-атака",
        "complex_icing": "Обледенение",
        "complex_start": "Запустить сценарий", "complex_stop": "Остановить всё",
        "complex_active": "СЦЕНАРИЙ АКТИВЕН", "complex_stopped": "Остановлено",

        "tip_wind_spd": "Скорость ветра в м/с.\nSIM_WIND_SPD",
        "tip_wind_dir": "Направление ОТКУДА дует, 0-360.\nSIM_WIND_DIR",
        "tip_wind_turb": "Амплитуда турбулентности.\nSIM_WIND_TURB",
        "tip_wind_dir_z": "Верт. угол: 0=гориз, +90=восход.\nSIM_WIND_DIR_Z",
        "tip_gps_lat": "Глитч широты (град). 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_X",
        "tip_gps_lon": "Глитч долготы (град). 0.0001 ~ 11 м.\nSIM_GPS1_GLTCH_Y",
        "tip_gps_alt": "Глитч высоты в метрах.\nSIM_GPS1_GLTCH_Z",
        "tip_gps_jam": "Полное глушение GPS.\nSIM_GPS1_JAM",
        "tip_gps_noise": "Случайный шум высоты (м).\nSIM_GPS1_NOISE",
        "tip_gps_vel_n": "Ошибка скорости на север (м/с).\nСпуфит граундспид.\nSIM_GPS1_VERR_X",
        "tip_gps_vel_e": "Ошибка скорости на восток (м/с).\nСпуфит граундспид.\nSIM_GPS1_VERR_Y",
        "tip_gps_vel_d": "Ошибка вертикальной скорости (м/с).\nSIM_GPS1_VERR_Z",
        "tip_gps_alt_ofs": "Постоянное смещение GPS высоты (м).\nSIM_GPS1_ALT_OFS",
        "tip_gps_alt_drift": "Дрифт GPS высоты (м/с).\nSIM_GPS1_DRFTALT",
        "tip_gps_numsats": "Кол-во спутников.\nМало = плохой фикс.\nSIM_GPS1_NUMSATS",
        "tip_baro_glitch": "Разовая ошибка высоты (м).\nSIM_BARO_GLITCH",
        "tip_baro_drift": "Непрерывный дрифт (м/с).\nSIM_BARO_DRIFT",
        "tip_baro_freeze": "Заморозить на последнем значении.\nSIM_BARO_FREEZE",
        "tip_baro_disable": "Полностью отключить барометр.\nSIM_BARO_DISABLE",
        "tip_baro_noise": "Случайный шум баро (м).\nПо умолчанию 0.2.\nSIM_BARO_RND",
        "tip_address": "MAVLink-адрес. SITL TCP-порты:\n5760, 5762, 5763.",
        "tip_pitot_fix_type": "Ставит ARSPD_TYPE=2, ARSPD_PIN=1.\nТРЕБУЕТ ПЕРЕЗАПУСК SITL.",
        "tip_complex_denied": "Глушение GPS + мало спутников +\nдрифт баро. Имитация полёта\nрядом с GPS-глушилкой.",
        "tip_complex_degrad": "Постепенная деградация всех датчиков:\nрастущий шум и дрифт.",
        "tip_complex_spoof": "Полная атака: спуф позиции GPS +\nскорости + манипуляция баро.\nАппарат думает что он в другом месте.",
        "tip_complex_icing": "Обледенение трубки Пито +\nсдвиг давления баро + вибрации.\nИмитация обледенения в полёте.",
    },
}

GPS_INTENSITY = {
    "weak":    (0.0001,  0.0001,  5.0),
    "medium":  (0.001,   0.001,   15.0),
    "strong":  (0.005,   0.005,   30.0),
    "extreme": (0.02,    0.02,    50.0),
}


# ═══════════════════════════════════════════════════════════════
#  Tooltip
# ═══════════════════════════════════════════════════════════════
class Tooltip:
    def __init__(self, widget, text):
        self.widget, self.text, self.tw = widget, text, None
        widget.bind("<Enter>", self._show)
        widget.bind("<Leave>", self._hide)

    def _show(self, _=None):
        if self.tw: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 4
        self.tw = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tk.Label(tw, text=self.text, justify="left", bg="#2b2b2b", fg="#e0e0e0",
                 relief="solid", borderwidth=1, font=("Segoe UI", 9), padx=8, pady=4).pack()

    def _hide(self, _=None):
        if self.tw: self.tw.destroy(); self.tw = None

    def update_text(self, t): self.text = t


# ═══════════════════════════════════════════════════════════════
#  MAVLink
# ═══════════════════════════════════════════════════════════════
class SITLConnection:
    def __init__(self):
        self.master = None
        self.connected = False
        self._lock = threading.Lock()

    def connect(self, addr):
        self.master = mavutil.mavlink_connection(addr)
        self.master.wait_heartbeat(timeout=5)
        self.connected = True

    def disconnect(self):
        if self.master: self.master.close()
        self.connected = False; self.master = None

    def set_param(self, name, value):
        if not self.connected: raise RuntimeError("Not connected")
        with self._lock:
            self.master.param_set_send(name, value)
            time.sleep(0.05)


# ═══════════════════════════════════════════════════════════════
#  Theme
# ═══════════════════════════════════════════════════════════════
BG, FG, ACCENT, GREEN = "#1e1e2e", "#cdd6f4", "#89b4fa", "#a6e3a1"
RED, YELLOW, SURFACE, ENTRY_BG = "#f38ba8", "#f9e2af", "#313244", "#45475a"
ORANGE = "#fab387"


# ═══════════════════════════════════════════════════════════════
#  App
# ═══════════════════════════════════════════════════════════════
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.conn = SITLConnection()
        self.tooltips = []
        self._spoof_active = False
        self._complex_active = False
        self._pitot_fail_active = False

        self.title("SITL Fault Injection")
        self.geometry("720x680")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._setup_styles()
        self._build_ui()
        self._apply_lang()

    def _setup_styles(self):
        s = ttk.Style(self); s.theme_use("clam")
        s.configure(".", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.configure("TLabelframe", background=BG, foreground=ACCENT, font=("Segoe UI", 10, "bold"))
        s.configure("TLabelframe.Label", background=BG, foreground=ACCENT)
        s.configure("TNotebook", background=BG, borderwidth=0)
        s.configure("TNotebook.Tab", background=SURFACE, foreground=FG, padding=(12, 5), font=("Segoe UI", 9, "bold"))
        s.map("TNotebook.Tab", background=[("selected", ACCENT)], foreground=[("selected", "#1e1e2e")])
        for name, bg, fg in [("Accent.TButton", ACCENT, "#1e1e2e"), ("Reset.TButton", SURFACE, YELLOW),
                              ("Stop.TButton", RED, "#1e1e2e"), ("Warn.TButton", ORANGE, "#1e1e2e"),
                              ("Lang.TButton", SURFACE, YELLOW)]:
            s.configure(name, background=bg, foreground=fg, font=("Segoe UI", 10, "bold"), padding=(14, 5))
            s.map(name, background=[("active", ENTRY_BG)])
        s.configure("Status.TLabel", background=BG, font=("Segoe UI", 10, "bold"))
        s.configure("Info.TLabel", background=BG, foreground=ORANGE, font=("Segoe UI", 9, "italic"))
        s.configure("TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TCheckbutton", background=[("active", BG)])
        s.configure("TEntry", fieldbackground=ENTRY_BG, foreground=FG, insertcolor=FG)
        s.configure("TRadiobutton", background=BG, foreground=FG, font=("Segoe UI", 10))
        s.map("TRadiobutton", background=[("active", BG)])

    def _sc(self, p, var, f, t, res):
        return tk.Scale(p, variable=var, from_=f, to=t, orient="horizontal", length=280,
                        resolution=res, bg=BG, fg=FG, troughcolor=SURFACE,
                        activebackground=ACCENT, highlightthickness=0, sliderrelief="flat",
                        bd=0, font=("Segoe UI", 8))

    def _row(self, fr, r, lbl_attr, var, f, t, res, tip_key, pad):
        lbl = ttk.Label(fr); lbl.grid(row=r, column=0, sticky="w", **pad)
        setattr(self, lbl_attr, lbl)
        sc = self._sc(fr, var, f, t, res); sc.grid(row=r, column=1, **pad)
        self._tip(lbl, tip_key); self._tip(sc, tip_key)
        return lbl, sc

    # ── Build UI ────────────────────────────────────────────
    def _build_ui(self):
        top = ttk.Frame(self); top.pack(fill="x", padx=10, pady=(8, 0))
        self.conn_frame = ttk.LabelFrame(top, text="Connection")
        self.conn_frame.pack(side="left", fill="x", expand=True)
        inner = ttk.Frame(self.conn_frame); inner.pack(padx=8, pady=5)
        self.addr_label = ttk.Label(inner); self.addr_label.pack(side="left", padx=(0, 4))
        self.addr_var = tk.StringVar(value="tcp:127.0.0.1:5762")
        e = ttk.Entry(inner, textvariable=self.addr_var, width=24); e.pack(side="left", padx=(0, 6))
        self._tip(e, "tip_address")
        self.conn_btn = ttk.Button(inner, style="Accent.TButton", command=self._toggle_connection)
        self.conn_btn.pack(side="left", padx=(0, 8))
        self.status_var = tk.StringVar(value="Disconnected")
        self.status_label = ttk.Label(inner, textvariable=self.status_var, style="Status.TLabel", foreground=RED)
        self.status_label.pack(side="left", padx=4)
        self.lang_btn = ttk.Button(top, text="RU", style="Lang.TButton", command=self._toggle_lang, width=4)
        self.lang_btn.pack(side="right", padx=(8, 0), pady=5)

        self.nb = ttk.Notebook(self); self.nb.pack(fill="both", expand=True, padx=10, pady=8)
        tabs = [
            self._build_wind_tab, self._build_gps_tab, self._build_baro_tab,
            self._build_pitot_tab, self._build_sensors_tab, self._build_complex_tab,
        ]
        self._tabs = [t(self.nb) for t in tabs]
        for t in self._tabs: self.nb.add(t, text="")

    # ═══ WIND ═══════════════════════════════════════════════
    def _build_wind_tab(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 5}
        self.wind_spd = tk.DoubleVar(value=0); self.wind_dir = tk.DoubleVar(value=180)
        self.wind_turb = tk.DoubleVar(value=0); self.wind_dir_z = tk.DoubleVar(value=0)
        self._row(fr, 0, "lw1", self.wind_spd, 0, 50, 0.5, "tip_wind_spd", pad)
        self._row(fr, 1, "lw2", self.wind_dir, 0, 360, 1, "tip_wind_dir", pad)
        self._row(fr, 2, "lw3", self.wind_turb, 0, 20, 0.5, "tip_wind_turb", pad)
        self._row(fr, 3, "lw4", self.wind_dir_z, -90, 90, 1, "tip_wind_dir_z", pad)
        bf = ttk.Frame(fr); bf.grid(row=4, column=0, columnspan=2, pady=12)
        self.btn_w_apply = ttk.Button(bf, style="Accent.TButton", command=self._apply_wind); self.btn_w_apply.pack(side="left", padx=6)
        self.btn_w_reset = ttk.Button(bf, style="Reset.TButton", command=self._reset_wind); self.btn_w_reset.pack(side="left", padx=6)
        return fr

    def _apply_wind(self):
        self._safe(lambda: [self.conn.set_param("SIM_WIND_SPD", self.wind_spd.get()),
            self.conn.set_param("SIM_WIND_DIR", self.wind_dir.get()),
            self.conn.set_param("SIM_WIND_TURB", self.wind_turb.get()),
            self.conn.set_param("SIM_WIND_DIR_Z", self.wind_dir_z.get())])

    def _reset_wind(self):
        self.wind_spd.set(0); self.wind_dir.set(180); self.wind_turb.set(0); self.wind_dir_z.set(0)
        self._apply_wind()

    # ═══ GPS ════════════════════════════════════════════════
    def _build_gps_tab(self, p):
        fr = ttk.Frame(p)
        self.gps_nb = ttk.Notebook(fr); self.gps_nb.pack(fill="both", expand=True, padx=4, pady=4)
        self.gps_nb.add(self._build_gps_manual(self.gps_nb), text="Manual")
        self.gps_nb.add(self._build_gps_auto(self.gps_nb), text="Military Spoof")
        return fr

    def _build_gps_manual(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 4}
        self.gps_lat = tk.DoubleVar(value=0); self.gps_lon = tk.DoubleVar(value=0)
        self.gps_alt = tk.DoubleVar(value=0); self.gps_jam_var = tk.IntVar(value=0)
        self.gps_noise = tk.DoubleVar(value=0)
        self.gps_vel_n = tk.DoubleVar(value=0); self.gps_vel_e = tk.DoubleVar(value=0)
        self.gps_vel_d = tk.DoubleVar(value=0)
        self.gps_alt_ofs = tk.DoubleVar(value=0); self.gps_alt_drift = tk.DoubleVar(value=0)
        self.gps_numsats = tk.IntVar(value=10)

        # position row
        r = 0
        for attr, var, tip in [("lg1", self.gps_lat, "tip_gps_lat"), ("lg2", self.gps_lon, "tip_gps_lon"),
                                ("lg3", self.gps_alt, "tip_gps_alt")]:
            lbl = ttk.Label(fr); lbl.grid(row=r, column=0, sticky="w", **pad); setattr(self, attr, lbl)
            e = ttk.Entry(fr, textvariable=var, width=12); e.grid(row=r, column=1, sticky="w", **pad)
            self._tip(lbl, tip); self._tip(e, tip); r += 1

        # velocity
        for attr, var, tip in [("lg_vn", self.gps_vel_n, "tip_gps_vel_n"), ("lg_ve", self.gps_vel_e, "tip_gps_vel_e"),
                                ("lg_vd", self.gps_vel_d, "tip_gps_vel_d")]:
            lbl = ttk.Label(fr); lbl.grid(row=r, column=0, sticky="w", **pad); setattr(self, attr, lbl)
            e = ttk.Entry(fr, textvariable=var, width=12); e.grid(row=r, column=1, sticky="w", **pad)
            self._tip(lbl, tip); self._tip(e, tip); r += 1

        # alt ofs/drift
        self._row(fr, r, "lg_ao", self.gps_alt_ofs, -200, 200, 1, "tip_gps_alt_ofs", pad); r += 1
        self._row(fr, r, "lg_ad", self.gps_alt_drift, -5, 5, 0.1, "tip_gps_alt_drift", pad); r += 1
        self._row(fr, r, "lg_ns", self.gps_numsats, 0, 20, 1, "tip_gps_numsats", pad); r += 1
        self._row(fr, r, "lg_no", self.gps_noise, 0, 50, 1, "tip_gps_noise", pad); r += 1

        self.chk_gps_jam = ttk.Checkbutton(fr, variable=self.gps_jam_var)
        self.chk_gps_jam.grid(row=r, column=0, columnspan=2, sticky="w", **pad); self._tip(self.chk_gps_jam, "tip_gps_jam"); r += 1

        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=8)
        self.btn_g_apply = ttk.Button(bf, style="Accent.TButton", command=self._apply_gps); self.btn_g_apply.pack(side="left", padx=6)
        self.btn_g_reset = ttk.Button(bf, style="Reset.TButton", command=self._reset_gps); self.btn_g_reset.pack(side="left", padx=6)
        return fr

    def _build_gps_auto(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 3}
        r = 0
        self.lbl_spoof_mode = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_spoof_mode.grid(row=r, column=0, sticky="w", **pad)
        self.spoof_mode_var = tk.StringVar(value="hold")
        mf = ttk.Frame(fr); mf.grid(row=r, column=1, sticky="w", **pad)
        self.rb_mode = {}
        for v in ("hold", "drift", "circle"):
            rb = ttk.Radiobutton(mf, variable=self.spoof_mode_var, value=v); rb.pack(anchor="w")
            self.rb_mode[v] = rb
        self._tip(self.lbl_spoof_mode, "tip_complex_spoof")
        r += 1
        self.lbl_intensity = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_intensity.grid(row=r, column=0, sticky="w", **pad)
        self.intensity_var = tk.StringVar(value="medium")
        inf = ttk.Frame(fr); inf.grid(row=r, column=1, sticky="w", **pad)
        self.rb_int = []
        for v in ("weak", "medium", "strong", "extreme"):
            rb = ttk.Radiobutton(inf, variable=self.intensity_var, value=v); rb.pack(anchor="w"); self.rb_int.append((rb, v))
        r += 1
        self.lbl_sp_speed = ttk.Label(fr); self.lbl_sp_speed.grid(row=r, column=0, sticky="w", **pad)
        sf = ttk.Frame(fr); sf.grid(row=r, column=1, sticky="w", **pad)
        self.spoof_speed_var = tk.StringVar(value="slow")
        self.rb_sp_slow = ttk.Radiobutton(sf, variable=self.spoof_speed_var, value="slow"); self.rb_sp_slow.pack(side="left", padx=(0, 10))
        self.rb_sp_fast = ttk.Radiobutton(sf, variable=self.spoof_speed_var, value="fast"); self.rb_sp_fast.pack(side="left")
        r += 1
        self.spoof_noise_var = tk.IntVar(value=1)
        self.chk_sp_noise = ttk.Checkbutton(fr, variable=self.spoof_noise_var)
        self.chk_sp_noise.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
        r += 1
        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=6)
        self.btn_sp_start = ttk.Button(bf, style="Accent.TButton", command=self._start_spoof); self.btn_sp_start.pack(side="left", padx=6)
        self.btn_sp_stop = ttk.Button(bf, style="Stop.TButton", command=self._stop_spoof); self.btn_sp_stop.pack(side="left", padx=6)
        r += 1
        self.sp_status_var = tk.StringVar(value="Stopped")
        self.sp_status = ttk.Label(fr, textvariable=self.sp_status_var, style="Info.TLabel")
        self.sp_status.grid(row=r, column=0, columnspan=2, **pad)
        return fr

    def _apply_gps(self):
        self._safe(lambda: [
            self.conn.set_param("SIM_GPS1_GLTCH_X", self.gps_lat.get()),
            self.conn.set_param("SIM_GPS1_GLTCH_Y", self.gps_lon.get()),
            self.conn.set_param("SIM_GPS1_GLTCH_Z", self.gps_alt.get()),
            self.conn.set_param("SIM_GPS1_VERR_X", self.gps_vel_n.get()),
            self.conn.set_param("SIM_GPS1_VERR_Y", self.gps_vel_e.get()),
            self.conn.set_param("SIM_GPS1_VERR_Z", self.gps_vel_d.get()),
            self.conn.set_param("SIM_GPS1_ALT_OFS", self.gps_alt_ofs.get()),
            self.conn.set_param("SIM_GPS1_DRFTALT", self.gps_alt_drift.get()),
            self.conn.set_param("SIM_GPS1_NUMSATS", self.gps_numsats.get()),
            self.conn.set_param("SIM_GPS1_NOISE", self.gps_noise.get()),
            self.conn.set_param("SIM_GPS1_JAM", self.gps_jam_var.get()),
        ])

    def _reset_gps(self):
        for v in [self.gps_lat, self.gps_lon, self.gps_alt, self.gps_vel_n, self.gps_vel_e,
                  self.gps_vel_d, self.gps_alt_ofs, self.gps_alt_drift, self.gps_noise]:
            v.set(0)
        self.gps_numsats.set(10); self.gps_jam_var.set(0)
        self._apply_gps()

    def _start_spoof(self):
        if self._spoof_active: return
        if not self.conn.connected: messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg")); return
        self._spoof_active = True
        self.sp_status_var.set(self._s("gps_active")); self.sp_status.configure(foreground=RED)
        threading.Thread(target=self._spoof_loop, daemon=True).start()

    def _stop_spoof(self):
        self._spoof_active = False
        self.sp_status_var.set(self._s("gps_stopped")); self.sp_status.configure(foreground=FG)
        if self.conn.connected:
            try:
                for p in ["SIM_GPS1_GLTCH_X","SIM_GPS1_GLTCH_Y","SIM_GPS1_GLTCH_Z",
                           "SIM_GPS1_VERR_X","SIM_GPS1_VERR_Y","SIM_GPS1_VERR_Z",
                           "SIM_GPS1_NOISE","SIM_GPS1_ALT_OFS","SIM_GPS1_DRFTALT"]:
                    self.conn.set_param(p, 0)
                self.conn.set_param("SIM_GPS1_NUMSATS", 10)
            except Exception: pass

    def _spoof_loop(self):
        t = 0; drift_lat = drift_lon = drift_alt = 0.0
        while self._spoof_active and self.conn.connected:
            mode = self.spoof_mode_var.get()
            ml, mo, ma = GPS_INTENSITY.get(self.intensity_var.get(), GPS_INTENSITY["medium"])
            rate = 0.02 if self.spoof_speed_var.get() == "slow" else 0.1
            noise = 5 if self.spoof_noise_var.get() else 0
            rr = lambda v: random.uniform(-v*0.05, v*0.05)
            if mode == "hold":
                lat, lon, alt = ml+rr(ml), mo+rr(mo), ma+random.uniform(-1,1)
            elif mode == "drift":
                drift_lat += ml*rate*(1+random.uniform(-0.2,0.2))
                drift_lon += mo*rate*(1+random.uniform(-0.2,0.2))
                drift_alt += ma*rate*0.5
                drift_lat=min(drift_lat,ml*3); drift_lon=min(drift_lon,mo*3); drift_alt=min(drift_alt,ma*3)
                lat,lon,alt = drift_lat, drift_lon, drift_alt
            elif mode == "circle":
                asp = 0.05 if self.spoof_speed_var.get() == "slow" else 0.2; t += asp
                lat,lon,alt = ml*math.sin(t)+rr(ml), mo*math.cos(t)+rr(mo), ma*0.5*math.sin(t*0.5)
            else: lat=lon=alt=0
            try:
                self.conn.set_param("SIM_GPS1_GLTCH_X", lat)
                self.conn.set_param("SIM_GPS1_GLTCH_Y", lon)
                self.conn.set_param("SIM_GPS1_GLTCH_Z", alt)
                # also spoof velocity proportional to position change
                self.conn.set_param("SIM_GPS1_VERR_X", lat * 1000 * random.uniform(0.8, 1.2))
                self.conn.set_param("SIM_GPS1_VERR_Y", lon * 1000 * random.uniform(0.8, 1.2))
                if noise: self.conn.set_param("SIM_GPS1_NOISE", noise)
            except Exception: self._spoof_active = False; break
            time.sleep(0.3)

    # ═══ BARO ═══════════════════════════════════════════════
    def _build_baro_tab(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 5}
        self.baro_glitch = tk.DoubleVar(value=0); self.baro_drift = tk.DoubleVar(value=0)
        self.baro_noise = tk.DoubleVar(value=0.2)
        self.baro_freeze_var = tk.IntVar(value=0); self.baro_disable_var = tk.IntVar(value=0)

        self._row(fr, 0, "lb1", self.baro_glitch, -200, 200, 1, "tip_baro_glitch", pad)
        self._row(fr, 1, "lb2", self.baro_drift, -5, 5, 0.1, "tip_baro_drift", pad)
        self._row(fr, 2, "lb3", self.baro_noise, 0, 20, 0.1, "tip_baro_noise", pad)

        r = 3
        self.chk_baro_freeze = ttk.Checkbutton(fr, variable=self.baro_freeze_var)
        self.chk_baro_freeze.grid(row=r, column=0, columnspan=2, sticky="w", **pad); self._tip(self.chk_baro_freeze, "tip_baro_freeze"); r += 1
        self.chk_baro_disable = ttk.Checkbutton(fr, variable=self.baro_disable_var)
        self.chk_baro_disable.grid(row=r, column=0, columnspan=2, sticky="w", **pad); self._tip(self.chk_baro_disable, "tip_baro_disable"); r += 1

        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=10)
        self.btn_b_apply = ttk.Button(bf, style="Accent.TButton", command=self._apply_baro); self.btn_b_apply.pack(side="left", padx=6)
        self.btn_b_reset = ttk.Button(bf, style="Reset.TButton", command=self._reset_baro); self.btn_b_reset.pack(side="left", padx=6)
        r += 1
        self.baro_status_var = tk.StringVar(value="Normal")
        self.baro_status = ttk.Label(fr, textvariable=self.baro_status_var, style="Info.TLabel")
        self.baro_status.grid(row=r, column=0, columnspan=2, **pad)
        return fr

    def _apply_baro(self):
        def do():
            self.conn.set_param("SIM_BARO_GLITCH", self.baro_glitch.get())
            self.conn.set_param("SIM_BARO_DRIFT", self.baro_drift.get())
            self.conn.set_param("SIM_BARO_RND", self.baro_noise.get())
            self.conn.set_param("SIM_BARO_FREEZE", self.baro_freeze_var.get())
            self.conn.set_param("SIM_BARO_DISABLE", self.baro_disable_var.get())
        self._safe(do)
        self.baro_status_var.set(self._s("baro_active")); self.baro_status.configure(foreground=RED)

    def _reset_baro(self):
        self.baro_glitch.set(0); self.baro_drift.set(0); self.baro_noise.set(0.2)
        self.baro_freeze_var.set(0); self.baro_disable_var.set(0)
        self._safe(lambda: [self.conn.set_param("SIM_BARO_GLITCH",0), self.conn.set_param("SIM_BARO_DRIFT",0),
            self.conn.set_param("SIM_BARO_RND",0.2), self.conn.set_param("SIM_BARO_FREEZE",0),
            self.conn.set_param("SIM_BARO_DISABLE",0)])
        self.baro_status_var.set(self._s("baro_normal")); self.baro_status.configure(foreground=GREEN)

    # ═══ PITOT ══════════════════════════════════════════════
    def _build_pitot_tab(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 5}
        r = 0
        self.btn_fix_arspd = ttk.Button(fr, style="Warn.TButton", command=self._fix_arspd)
        self.btn_fix_arspd.grid(row=r, column=0, columnspan=2, pady=(6,2), padx=12, sticky="w"); self._tip(self.btn_fix_arspd, "tip_pitot_fix_type"); r += 1
        ttk.Separator(fr, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", padx=12, pady=4); r += 1

        self.lbl_pitot_mode = ttk.Label(fr, font=("Segoe UI", 10, "bold"))
        self.lbl_pitot_mode.grid(row=r, column=0, sticky="nw", **pad)
        self.pitot_mode_var = tk.StringVar(value="blocked")
        mf = ttk.Frame(fr); mf.grid(row=r, column=1, sticky="w", **pad)
        self.rb_pitot = {}
        for v in ("blocked", "stuck", "reversed", "noise"):
            rb = ttk.Radiobutton(mf, variable=self.pitot_mode_var, value=v); rb.pack(anchor="w"); self.rb_pitot[v] = rb
        r += 1
        self.arspd_fail = tk.DoubleVar(value=0); self.arspd_failp = tk.DoubleVar(value=0); self.arspd_noise = tk.DoubleVar(value=2)
        self._row(fr, r, "lp1", self.arspd_fail, 0, 80, 0.5, "tip_gps_vel_n", pad); r += 1
        self._row(fr, r, "lp2", self.arspd_failp, 0, 500, 1, "tip_baro_glitch", pad); r += 1
        self._row(fr, r, "lp3", self.arspd_noise, 0, 200, 1, "tip_baro_noise", pad); r += 1

        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=8)
        self.btn_p_apply = ttk.Button(bf, style="Stop.TButton", command=self._apply_pitot); self.btn_p_apply.pack(side="left", padx=6)
        self.btn_p_reset = ttk.Button(bf, style="Reset.TButton", command=self._reset_pitot); self.btn_p_reset.pack(side="left", padx=6)
        r += 1
        self.pitot_status_var = tk.StringVar(value="Normal")
        self.pitot_status = ttk.Label(fr, textvariable=self.pitot_status_var, style="Info.TLabel")
        self.pitot_status.grid(row=r, column=0, columnspan=2, **pad)
        return fr

    def _fix_arspd(self):
        self._safe(lambda: [self.conn.set_param("ARSPD_TYPE", 2), self.conn.set_param("ARSPD_PIN", 1)])
        messagebox.showinfo("Reboot", "ARSPD_TYPE=2, PIN=1 set.\nRestart SITL to apply.")

    def _apply_pitot(self):
        mode = self.pitot_mode_var.get()
        def do():
            for p in ["SIM_ARSPD_FAIL","SIM_ARSPD_FAILP","SIM_ARSPD_PITOT","SIM_ARSPD_SIGN"]:
                self.conn.set_param(p, 0)
            self.conn.set_param("SIM_ARSPD_RND", 2); time.sleep(0.1)
            if mode == "blocked": self.conn.set_param("SIM_ARSPD_FAILP", 101325)
            elif mode == "stuck":
                v = max(self.arspd_fail.get(), 0.1); self.conn.set_param("SIM_ARSPD_FAIL", v)
            elif mode == "reversed": self.conn.set_param("SIM_ARSPD_SIGN", 1)
            elif mode == "noise": self.conn.set_param("SIM_ARSPD_RND", self.arspd_noise.get())
        self._safe(do)
        self.pitot_status_var.set(self._s("pitot_active")); self.pitot_status.configure(foreground=RED)

    def _reset_pitot(self):
        self._safe(lambda: [self.conn.set_param(p, 0) for p in ["SIM_ARSPD_FAIL","SIM_ARSPD_FAILP","SIM_ARSPD_PITOT","SIM_ARSPD_SIGN"]] +
                   [self.conn.set_param("SIM_ARSPD_RND", 2)])
        self.pitot_status_var.set(self._s("pitot_normal")); self.pitot_status.configure(foreground=GREEN)

    # ═══ SENSORS ════════════════════════════════════════════
    def _build_sensors_tab(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 4}
        r = 0
        self.lbl_imu = ttk.Label(fr, font=("Segoe UI", 10, "bold")); self.lbl_imu.grid(row=r, column=0, sticky="w", **pad); r += 1
        self.accel_vars = []
        self.accel_chks = []
        for i in range(3):
            v = tk.IntVar(value=0); self.accel_vars.append(v)
            c = ttk.Checkbutton(fr, variable=v); c.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
            self.accel_chks.append(c); r += 1

        self.gyro_drift = tk.DoubleVar(value=0)
        self._row(fr, r, "ls_gd", self.gyro_drift, 0, 20, 0.1, "tip_wind_turb", pad); r += 1

        self.vib_x = tk.DoubleVar(value=0); self.vib_y = tk.DoubleVar(value=0); self.vib_z = tk.DoubleVar(value=0)
        self._row(fr, r, "ls_vx", self.vib_x, 0, 300, 1, "tip_wind_spd", pad); r += 1
        self._row(fr, r, "ls_vy", self.vib_y, 0, 300, 1, "tip_wind_spd", pad); r += 1
        self._row(fr, r, "ls_vz", self.vib_z, 0, 300, 1, "tip_wind_spd", pad); r += 1

        ttk.Separator(fr, orient="horizontal").grid(row=r, column=0, columnspan=2, sticky="ew", padx=12, pady=4); r += 1
        self.lbl_comp = ttk.Label(fr, font=("Segoe UI", 10, "bold")); self.lbl_comp.grid(row=r, column=0, sticky="w", **pad); r += 1
        self.mag_vars = []
        self.mag_chks = []
        for i in range(3):
            v = tk.IntVar(value=0); self.mag_vars.append(v)
            c = ttk.Checkbutton(fr, variable=v); c.grid(row=r, column=0, columnspan=2, sticky="w", **pad)
            self.mag_chks.append(c); r += 1

        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=8)
        self.btn_s_apply = ttk.Button(bf, style="Accent.TButton", command=self._apply_sensors); self.btn_s_apply.pack(side="left", padx=6)
        self.btn_s_reset = ttk.Button(bf, style="Reset.TButton", command=self._reset_sensors); self.btn_s_reset.pack(side="left", padx=6)
        return fr

    def _apply_sensors(self):
        def do():
            for i, v in enumerate(self.accel_vars):
                self.conn.set_param(f"SIM_ACCEL{i+1}_FAIL", v.get())
            for i, v in enumerate(self.mag_vars):
                self.conn.set_param(f"SIM_MAG{i+1}_FAIL", v.get())
            self.conn.set_param("SIM_DRIFT_SPEED", self.gyro_drift.get())
            self.conn.set_param("SIM_VIB_FREQ_X", self.vib_x.get())
            self.conn.set_param("SIM_VIB_FREQ_Y", self.vib_y.get())
            self.conn.set_param("SIM_VIB_FREQ_Z", self.vib_z.get())
        self._safe(do)

    def _reset_sensors(self):
        for v in self.accel_vars + self.mag_vars: v.set(0)
        self.gyro_drift.set(0); self.vib_x.set(0); self.vib_y.set(0); self.vib_z.set(0)
        self._apply_sensors()

    # ═══ COMPLEX ════════════════════════════════════════════
    def _build_complex_tab(self, p):
        fr = ttk.Frame(p); pad = {"padx": 12, "pady": 6}
        r = 0
        self.lbl_cx_title = ttk.Label(fr, font=("Segoe UI", 11, "bold")); self.lbl_cx_title.grid(row=r, column=0, columnspan=2, sticky="w", **pad); r += 1
        self.complex_var = tk.StringVar(value="gps_denied")
        self.rb_cx = {}
        for v, tip in [("gps_denied", "tip_complex_denied"), ("sensor_deg", "tip_complex_degrad"),
                        ("full_spoof", "tip_complex_spoof"), ("icing", "tip_complex_icing")]:
            rb = ttk.Radiobutton(fr, variable=self.complex_var, value=v)
            rb.grid(row=r, column=0, columnspan=2, sticky="w", **pad); self._tip(rb, tip)
            self.rb_cx[v] = rb; r += 1

        bf = ttk.Frame(fr); bf.grid(row=r, column=0, columnspan=2, pady=12)
        self.btn_cx_start = ttk.Button(bf, style="Accent.TButton", command=self._start_complex); self.btn_cx_start.pack(side="left", padx=6)
        self.btn_cx_stop = ttk.Button(bf, style="Stop.TButton", command=self._stop_complex); self.btn_cx_stop.pack(side="left", padx=6)
        r += 1
        self.cx_status_var = tk.StringVar(value="Stopped")
        self.cx_status = ttk.Label(fr, textvariable=self.cx_status_var, style="Info.TLabel")
        self.cx_status.grid(row=r, column=0, columnspan=2, **pad)
        return fr

    def _start_complex(self):
        if self._complex_active: return
        if not self.conn.connected: messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg")); return
        self._complex_active = True
        self.cx_status_var.set(self._s("complex_active")); self.cx_status.configure(foreground=RED)
        threading.Thread(target=self._complex_loop, daemon=True).start()

    def _stop_complex(self):
        self._complex_active = False
        self.cx_status_var.set(self._s("complex_stopped")); self.cx_status.configure(foreground=FG)
        if not self.conn.connected: return
        try:
            for p in ["SIM_GPS1_GLTCH_X","SIM_GPS1_GLTCH_Y","SIM_GPS1_GLTCH_Z",
                       "SIM_GPS1_VERR_X","SIM_GPS1_VERR_Y","SIM_GPS1_VERR_Z",
                       "SIM_GPS1_JAM","SIM_GPS1_NOISE","SIM_GPS1_ALT_OFS","SIM_GPS1_DRFTALT",
                       "SIM_BARO_GLITCH","SIM_BARO_DRIFT","SIM_BARO_FREEZE",
                       "SIM_ARSPD_FAIL","SIM_ARSPD_FAILP","SIM_ARSPD_PITOT","SIM_ARSPD_SIGN",
                       "SIM_DRIFT_SPEED","SIM_VIB_FREQ_X","SIM_VIB_FREQ_Y","SIM_VIB_FREQ_Z"]:
                self.conn.set_param(p, 0)
            self.conn.set_param("SIM_GPS1_NUMSATS", 10)
            self.conn.set_param("SIM_BARO_RND", 0.2)
            self.conn.set_param("SIM_ARSPD_RND", 2)
            self.conn.set_param("SIM_BARO_DISABLE", 0)
        except Exception: pass

    def _complex_loop(self):
        scenario = self.complex_var.get()
        t = 0
        while self._complex_active and self.conn.connected:
            t += 1
            try:
                if scenario == "gps_denied":
                    # GPS jamming + degraded sats + baro drift
                    phase = min(t * 0.3, 1.0)  # ramp up over ~3 seconds
                    self.conn.set_param("SIM_GPS1_JAM", 1 if t > 10 else 0)
                    self.conn.set_param("SIM_GPS1_NUMSATS", max(0, int(10 - t * 0.5)))
                    self.conn.set_param("SIM_GPS1_NOISE", min(t * 2, 50))
                    self.conn.set_param("SIM_BARO_DRIFT", 0.3 * phase)
                    self.conn.set_param("SIM_BARO_RND", 0.2 + t * 0.1)

                elif scenario == "sensor_deg":
                    # gradual degradation of everything
                    self.conn.set_param("SIM_GPS1_NOISE", min(t * 0.5, 30))
                    self.conn.set_param("SIM_BARO_RND", 0.2 + t * 0.05)
                    self.conn.set_param("SIM_BARO_DRIFT", min(t * 0.02, 1.0))
                    self.conn.set_param("SIM_ARSPD_RND", 2 + t * 0.5)
                    self.conn.set_param("SIM_DRIFT_SPEED", min(t * 0.1, 5))
                    self.conn.set_param("SIM_VIB_FREQ_X", min(t * 2, 100))
                    self.conn.set_param("SIM_VIB_FREQ_Y", min(t * 2, 100))
                    self.conn.set_param("SIM_VIB_FREQ_Z", min(t * 3, 150))

                elif scenario == "full_spoof":
                    # full GPS + baro spoofing attack
                    drift = min(t * 0.00005, 0.005)
                    self.conn.set_param("SIM_GPS1_GLTCH_X", drift + random.uniform(-drift*0.05, drift*0.05))
                    self.conn.set_param("SIM_GPS1_GLTCH_Y", drift * 1.2 + random.uniform(-drift*0.05, drift*0.05))
                    self.conn.set_param("SIM_GPS1_GLTCH_Z", min(t * 0.2, 30))
                    self.conn.set_param("SIM_GPS1_VERR_X", min(t * 0.1, 5) * random.uniform(0.8, 1.2))
                    self.conn.set_param("SIM_GPS1_VERR_Y", min(t * 0.1, 5) * random.uniform(0.8, 1.2))
                    self.conn.set_param("SIM_GPS1_ALT_OFS", min(t * 0.5, 50))
                    self.conn.set_param("SIM_BARO_GLITCH", min(t * 0.3, 20))
                    self.conn.set_param("SIM_GPS1_NOISE", 3)

                elif scenario == "icing":
                    # pitot icing + baro shift + vibrations
                    ice = min(t * 0.01, 1.0)
                    # gradually increase fail pressure toward blocked
                    if ice > 0.5:
                        self.conn.set_param("SIM_ARSPD_FAILP", 101325 * ice)
                    self.conn.set_param("SIM_ARSPD_RND", 2 + t * 1.5)
                    self.conn.set_param("SIM_BARO_GLITCH", -min(t * 0.1, 5))  # pressure increase from ice
                    self.conn.set_param("SIM_VIB_FREQ_X", min(t * 3, 120))
                    self.conn.set_param("SIM_VIB_FREQ_Z", min(t * 4, 180))

            except Exception:
                self._complex_active = False; break
            time.sleep(0.5)

    # ── Connection ──────────────────────────────────────────
    def _toggle_connection(self):
        if self.conn.connected:
            self._stop_spoof(); self._stop_complex()
            self.conn.disconnect()
            self.status_var.set(self._s("disconnected")); self.status_label.configure(foreground=RED)
            self.conn_btn.configure(text=self._s("connect"))
        else:
            addr = self.addr_var.get().strip()
            self.status_var.set(self._s("connecting")); self.status_label.configure(foreground=YELLOW)
            self.update_idletasks()
            threading.Thread(target=self._do_connect, args=(addr,), daemon=True).start()

    def _do_connect(self, addr):
        try:
            self.conn.connect(addr)
            self.after(0, lambda: [self.status_var.set(self._s("connected")),
                self.status_label.configure(foreground=GREEN), self.conn_btn.configure(text=self._s("disconnect"))])
        except Exception as e:
            self.after(0, lambda: [self.status_var.set(self._s("failed")),
                self.status_label.configure(foreground=RED), messagebox.showerror(self._s("conn_error"), str(e))])

    # ── Language ────────────────────────────────────────────
    def _s(self, k): return STRINGS[self.lang].get(k, k)
    def _toggle_lang(self): self.lang = "ru" if self.lang == "en" else "en"; self._apply_lang()

    def _apply_lang(self):
        s = STRINGS[self.lang]; self.title(s["title"])
        self.conn_frame.configure(text=s["connection"]); self.addr_label.configure(text=s["address"])
        self.lang_btn.configure(text=s["lang_btn"])
        if self.conn.connected: self.status_var.set(s["connected"]); self.conn_btn.configure(text=s["disconnect"])
        else: self.status_var.set(s["disconnected"]); self.conn_btn.configure(text=s["connect"])

        tab_keys = ["tab_wind","tab_gps","tab_baro","tab_pitot","tab_sensors","tab_complex"]
        for i, k in enumerate(tab_keys): self.nb.tab(i, text=s[k])

        # wind
        self.lw1.configure(text=s["wind_spd"]); self.lw2.configure(text=s["wind_dir"])
        self.lw3.configure(text=s["wind_turb"]); self.lw4.configure(text=s["wind_dir_z"])
        self.btn_w_apply.configure(text=s["apply"]); self.btn_w_reset.configure(text=s["reset"])

        # gps manual
        self.gps_nb.tab(0, text=s["gps_manual"]); self.gps_nb.tab(1, text=s["gps_auto"])
        self.lg1.configure(text=s["gps_lat"]); self.lg2.configure(text=s["gps_lon"]); self.lg3.configure(text=s["gps_alt"])
        self.lg_vn.configure(text=s["gps_vel_n"]); self.lg_ve.configure(text=s["gps_vel_e"]); self.lg_vd.configure(text=s["gps_vel_d"])
        self.lg_ao.configure(text=s["gps_alt_ofs"]); self.lg_ad.configure(text=s["gps_alt_drift"])
        self.lg_ns.configure(text=s["gps_numsats"]); self.lg_no.configure(text=s["gps_noise"])
        self.chk_gps_jam.configure(text=s["gps_jam"])
        self.btn_g_apply.configure(text=s["apply"]); self.btn_g_reset.configure(text=s["reset"])

        # gps auto
        self.lbl_spoof_mode.configure(text=s["gps_spoof_mode"])
        self.rb_mode["hold"].configure(text=s["gps_mode_hold"])
        self.rb_mode["drift"].configure(text=s["gps_mode_drift"])
        self.rb_mode["circle"].configure(text=s["gps_mode_circle"])
        self.lbl_intensity.configure(text=s["gps_intensity"])
        for (rb,v), k in zip(self.rb_int, ["gps_int_weak","gps_int_medium","gps_int_strong","gps_int_extreme"]):
            rb.configure(text=s[k])
        self.lbl_sp_speed.configure(text=s["gps_speed_label"])
        self.rb_sp_slow.configure(text=s["gps_speed_slow"]); self.rb_sp_fast.configure(text=s["gps_speed_fast"])
        self.chk_sp_noise.configure(text=s["gps_add_noise"])
        self.btn_sp_start.configure(text=s["gps_start"]); self.btn_sp_stop.configure(text=s["gps_stop"])
        self.sp_status_var.set(s["gps_active"] if self._spoof_active else s["gps_stopped"])

        # baro
        self.lb1.configure(text=s["baro_glitch"]); self.lb2.configure(text=s["baro_drift"]); self.lb3.configure(text=s["baro_noise"])
        self.chk_baro_freeze.configure(text=s["baro_freeze"]); self.chk_baro_disable.configure(text=s["baro_disable"])
        self.btn_b_apply.configure(text=s["apply"]); self.btn_b_reset.configure(text=s["reset"])

        # pitot
        self.btn_fix_arspd.configure(text=s["pitot_fix_type"]); self.lbl_pitot_mode.configure(text=s["pitot_mode"])
        self.rb_pitot["blocked"].configure(text=s["pitot_blocked"]); self.rb_pitot["stuck"].configure(text=s["pitot_stuck"])
        self.rb_pitot["reversed"].configure(text=s["pitot_reversed"]); self.rb_pitot["noise"].configure(text=s["pitot_noise"])
        self.lp1.configure(text=s["arspd_fail_val"]); self.lp2.configure(text=s["arspd_failp"]); self.lp3.configure(text=s["arspd_noise_val"])
        self.btn_p_apply.configure(text=s["pitot_activate"]); self.btn_p_reset.configure(text=s["reset"])

        # sensors
        self.lbl_imu.configure(text=s["imu_section"]); self.lbl_comp.configure(text=s["compass_section"])
        for i, k in enumerate(["accel1_fail","accel2_fail","accel3_fail"]): self.accel_chks[i].configure(text=s[k])
        for i, k in enumerate(["mag1_fail","mag2_fail","mag3_fail"]): self.mag_chks[i].configure(text=s[k])
        self.ls_gd.configure(text=s["gyro_drift"])
        self.ls_vx.configure(text=s["vib_freq_x"]); self.ls_vy.configure(text=s["vib_freq_y"]); self.ls_vz.configure(text=s["vib_freq_z"])
        self.btn_s_apply.configure(text=s["apply"]); self.btn_s_reset.configure(text=s["reset"])

        # complex
        self.lbl_cx_title.configure(text=s["complex_title"])
        self.rb_cx["gps_denied"].configure(text=s["complex_gps_denied"])
        self.rb_cx["sensor_deg"].configure(text=s["complex_sensor_deg"])
        self.rb_cx["full_spoof"].configure(text=s["complex_full_spoof"])
        self.rb_cx["icing"].configure(text=s["complex_icing"])
        self.btn_cx_start.configure(text=s["complex_start"]); self.btn_cx_stop.configure(text=s["complex_stop"])
        self.cx_status_var.set(s["complex_active"] if self._complex_active else s["complex_stopped"])

        for tip, key in self.tooltips: tip.update_text(s.get(key, key))

    def _tip(self, w, k):
        t = Tooltip(w, self._s(k)); self.tooltips.append((t, k))

    def _safe(self, fn):
        if not self.conn.connected: messagebox.showwarning(self._s("not_connected"), self._s("not_connected_msg")); return
        try: fn()
        except Exception as e: messagebox.showerror(self._s("error"), str(e))


if __name__ == "__main__":
    App().mainloop()

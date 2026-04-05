import customtkinter as ctk
from tkinter import messagebox
import threading
import time
import random
import math
from pymavlink import mavutil

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── Localization ────────────────────────────────────────────
L = {
 "en": {
    "title":"SITL Fault Injection","connect":"Connect","disconnect":"Disconnect",
    "connected":"Connected","disconnected":"Disconnected","connecting":"Connecting...",
    "failed":"Failed","lang":"RU","no_conn":"Connect to SITL first.",
    "tab_wind":"Wind","tab_gps":"GPS","tab_baro":"Baro","tab_pitot":"Pitot",
    "tab_sensors":"Sensors","tab_complex":"Complex","tab_system":"System",
    "sys_sim_speed":"Simulation Speed","sys_speedup":"Speed multiplier",
    "sys_speed_presets":"Presets",
    "sys_batt":"Battery Simulation",
    "sys_batt_v":"Voltage (V)","sys_batt_cap":"Capacity (Ah)",
    "sys_batt_start_v":"Start voltage (V)","sys_batt_end_v":"End voltage (V)",
    "sys_batt_time":"Discharge time (min)","sys_batt_curve":"Curve",
    "sys_batt_linear":"Linear","sys_batt_lipo":"LiPo (realistic)",
    "sys_batt_start":"Start Discharge","sys_batt_stop":"Stop",
    "sys_batt_reset":"Reset to 12.6V","sys_batt_now":"Current voltage",
    "sys_batt_running":"DISCHARGING","sys_batt_idle":"Idle",
    "wind_spd":"Speed (m/s)","wind_dir":"Direction (deg)","wind_turb":"Turbulence (m/s)",
    "wind_dir_z":"Vertical angle (deg)",
    "apply":"Apply","reset":"Reset","start":"Start","stop":"Stop",
    "gps_manual":"Manual","gps_auto":"Auto Spoof",
    "gps_lat":"Lat offset (deg)","gps_lon":"Lon offset (deg)","gps_alt":"Alt offset (m)",
    "gps_jam":"GPS Jamming","gps_noise":"Noise (m)",
    "gps_vel_n":"Vel North (m/s)","gps_vel_e":"Vel East (m/s)","gps_vel_d":"Vel Down (m/s)",
    "gps_alt_ofs":"Alt bias (m)","gps_alt_drift":"Alt drift (m/s)","gps_numsats":"Satellites",
    "mode":"Mode","hold":"Hold position","drift":"Gradual drift","circle":"Circle",
    "intensity":"Intensity","weak":"Weak ~10m","medium":"Medium ~100m",
    "strong":"Strong ~500m","extreme":"Extreme ~2km",
    "speed":"Speed","slow":"Slow","fast":"Fast","add_noise":"Add noise",
    "active":"ACTIVE","stopped":"Stopped",
    "baro_glitch":"Glitch (m)","baro_drift":"Drift (m/s)","baro_noise":"Noise (m)",
    "baro_freeze":"Freeze","baro_disable":"Disable",
    "pitot_fix":"Fix ARSPD_TYPE for SITL","pitot_mode":"Failure mode",
    "blocked":"Blocked tube","stuck":"Stuck value","reversed":"Reversed","noisy":"Noisy",
    "stuck_val":"Stuck speed (m/s)","noise_pa":"Noise (Pa)","activate":"Activate",
    "imu":"IMU Failures","compass":"Compass Failures",
    "accel":"Accel","mag":"Compass","gyro_drift":"Gyro drift (deg/s/min)",
    "vib_x":"Vibration X (Hz)","vib_y":"Vibration Y (Hz)","vib_z":"Vibration Z (Hz)",
    "scenarios":"Attack Scenarios","gps_denied":"GPS Denied",
    "sensor_deg":"Sensor Degradation","full_spoof":"Full Spoofing",
    "icing":"Icing Conditions",
    "tip_wind_spd":"Simulated wind speed\nSIM_WIND_SPD",
    "tip_wind_dir":"Direction wind comes FROM\nSIM_WIND_DIR",
    "tip_wind_turb":"Turbulence amplitude\nSIM_WIND_TURB",
    "tip_wind_dir_z":"Vertical: 0=horiz, 90=up\nSIM_WIND_DIR_Z",
    "tip_gps_lat":"0.0001 ~ 11m\nSIM_GPS1_GLTCH_X",
    "tip_gps_lon":"0.0001 ~ 11m\nSIM_GPS1_GLTCH_Y",
    "tip_gps_alt":"Altitude glitch (m)\nSIM_GPS1_GLTCH_Z",
    "tip_gps_vel_n":"Ground speed spoof N\nSIM_GPS1_VERR_X",
    "tip_gps_vel_e":"Ground speed spoof E\nSIM_GPS1_VERR_Y",
    "tip_gps_vel_d":"Vertical speed spoof\nSIM_GPS1_VERR_Z",
    "tip_gps_alt_ofs":"Persistent alt bias\nSIM_GPS1_ALT_OFS",
    "tip_gps_alt_drift":"Alt drift rate\nSIM_GPS1_DRFTALT",
    "tip_gps_numsats":"Satellite count\nSIM_GPS1_NUMSATS",
    "tip_baro_glitch":"Altitude step error\nSIM_BARO_GLITCH",
    "tip_baro_drift":"Continuous drift\nSIM_BARO_DRIFT",
    "tip_baro_noise":"Random noise\nSIM_BARO_RND",
    "tip_baro_freeze":"Freeze at last value\nSIM_BARO_FREEZE",
    "tip_baro_disable":"Disable barometer\nSIM_BARO_DISABLE",
    "tip_pitot_fix":"Sets ARSPD_TYPE=2 PIN=1\nRequires SITL restart",
    "tip_blocked":"Pitot blocked, reads 0\nSIM_ARSPD_FAILP=101325",
    "tip_stuck":"Fixed airspeed value\nSIM_ARSPD_FAIL",
    "tip_reversed":"Swapped pitot/static\nSIM_ARSPD_SIGN",
    "tip_noisy":"Large sensor noise\nSIM_ARSPD_RND",
    "tip_gps_denied":"GPS jam + sat loss +\nbaro drift over time",
    "tip_sensor_deg":"All sensors degrade\nprogressively",
    "tip_full_spoof":"GPS + velocity + baro\ncoordinated attack",
    "tip_icing":"Pitot icing + baro shift\n+ vibrations",
  },
 "ru": {
    "title":"SITL Fault Injection","connect":"Подключить","disconnect":"Отключить",
    "connected":"Подключено","disconnected":"Отключено","connecting":"Подключение...",
    "failed":"Ошибка","lang":"EN","no_conn":"Сначала подключитесь к SITL.",
    "tab_wind":"Ветер","tab_gps":"GPS","tab_baro":"Баро","tab_pitot":"ПВД",
    "tab_sensors":"Датчики","tab_complex":"Комплекс","tab_system":"Система",
    "sys_sim_speed":"Скорость симуляции","sys_speedup":"Множитель скорости",
    "sys_speed_presets":"Пресеты",
    "sys_batt":"Симуляция батареи",
    "sys_batt_v":"Напряжение (В)","sys_batt_cap":"Ёмкость (Ач)",
    "sys_batt_start_v":"Старт напряжение (В)","sys_batt_end_v":"Конечное (В)",
    "sys_batt_time":"Время разряда (мин)","sys_batt_curve":"Кривая",
    "sys_batt_linear":"Линейная","sys_batt_lipo":"LiPo (реалистичная)",
    "sys_batt_start":"Начать разряд","sys_batt_stop":"Стоп",
    "sys_batt_reset":"Сброс к 12.6В","sys_batt_now":"Текущее напряжение",
    "sys_batt_running":"РАЗРЯЖАЕТСЯ","sys_batt_idle":"Ожидание",
    "wind_spd":"Скорость (м/с)","wind_dir":"Направление (град)","wind_turb":"Турбулентность (м/с)",
    "wind_dir_z":"Верт. угол (град)",
    "apply":"Применить","reset":"Сброс","start":"Старт","stop":"Стоп",
    "gps_manual":"Ручное","gps_auto":"Авто-спуф",
    "gps_lat":"Смещ. широты (град)","gps_lon":"Смещ. долготы (град)","gps_alt":"Смещ. высоты (м)",
    "gps_jam":"Глушение GPS","gps_noise":"Шум (м)",
    "gps_vel_n":"Скорость N (м/с)","gps_vel_e":"Скорость E (м/с)","gps_vel_d":"Скорость D (м/с)",
    "gps_alt_ofs":"Смещ. высоты (м)","gps_alt_drift":"Дрифт высоты (м/с)","gps_numsats":"Спутники",
    "mode":"Режим","hold":"Удержание","drift":"Плавный увод","circle":"По кругу",
    "intensity":"Интенсивность","weak":"Слабый ~10м","medium":"Средний ~100м",
    "strong":"Сильный ~500м","extreme":"Экстрем ~2км",
    "speed":"Скорость","slow":"Медленно","fast":"Быстро","add_noise":"Добавить шум",
    "active":"АКТИВНО","stopped":"Остановлено",
    "baro_glitch":"Глитч (м)","baro_drift":"Дрифт (м/с)","baro_noise":"Шум (м)",
    "baro_freeze":"Заморозить","baro_disable":"Отключить",
    "pitot_fix":"Исправить ARSPD_TYPE","pitot_mode":"Режим отказа",
    "blocked":"Забитая трубка","stuck":"Залипание","reversed":"Реверс","noisy":"Шумный",
    "stuck_val":"Залипшая скорость (м/с)","noise_pa":"Шум (Па)","activate":"Активировать",
    "imu":"Отказы IMU","compass":"Отказы компаса",
    "accel":"Акселерометр","mag":"Компас","gyro_drift":"Дрифт гиро (град/с/мин)",
    "vib_x":"Вибрация X (Гц)","vib_y":"Вибрация Y (Гц)","vib_z":"Вибрация Z (Гц)",
    "scenarios":"Сценарии атак","gps_denied":"GPS Denied",
    "sensor_deg":"Деградация датчиков","full_spoof":"Полный спуфинг",
    "icing":"Обледенение",
    "tip_wind_spd":"Скорость ветра\nSIM_WIND_SPD",
    "tip_wind_dir":"Откуда дует ветер\nSIM_WIND_DIR",
    "tip_wind_turb":"Амплитуда турбулентности\nSIM_WIND_TURB",
    "tip_wind_dir_z":"0=гориз, 90=восход\nSIM_WIND_DIR_Z",
    "tip_gps_lat":"0.0001 ~ 11м\nSIM_GPS1_GLTCH_X",
    "tip_gps_lon":"0.0001 ~ 11м\nSIM_GPS1_GLTCH_Y",
    "tip_gps_alt":"Глитч высоты (м)\nSIM_GPS1_GLTCH_Z",
    "tip_gps_vel_n":"Спуф граундспида N\nSIM_GPS1_VERR_X",
    "tip_gps_vel_e":"Спуф граундспида E\nSIM_GPS1_VERR_Y",
    "tip_gps_vel_d":"Спуф верт. скорости\nSIM_GPS1_VERR_Z",
    "tip_gps_alt_ofs":"Постоянное смещение\nSIM_GPS1_ALT_OFS",
    "tip_gps_alt_drift":"Скорость дрифта\nSIM_GPS1_DRFTALT",
    "tip_gps_numsats":"Кол-во спутников\nSIM_GPS1_NUMSATS",
    "tip_baro_glitch":"Разовый сдвиг высоты\nSIM_BARO_GLITCH",
    "tip_baro_drift":"Непрерывный дрифт\nSIM_BARO_DRIFT",
    "tip_baro_noise":"Случайный шум\nSIM_BARO_RND",
    "tip_baro_freeze":"Заморозка на последнем\nSIM_BARO_FREEZE",
    "tip_baro_disable":"Полное отключение\nSIM_BARO_DISABLE",
    "tip_pitot_fix":"ARSPD_TYPE=2 PIN=1\nТребует перезапуск SITL",
    "tip_blocked":"Забитая трубка, скорость=0\nSIM_ARSPD_FAILP=101325",
    "tip_stuck":"Фиксированная скорость\nSIM_ARSPD_FAIL",
    "tip_reversed":"Перепутаны порты\nSIM_ARSPD_SIGN",
    "tip_noisy":"Большой шум\nSIM_ARSPD_RND",
    "tip_gps_denied":"Глушение + потеря спутников\n+ дрифт баро",
    "tip_sensor_deg":"Все датчики деградируют\nпостепенно",
    "tip_full_spoof":"GPS + скорость + баро\nкоординированная атака",
    "tip_icing":"Обледенение ПВД +\nсдвиг баро + вибрации",
  },
}

GPS_INT = {"weak":(0.0001,0.0001,5),"medium":(0.001,0.001,15),"strong":(0.005,0.005,30),"extreme":(0.02,0.02,50)}


# ── Tooltip ─────────────────────────────────────────────────
class CTkTooltip:
    _all = []  # global registry for force-hide

    def __init__(self, w, text):
        self.w, self.text, self.tw = w, text, None
        self._after_id = None
        self._poll_id = None
        w.bind("<Enter>", self._enter)
        w.bind("<Leave>", self._hide)
        w.bind("<ButtonPress>", self._hide)
        w.bind("<Destroy>", self._hide)
        CTkTooltip._all.append(self)

    def _enter(self, _=None):
        self._cancel()
        self._after_id = self.w.after(450, self._show)

    def _show(self):
        if self.tw: return
        try:
            if not self.w.winfo_exists() or not self.w.winfo_viewable():
                return
        except Exception:
            return
        x = self.w.winfo_rootx() + 15
        y = self.w.winfo_rooty() + self.w.winfo_height() + 5
        self.tw = tw = ctk.CTkToplevel(self.w)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.configure(fg_color="#1a1a2e")
        tw.attributes("-topmost", True)
        ctk.CTkLabel(tw, text=self.text, font=("Segoe UI", 11), text_color="#a0a0c0",
                     fg_color="#1a1a2e", corner_radius=6, padx=10, pady=6).pack()
        # auto-hide safety + mouse tracking
        self._after_id = self.w.after(6000, self._hide)
        self._poll_id = self.w.after(150, self._poll)

    def _poll(self):
        """Hide if mouse is no longer over the original widget."""
        if not self.tw:
            return
        try:
            import tkinter
            px = self.w.winfo_pointerx()
            py = self.w.winfo_pointery()
            wx1 = self.w.winfo_rootx()
            wy1 = self.w.winfo_rooty()
            wx2 = wx1 + self.w.winfo_width()
            wy2 = wy1 + self.w.winfo_height()
            if not (wx1 <= px <= wx2 and wy1 <= py <= wy2):
                self._hide()
                return
        except Exception:
            self._hide()
            return
        self._poll_id = self.w.after(150, self._poll)

    def _hide(self, _=None):
        self._cancel()
        if self.tw:
            try: self.tw.destroy()
            except Exception: pass
            self.tw = None

    def _cancel(self):
        for attr in ("_after_id", "_poll_id"):
            aid = getattr(self, attr, None)
            if aid:
                try: self.w.after_cancel(aid)
                except Exception: pass
                setattr(self, attr, None)

    def set(self, t):
        self.text = t

    @classmethod
    def hide_all(cls):
        for t in cls._all:
            t._hide()


# ── MAVLink ─────────────────────────────────────────────────
class Conn:
    def __init__(self):
        self.m = None; self.ok = False; self._lk = threading.Lock()
    def connect(self, a):
        self.m = mavutil.mavlink_connection(a); self.m.wait_heartbeat(timeout=5); self.ok = True
    def close(self):
        if self.m: self.m.close()
        self.ok = False; self.m = None
    def sp(self, n, v):
        if not self.ok: raise RuntimeError("Not connected")
        with self._lk: self.m.param_set_send(n, v); time.sleep(0.05)


# ── Colors ──────────────────────────────────────────────────
C_BG = "#0f0f1a"
C_CARD = "#161625"
C_SURF = "#1e1e35"
C_ACC = "#6366f1"
C_ACC2 = "#818cf8"
C_RED = "#ef4444"
C_GRN = "#22c55e"
C_YEL = "#eab308"
C_ORG = "#f97316"
C_TXT = "#e2e8f0"
C_DIM = "#64748b"
C_INP = "#1e293b"


# ── App ─────────────────────────────────────────────────────
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "en"; self.conn = Conn(); self.tips = []
        self._spoof = False; self._complex = False; self._batt_running = False
        self.title("SITL Fault Injection"); self.geometry("780x700")
        self.configure(fg_color=C_BG)
        self._build()
        self._lang_apply()

    def _s(self, k): return L[self.lang].get(k, k)
    def _tip(self, w, k):
        t = CTkTooltip(w, self._s(k)); self.tips.append((t, k))

    def _safe(self, fn):
        if not self.conn.ok: messagebox.showwarning("", self._s("no_conn")); return
        try: fn()
        except Exception as e: messagebox.showerror("Error", str(e))

    # ── Header ──────────────────────────────────────────────
    def _build(self):
        hdr = ctk.CTkFrame(self, fg_color=C_CARD, corner_radius=12, height=56)
        hdr.pack(fill="x", padx=12, pady=(10,6)); hdr.pack_propagate(False)

        self.addr = ctk.CTkEntry(hdr, width=200, height=32, fg_color=C_INP, border_width=0,
                                  placeholder_text="tcp:127.0.0.1:5762", font=("JetBrains Mono",12))
        self.addr.pack(side="left", padx=(12,6), pady=12); self.addr.insert(0, "tcp:127.0.0.1:5762")

        self.conn_btn = ctk.CTkButton(hdr, text="Connect", width=100, height=32, corner_radius=8,
                                       fg_color=C_ACC, hover_color=C_ACC2, font=("Segoe UI",12,"bold"),
                                       command=self._toggle_conn)
        self.conn_btn.pack(side="left", padx=4)

        self.status_dot = ctk.CTkLabel(hdr, text="\u25cf", font=("Segoe UI",16), text_color=C_RED, width=20)
        self.status_dot.pack(side="left", padx=2)
        self.status_lbl = ctk.CTkLabel(hdr, text="Disconnected", font=("Segoe UI",11), text_color=C_DIM)
        self.status_lbl.pack(side="left", padx=2)

        self.lang_btn = ctk.CTkButton(hdr, text="RU", width=40, height=28, corner_radius=6,
                                       fg_color=C_SURF, hover_color=C_INP, font=("Segoe UI",11,"bold"),
                                       text_color=C_DIM, command=self._toggle_lang)
        self.lang_btn.pack(side="right", padx=12)

        # tabs
        self.tabview = ctk.CTkTabview(self, fg_color=C_BG, segmented_button_fg_color=C_CARD,
                                       segmented_button_selected_color=C_ACC,
                                       segmented_button_unselected_color=C_SURF,
                                       corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=12, pady=(0,10))

        self._tab_keys = ["tab_wind","tab_gps","tab_baro","tab_pitot","tab_sensors","tab_complex","tab_system"]
        for k in self._tab_keys:
            self.tabview.add(self._s(k))

        self._build_wind(); self._build_gps(); self._build_baro()
        self._build_pitot(); self._build_sensors(); self._build_complex()
        self._build_system()

        # global safety: hide any lingering tooltips when window loses focus/moves
        self.bind("<FocusOut>", lambda e: CTkTooltip.hide_all())
        self.bind("<Configure>", lambda e: CTkTooltip.hide_all())
        self.bind("<Unmap>", lambda e: CTkTooltip.hide_all())

    def _card(self, parent, **kw):
        return ctk.CTkFrame(parent, fg_color=C_CARD, corner_radius=10, **kw)

    def _slider_row(self, parent, label, var, from_, to, row, tip_key=None):
        lbl = ctk.CTkLabel(parent, text=label, font=("Segoe UI",12), text_color=C_TXT, anchor="w")
        lbl.grid(row=row, column=0, sticky="w", padx=12, pady=6)
        sl = ctk.CTkSlider(parent, from_=from_, to=to, variable=var, width=220,
                           fg_color=C_SURF, progress_color=C_ACC, button_color=C_ACC2, button_hover_color="#a5b4fc")
        sl.grid(row=row, column=1, padx=8, pady=6)
        # editable entry bound to the same var - allows typing exact values
        e = ctk.CTkEntry(parent, textvariable=var, width=70, height=26, fg_color=C_INP,
                         border_width=0, font=("JetBrains Mono",11), justify="center")
        e.grid(row=row, column=2, padx=(0,12), pady=6)
        if tip_key: self._tip(lbl, tip_key); self._tip(sl, tip_key)
        return lbl

    def _entry_row(self, parent, label, var, row, tip_key=None):
        lbl = ctk.CTkLabel(parent, text=label, font=("Segoe UI",12), text_color=C_TXT, anchor="w")
        lbl.grid(row=row, column=0, sticky="w", padx=12, pady=5)
        e = ctk.CTkEntry(parent, textvariable=var, width=100, height=28, fg_color=C_INP,
                         border_width=0, font=("JetBrains Mono",11))
        e.grid(row=row, column=1, sticky="w", padx=8, pady=5)
        if tip_key: self._tip(lbl, tip_key); self._tip(e, tip_key)
        return lbl

    def _btn(self, parent, text, cmd, color=C_ACC, hover=C_ACC2, **kw):
        return ctk.CTkButton(parent, text=text, command=cmd, height=32, corner_radius=8,
                              fg_color=color, hover_color=hover, font=("Segoe UI",12,"bold"), **kw)

    def _tab(self, key):
        return self.tabview.tab(self._s(key))

    # ═══ WIND ═══════════════════════════════════════════════
    def _build_wind(self):
        tab = self._tab("tab_wind")
        c = self._card(tab); c.pack(fill="x", padx=8, pady=8)
        self.wind_spd = ctk.DoubleVar(value=0); self.wind_dir = ctk.DoubleVar(value=180)
        self.wind_turb = ctk.DoubleVar(value=0); self.wind_dir_z = ctk.DoubleVar(value=0)
        self._wl = []
        self._wl.append(self._slider_row(c, "Speed (m/s)", self.wind_spd, 0, 50, 0, "tip_wind_spd"))
        self._wl.append(self._slider_row(c, "Direction (deg)", self.wind_dir, 0, 360, 1, "tip_wind_dir"))
        self._wl.append(self._slider_row(c, "Turbulence (m/s)", self.wind_turb, 0, 20, 2, "tip_wind_turb"))
        self._wl.append(self._slider_row(c, "Vertical (deg)", self.wind_dir_z, -90, 90, 3, "tip_wind_dir_z"))
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.grid(row=4, column=0, columnspan=3, pady=12)
        self.btn_wa = self._btn(bf, "Apply", self._apply_wind); self.btn_wa.pack(side="left", padx=6)
        self.btn_wr = self._btn(bf, "Reset", self._reset_wind, C_SURF, C_INP); self.btn_wr.pack(side="left", padx=6)

    def _apply_wind(self):
        self._safe(lambda: [self.conn.sp("SIM_WIND_SPD",self.wind_spd.get()), self.conn.sp("SIM_WIND_DIR",self.wind_dir.get()),
            self.conn.sp("SIM_WIND_TURB",self.wind_turb.get()), self.conn.sp("SIM_WIND_DIR_Z",self.wind_dir_z.get())])
    def _reset_wind(self):
        self.wind_spd.set(0); self.wind_dir.set(180); self.wind_turb.set(0); self.wind_dir_z.set(0); self._apply_wind()

    # ═══ GPS ════════════════════════════════════════════════
    def _build_gps(self):
        tab = self._tab("tab_gps")
        self.gps_sub = ctk.CTkTabview(tab, fg_color=C_BG, segmented_button_fg_color=C_CARD,
                                       segmented_button_selected_color=C_ACC, segmented_button_unselected_color=C_SURF, height=30)
        self.gps_sub.pack(fill="both", expand=True, padx=4, pady=4)
        self.gps_sub.add(self._s("gps_manual")); self.gps_sub.add(self._s("gps_auto"))
        self._build_gps_manual(); self._build_gps_auto()

    def _build_gps_manual(self):
        p = self.gps_sub.tab(self._s("gps_manual"))
        sc = ctk.CTkScrollableFrame(p, fg_color=C_BG); sc.pack(fill="both", expand=True)
        c = self._card(sc); c.pack(fill="x", padx=4, pady=4)
        self.gps_lat=ctk.DoubleVar(value=0); self.gps_lon=ctk.DoubleVar(value=0); self.gps_alt=ctk.DoubleVar(value=0)
        self.gps_vel_n=ctk.DoubleVar(value=0); self.gps_vel_e=ctk.DoubleVar(value=0); self.gps_vel_d=ctk.DoubleVar(value=0)
        self.gps_alt_ofs=ctk.DoubleVar(value=0); self.gps_alt_drift=ctk.DoubleVar(value=0)
        self.gps_numsats=ctk.IntVar(value=10); self.gps_noise=ctk.DoubleVar(value=0); self.gps_jam=ctk.IntVar(value=0)
        self._gl = []
        entries = [("gps_lat",self.gps_lat,"tip_gps_lat"),("gps_lon",self.gps_lon,"tip_gps_lon"),
                   ("gps_alt",self.gps_alt,"tip_gps_alt"),("gps_vel_n",self.gps_vel_n,"tip_gps_vel_n"),
                   ("gps_vel_e",self.gps_vel_e,"tip_gps_vel_e"),("gps_vel_d",self.gps_vel_d,"tip_gps_vel_d")]
        for i,(k,v,t) in enumerate(entries):
            self._gl.append(self._entry_row(c, self._s(k), v, i, t))
        sliders = [("gps_alt_ofs",self.gps_alt_ofs,-200,200,"tip_gps_alt_ofs"),
                   ("gps_alt_drift",self.gps_alt_drift,-5,5,"tip_gps_alt_drift"),
                   ("gps_numsats",self.gps_numsats,0,20,"tip_gps_numsats"),
                   ("gps_noise",self.gps_noise,0,50,"tip_gps_noise")]
        for i,(k,v,f,t2,tp) in enumerate(sliders):
            self._gl.append(self._slider_row(c, self._s(k), v, f, t2, len(entries)+i, tp))
        r = len(entries)+len(sliders)
        self.chk_jam = ctk.CTkCheckBox(c, text=self._s("gps_jam"), variable=self.gps_jam,
                                        fg_color=C_ACC, hover_color=C_ACC2, font=("Segoe UI",12))
        self.chk_jam.grid(row=r, column=0, columnspan=2, sticky="w", padx=12, pady=6); self._tip(self.chk_jam, "tip_gps_alt"); r+=1
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.grid(row=r, column=0, columnspan=3, pady=10)
        self.btn_ga = self._btn(bf, "Apply", self._apply_gps); self.btn_ga.pack(side="left", padx=6)
        self.btn_gr = self._btn(bf, "Reset", self._reset_gps, C_SURF, C_INP); self.btn_gr.pack(side="left", padx=6)

    def _build_gps_auto(self):
        p = self.gps_sub.tab(self._s("gps_auto"))
        c = self._card(p); c.pack(fill="x", padx=4, pady=4)
        r = 0
        self.spoof_mode = ctk.StringVar(value="hold")
        self._lbl_mode = ctk.CTkLabel(c, text="Mode", font=("Segoe UI",12,"bold"), text_color=C_ACC)
        self._lbl_mode.grid(row=r, column=0, sticky="w", padx=12, pady=6)
        mf = ctk.CTkFrame(c, fg_color="transparent"); mf.grid(row=r, column=1, sticky="w", padx=8, pady=6)
        self._rb_modes = {}
        for v in ["hold","drift","circle"]:
            rb = ctk.CTkRadioButton(mf, text=self._s(v), variable=self.spoof_mode, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",11))
            rb.pack(anchor="w", pady=1); self._rb_modes[v] = rb
        r += 1
        self.intensity = ctk.StringVar(value="medium")
        self._lbl_int = ctk.CTkLabel(c, text="Intensity", font=("Segoe UI",12,"bold"), text_color=C_ACC)
        self._lbl_int.grid(row=r, column=0, sticky="nw", padx=12, pady=6)
        inf = ctk.CTkFrame(c, fg_color="transparent"); inf.grid(row=r, column=1, sticky="w", padx=8, pady=6)
        self._rb_int = {}
        for v in ["weak","medium","strong","extreme"]:
            rb = ctk.CTkRadioButton(inf, text=self._s(v), variable=self.intensity, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",11))
            rb.pack(anchor="w", pady=1); self._rb_int[v] = rb
        r += 1
        self.spoof_speed = ctk.StringVar(value="slow")
        self._lbl_sp = ctk.CTkLabel(c, text="Speed", font=("Segoe UI",12,"bold"), text_color=C_ACC)
        self._lbl_sp.grid(row=r, column=0, sticky="w", padx=12, pady=6)
        sf = ctk.CTkFrame(c, fg_color="transparent"); sf.grid(row=r, column=1, sticky="w", padx=8, pady=6)
        self._rb_sp = {}
        for v in ["slow","fast"]:
            rb = ctk.CTkRadioButton(sf, text=self._s(v), variable=self.spoof_speed, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",11))
            rb.pack(side="left", padx=8); self._rb_sp[v] = rb
        r += 1
        self.spoof_noise = ctk.IntVar(value=1)
        self.chk_sp_noise = ctk.CTkCheckBox(c, text=self._s("add_noise"), variable=self.spoof_noise,
                                             fg_color=C_ACC, font=("Segoe UI",12))
        self.chk_sp_noise.grid(row=r, column=0, columnspan=2, sticky="w", padx=12, pady=6); r += 1
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.grid(row=r, column=0, columnspan=3, pady=10)
        self.btn_sp_start = self._btn(bf, "Start", self._start_spoof); self.btn_sp_start.pack(side="left", padx=6)
        self.btn_sp_stop = self._btn(bf, "Stop", self._stop_spoof, C_RED, "#dc2626"); self.btn_sp_stop.pack(side="left", padx=6)
        r += 1
        self.sp_status = ctk.CTkLabel(c, text="Stopped", font=("Segoe UI",12,"bold"), text_color=C_DIM)
        self.sp_status.grid(row=r, column=0, columnspan=3, pady=6)

    def _apply_gps(self):
        self._safe(lambda: [self.conn.sp("SIM_GPS1_GLTCH_X",self.gps_lat.get()),self.conn.sp("SIM_GPS1_GLTCH_Y",self.gps_lon.get()),
            self.conn.sp("SIM_GPS1_GLTCH_Z",self.gps_alt.get()),self.conn.sp("SIM_GPS1_VERR_X",self.gps_vel_n.get()),
            self.conn.sp("SIM_GPS1_VERR_Y",self.gps_vel_e.get()),self.conn.sp("SIM_GPS1_VERR_Z",self.gps_vel_d.get()),
            self.conn.sp("SIM_GPS1_ALT_OFS",self.gps_alt_ofs.get()),self.conn.sp("SIM_GPS1_DRFTALT",self.gps_alt_drift.get()),
            self.conn.sp("SIM_GPS1_NUMSATS",self.gps_numsats.get()),self.conn.sp("SIM_GPS1_NOISE",self.gps_noise.get()),
            self.conn.sp("SIM_GPS1_JAM",self.gps_jam.get())])
    def _reset_gps(self):
        for v in [self.gps_lat,self.gps_lon,self.gps_alt,self.gps_vel_n,self.gps_vel_e,self.gps_vel_d,
                  self.gps_alt_ofs,self.gps_alt_drift,self.gps_noise]: v.set(0)
        self.gps_numsats.set(10); self.gps_jam.set(0); self._apply_gps()

    def _start_spoof(self):
        if self._spoof: return
        if not self.conn.ok: messagebox.showwarning("",self._s("no_conn")); return
        self._spoof = True; self.sp_status.configure(text=self._s("active"), text_color=C_RED)
        threading.Thread(target=self._spoof_loop, daemon=True).start()
    def _stop_spoof(self):
        self._spoof = False; self.sp_status.configure(text=self._s("stopped"), text_color=C_DIM)
        if self.conn.ok:
            try:
                for p in ["SIM_GPS1_GLTCH_X","SIM_GPS1_GLTCH_Y","SIM_GPS1_GLTCH_Z","SIM_GPS1_VERR_X",
                           "SIM_GPS1_VERR_Y","SIM_GPS1_VERR_Z","SIM_GPS1_NOISE","SIM_GPS1_ALT_OFS","SIM_GPS1_DRFTALT"]:
                    self.conn.sp(p, 0)
                self.conn.sp("SIM_GPS1_NUMSATS", 10)
            except: pass
    def _spoof_loop(self):
        t=0; dl=do=da=0.0
        while self._spoof and self.conn.ok:
            ml,mo,ma = GPS_INT.get(self.intensity.get(), GPS_INT["medium"])
            rate = 0.02 if self.spoof_speed.get()=="slow" else 0.1
            rr = lambda v: random.uniform(-v*0.05,v*0.05)
            m = self.spoof_mode.get()
            if m=="hold": lat,lon,alt = ml+rr(ml), mo+rr(mo), ma+random.uniform(-1,1)
            elif m=="drift":
                dl+=ml*rate*(1+random.uniform(-0.2,0.2)); do+=mo*rate*(1+random.uniform(-0.2,0.2)); da+=ma*rate*0.5
                dl=min(dl,ml*3); do=min(do,mo*3); da=min(da,ma*3); lat,lon,alt=dl,do,da
            elif m=="circle":
                asp=0.05 if self.spoof_speed.get()=="slow" else 0.2; t+=asp
                lat,lon,alt = ml*math.sin(t)+rr(ml), mo*math.cos(t)+rr(mo), ma*0.5*math.sin(t*0.5)
            else: lat=lon=alt=0
            try:
                self.conn.sp("SIM_GPS1_GLTCH_X",lat); self.conn.sp("SIM_GPS1_GLTCH_Y",lon); self.conn.sp("SIM_GPS1_GLTCH_Z",alt)
                self.conn.sp("SIM_GPS1_VERR_X",lat*1000*random.uniform(0.8,1.2))
                self.conn.sp("SIM_GPS1_VERR_Y",lon*1000*random.uniform(0.8,1.2))
                if self.spoof_noise.get(): self.conn.sp("SIM_GPS1_NOISE",5)
            except: self._spoof=False; break
            time.sleep(0.3)

    # ═══ BARO ═══════════════════════════════════════════════
    def _build_baro(self):
        tab = self._tab("tab_baro")
        c = self._card(tab); c.pack(fill="x", padx=8, pady=8)
        self.baro_glitch=ctk.DoubleVar(value=0); self.baro_drift=ctk.DoubleVar(value=0); self.baro_noise=ctk.DoubleVar(value=0.2)
        self.baro_freeze=ctk.IntVar(value=0); self.baro_disable=ctk.IntVar(value=0)
        self._bl = []
        self._bl.append(self._slider_row(c, "Glitch (m)", self.baro_glitch, -200, 200, 0, "tip_baro_glitch"))
        self._bl.append(self._slider_row(c, "Drift (m/s)", self.baro_drift, -5, 5, 1, "tip_baro_drift"))
        self._bl.append(self._slider_row(c, "Noise (m)", self.baro_noise, 0, 20, 2, "tip_baro_noise"))
        self.chk_bf = ctk.CTkCheckBox(c, text="Freeze", variable=self.baro_freeze, fg_color=C_ACC, font=("Segoe UI",12))
        self.chk_bf.grid(row=3, column=0, columnspan=2, sticky="w", padx=12, pady=6); self._tip(self.chk_bf, "tip_baro_freeze")
        self.chk_bd = ctk.CTkCheckBox(c, text="Disable", variable=self.baro_disable, fg_color=C_RED, font=("Segoe UI",12))
        self.chk_bd.grid(row=4, column=0, columnspan=2, sticky="w", padx=12, pady=6); self._tip(self.chk_bd, "tip_baro_disable")
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.grid(row=5, column=0, columnspan=3, pady=12)
        self.btn_ba = self._btn(bf, "Apply", self._apply_baro); self.btn_ba.pack(side="left", padx=6)
        self.btn_br = self._btn(bf, "Reset", self._reset_baro, C_SURF, C_INP); self.btn_br.pack(side="left", padx=6)
        self.baro_st = ctk.CTkLabel(c, text="Normal", font=("Segoe UI",12,"bold"), text_color=C_GRN)
        self.baro_st.grid(row=6, column=0, columnspan=3, pady=4)

    def _apply_baro(self):
        self._safe(lambda: [self.conn.sp("SIM_BARO_GLITCH",self.baro_glitch.get()),self.conn.sp("SIM_BARO_DRIFT",self.baro_drift.get()),
            self.conn.sp("SIM_BARO_RND",self.baro_noise.get()),self.conn.sp("SIM_BARO_FREEZE",self.baro_freeze.get()),
            self.conn.sp("SIM_BARO_DISABLE",self.baro_disable.get())])
        self.baro_st.configure(text="FAULT ACTIVE", text_color=C_RED)
    def _reset_baro(self):
        self.baro_glitch.set(0); self.baro_drift.set(0); self.baro_noise.set(0.2); self.baro_freeze.set(0); self.baro_disable.set(0)
        self._safe(lambda: [self.conn.sp("SIM_BARO_GLITCH",0),self.conn.sp("SIM_BARO_DRIFT",0),
            self.conn.sp("SIM_BARO_RND",0.2),self.conn.sp("SIM_BARO_FREEZE",0),self.conn.sp("SIM_BARO_DISABLE",0)])
        self.baro_st.configure(text="Normal", text_color=C_GRN)

    # ═══ PITOT ══════════════════════════════════════════════
    def _build_pitot(self):
        tab = self._tab("tab_pitot")
        c = self._card(tab); c.pack(fill="x", padx=8, pady=8)
        self.btn_fix = self._btn(c, "Fix ARSPD_TYPE for SITL", self._fix_arspd, C_ORG, C_YEL, width=240)
        self.btn_fix.grid(row=0, column=0, columnspan=3, padx=12, pady=(10,6), sticky="w"); self._tip(self.btn_fix, "tip_pitot_fix")
        self.pitot_mode = ctk.StringVar(value="blocked")
        self._lbl_pm = ctk.CTkLabel(c, text="Mode", font=("Segoe UI",12,"bold"), text_color=C_ACC)
        self._lbl_pm.grid(row=1, column=0, sticky="nw", padx=12, pady=6)
        mf = ctk.CTkFrame(c, fg_color="transparent"); mf.grid(row=1, column=1, sticky="w", padx=8, pady=6)
        self._rb_pitot = {}
        for v, tip in [("blocked","tip_blocked"),("stuck","tip_stuck"),("reversed","tip_reversed"),("noisy","tip_noisy")]:
            rb = ctk.CTkRadioButton(mf, text=self._s(v), variable=self.pitot_mode, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",11))
            rb.pack(anchor="w", pady=1); self._rb_pitot[v] = rb; self._tip(rb, tip)
        self.arspd_fail = ctk.DoubleVar(value=0); self.arspd_noise_v = ctk.DoubleVar(value=2)
        self._pl = []
        self._pl.append(self._slider_row(c, "Stuck speed (m/s)", self.arspd_fail, 0, 80, 2, "tip_stuck"))
        self._pl.append(self._slider_row(c, "Noise (Pa)", self.arspd_noise_v, 0, 200, 3, "tip_noisy"))
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.grid(row=4, column=0, columnspan=3, pady=10)
        self.btn_pa = self._btn(bf, "Activate", self._apply_pitot, C_RED, "#dc2626"); self.btn_pa.pack(side="left", padx=6)
        self.btn_pr = self._btn(bf, "Reset", self._reset_pitot, C_SURF, C_INP); self.btn_pr.pack(side="left", padx=6)
        self.pitot_st = ctk.CTkLabel(c, text="Normal", font=("Segoe UI",12,"bold"), text_color=C_GRN)
        self.pitot_st.grid(row=5, column=0, columnspan=3, pady=4)

    def _fix_arspd(self):
        self._safe(lambda: [self.conn.sp("ARSPD_TYPE",2), self.conn.sp("ARSPD_PIN",1)])
        messagebox.showinfo("Reboot","ARSPD_TYPE=2, PIN=1 set.\nRestart SITL to apply.")
    def _apply_pitot(self):
        m = self.pitot_mode.get()
        def do():
            for p in ["SIM_ARSPD_FAIL","SIM_ARSPD_FAILP","SIM_ARSPD_PITOT","SIM_ARSPD_SIGN"]: self.conn.sp(p,0)
            self.conn.sp("SIM_ARSPD_RND",2); time.sleep(0.1)
            if m=="blocked": self.conn.sp("SIM_ARSPD_FAILP",101325)
            elif m=="stuck": self.conn.sp("SIM_ARSPD_FAIL",max(self.arspd_fail.get(),0.1))
            elif m=="reversed": self.conn.sp("SIM_ARSPD_SIGN",1)
            elif m=="noisy": self.conn.sp("SIM_ARSPD_RND",self.arspd_noise_v.get())
        self._safe(do); self.pitot_st.configure(text="FAILURE ACTIVE", text_color=C_RED)
    def _reset_pitot(self):
        self._safe(lambda: [self.conn.sp(p,0) for p in ["SIM_ARSPD_FAIL","SIM_ARSPD_FAILP","SIM_ARSPD_PITOT","SIM_ARSPD_SIGN"]]+
                   [self.conn.sp("SIM_ARSPD_RND",2)])
        self.pitot_st.configure(text="Normal", text_color=C_GRN)

    # ═══ SENSORS ════════════════════════════════════════════
    def _build_sensors(self):
        tab = self._tab("tab_sensors")
        sc = ctk.CTkScrollableFrame(tab, fg_color=C_BG); sc.pack(fill="both", expand=True)
        # IMU
        c1 = self._card(sc); c1.pack(fill="x", padx=8, pady=4)
        self._lbl_imu = ctk.CTkLabel(c1, text="IMU Failures", font=("Segoe UI",13,"bold"), text_color=C_ACC)
        self._lbl_imu.pack(anchor="w", padx=12, pady=(8,4))
        self.accel_vars = []; self.accel_chks = []
        for i in range(3):
            v = ctk.IntVar(value=0); self.accel_vars.append(v)
            cb = ctk.CTkCheckBox(c1, text=f"Accel {i+1} fail", variable=v, fg_color=C_RED, font=("Segoe UI",12))
            cb.pack(anchor="w", padx=20, pady=2); self.accel_chks.append(cb)
        gf = ctk.CTkFrame(c1, fg_color="transparent"); gf.pack(fill="x", padx=4)
        self.gyro_drift = ctk.DoubleVar(value=0)
        self.vib_x=ctk.DoubleVar(value=0); self.vib_y=ctk.DoubleVar(value=0); self.vib_z=ctk.DoubleVar(value=0)
        self._sl = []
        self._sl.append(self._slider_row(gf, "Gyro drift", self.gyro_drift, 0, 20, 0))
        self._sl.append(self._slider_row(gf, "Vibration X", self.vib_x, 0, 300, 1))
        self._sl.append(self._slider_row(gf, "Vibration Y", self.vib_y, 0, 300, 2))
        self._sl.append(self._slider_row(gf, "Vibration Z", self.vib_z, 0, 300, 3))
        # Compass
        c2 = self._card(sc); c2.pack(fill="x", padx=8, pady=4)
        self._lbl_comp = ctk.CTkLabel(c2, text="Compass Failures", font=("Segoe UI",13,"bold"), text_color=C_ACC)
        self._lbl_comp.pack(anchor="w", padx=12, pady=(8,4))
        self.mag_vars = []; self.mag_chks = []
        for i in range(3):
            v = ctk.IntVar(value=0); self.mag_vars.append(v)
            cb = ctk.CTkCheckBox(c2, text=f"Compass {i+1} fail", variable=v, fg_color=C_RED, font=("Segoe UI",12))
            cb.pack(anchor="w", padx=20, pady=2); self.mag_chks.append(cb)
        bf = ctk.CTkFrame(sc, fg_color="transparent"); bf.pack(pady=8)
        self.btn_sa = self._btn(bf, "Apply", self._apply_sensors); self.btn_sa.pack(side="left", padx=6)
        self.btn_sr = self._btn(bf, "Reset", self._reset_sensors, C_SURF, C_INP); self.btn_sr.pack(side="left", padx=6)

    def _apply_sensors(self):
        def do():
            for i,v in enumerate(self.accel_vars): self.conn.sp(f"SIM_ACCEL{i+1}_FAIL",v.get())
            for i,v in enumerate(self.mag_vars): self.conn.sp(f"SIM_MAG{i+1}_FAIL",v.get())
            self.conn.sp("SIM_DRIFT_SPEED",self.gyro_drift.get())
            self.conn.sp("SIM_VIB_FREQ_X",self.vib_x.get()); self.conn.sp("SIM_VIB_FREQ_Y",self.vib_y.get()); self.conn.sp("SIM_VIB_FREQ_Z",self.vib_z.get())
        self._safe(do)
    def _reset_sensors(self):
        for v in self.accel_vars+self.mag_vars: v.set(0)
        self.gyro_drift.set(0); self.vib_x.set(0); self.vib_y.set(0); self.vib_z.set(0); self._apply_sensors()

    # ═══ COMPLEX ════════════════════════════════════════════
    def _build_complex(self):
        tab = self._tab("tab_complex")
        c = self._card(tab); c.pack(fill="x", padx=8, pady=8)
        self._lbl_cx = ctk.CTkLabel(c, text="Attack Scenarios", font=("Segoe UI",14,"bold"), text_color=C_ACC)
        self._lbl_cx.pack(anchor="w", padx=12, pady=(10,6))
        self.cx_var = ctk.StringVar(value="gps_denied")
        self._rb_cx = {}
        for v, tip in [("gps_denied","tip_gps_denied"),("sensor_deg","tip_sensor_deg"),
                        ("full_spoof","tip_full_spoof"),("icing","tip_icing")]:
            rb = ctk.CTkRadioButton(c, text=self._s(v), variable=self.cx_var, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",12))
            rb.pack(anchor="w", padx=20, pady=3); self._rb_cx[v] = rb; self._tip(rb, tip)
        bf = ctk.CTkFrame(c, fg_color="transparent"); bf.pack(pady=12)
        self.btn_cxs = self._btn(bf, "Start Scenario", self._start_complex); self.btn_cxs.pack(side="left", padx=6)
        self.btn_cxr = self._btn(bf, "Stop All", self._stop_complex, C_RED, "#dc2626"); self.btn_cxr.pack(side="left", padx=6)
        self.cx_status = ctk.CTkLabel(c, text="Stopped", font=("Segoe UI",13,"bold"), text_color=C_DIM)
        self.cx_status.pack(pady=6)

    def _start_complex(self):
        if self._complex: return
        if not self.conn.ok: messagebox.showwarning("",self._s("no_conn")); return
        self._complex = True; self.cx_status.configure(text=self._s("active"), text_color=C_RED)
        threading.Thread(target=self._complex_loop, daemon=True).start()

    def _stop_complex(self):
        self._complex = False; self.cx_status.configure(text=self._s("stopped"), text_color=C_DIM)
        if not self.conn.ok: return
        try:
            for p in ["SIM_GPS1_GLTCH_X","SIM_GPS1_GLTCH_Y","SIM_GPS1_GLTCH_Z","SIM_GPS1_VERR_X","SIM_GPS1_VERR_Y",
                       "SIM_GPS1_VERR_Z","SIM_GPS1_JAM","SIM_GPS1_NOISE","SIM_GPS1_ALT_OFS","SIM_GPS1_DRFTALT",
                       "SIM_BARO_GLITCH","SIM_BARO_DRIFT","SIM_BARO_FREEZE","SIM_ARSPD_FAIL","SIM_ARSPD_FAILP",
                       "SIM_ARSPD_PITOT","SIM_ARSPD_SIGN","SIM_DRIFT_SPEED","SIM_VIB_FREQ_X","SIM_VIB_FREQ_Y","SIM_VIB_FREQ_Z"]:
                self.conn.sp(p,0)
            self.conn.sp("SIM_GPS1_NUMSATS",10); self.conn.sp("SIM_BARO_RND",0.2); self.conn.sp("SIM_ARSPD_RND",2)
            self.conn.sp("SIM_BARO_DISABLE",0)
        except: pass

    def _complex_loop(self):
        sc = self.cx_var.get(); t = 0
        while self._complex and self.conn.ok:
            t += 1
            try:
                if sc == "gps_denied":
                    self.conn.sp("SIM_GPS1_JAM", 1 if t>10 else 0)
                    self.conn.sp("SIM_GPS1_NUMSATS", max(0,int(10-t*0.5)))
                    self.conn.sp("SIM_GPS1_NOISE", min(t*2,50))
                    self.conn.sp("SIM_BARO_DRIFT", min(t*0.03,1.0))
                    self.conn.sp("SIM_BARO_RND", 0.2+t*0.1)
                elif sc == "sensor_deg":
                    self.conn.sp("SIM_GPS1_NOISE", min(t*0.5,30))
                    self.conn.sp("SIM_BARO_RND", 0.2+t*0.05)
                    self.conn.sp("SIM_BARO_DRIFT", min(t*0.02,1.0))
                    self.conn.sp("SIM_ARSPD_RND", 2+t*0.5)
                    self.conn.sp("SIM_DRIFT_SPEED", min(t*0.1,5))
                    self.conn.sp("SIM_VIB_FREQ_X", min(t*2,100)); self.conn.sp("SIM_VIB_FREQ_Y", min(t*2,100))
                    self.conn.sp("SIM_VIB_FREQ_Z", min(t*3,150))
                elif sc == "full_spoof":
                    d = min(t*0.00005,0.005)
                    self.conn.sp("SIM_GPS1_GLTCH_X", d+random.uniform(-d*0.05,d*0.05))
                    self.conn.sp("SIM_GPS1_GLTCH_Y", d*1.2+random.uniform(-d*0.05,d*0.05))
                    self.conn.sp("SIM_GPS1_GLTCH_Z", min(t*0.2,30))
                    self.conn.sp("SIM_GPS1_VERR_X", min(t*0.1,5)*random.uniform(0.8,1.2))
                    self.conn.sp("SIM_GPS1_VERR_Y", min(t*0.1,5)*random.uniform(0.8,1.2))
                    self.conn.sp("SIM_GPS1_ALT_OFS", min(t*0.5,50))
                    self.conn.sp("SIM_BARO_GLITCH", min(t*0.3,20)); self.conn.sp("SIM_GPS1_NOISE",3)
                elif sc == "icing":
                    ice = min(t*0.01,1.0)
                    if ice>0.5: self.conn.sp("SIM_ARSPD_FAILP",101325*ice)
                    self.conn.sp("SIM_ARSPD_RND",2+t*1.5)
                    self.conn.sp("SIM_BARO_GLITCH",-min(t*0.1,5))
                    self.conn.sp("SIM_VIB_FREQ_X",min(t*3,120)); self.conn.sp("SIM_VIB_FREQ_Z",min(t*4,180))
            except: self._complex=False; break
            time.sleep(0.5)

    # ═══ SYSTEM (sim speed + battery) ═══════════════════════
    def _build_system(self):
        tab = self._tab("tab_system")
        sc = ctk.CTkScrollableFrame(tab, fg_color=C_BG)
        sc.pack(fill="both", expand=True)

        # ── Simulation Speed ──
        c1 = self._card(sc); c1.pack(fill="x", padx=8, pady=6)
        self._lbl_sys_speed = ctk.CTkLabel(c1, text="Simulation Speed",
                                            font=("Segoe UI",13,"bold"), text_color=C_ACC)
        self._lbl_sys_speed.grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(10,4))

        self.sim_speedup = ctk.DoubleVar(value=1.0)
        self._sys_sl = []
        self._sys_sl.append(self._slider_row(c1, "Speed multiplier", self.sim_speedup, 0.1, 20, 1))

        # preset buttons
        pf = ctk.CTkFrame(c1, fg_color="transparent")
        pf.grid(row=2, column=0, columnspan=3, padx=12, pady=(2,8), sticky="w")
        self._lbl_presets = ctk.CTkLabel(pf, text="Presets", font=("Segoe UI",11), text_color=C_DIM)
        self._lbl_presets.pack(side="left", padx=(0,8))
        for mult in (0.5, 1, 2, 5, 10):
            b = ctk.CTkButton(pf, text=f"{mult}x", width=44, height=26, corner_radius=6,
                               fg_color=C_SURF, hover_color=C_INP, font=("JetBrains Mono",11),
                               command=lambda m=mult: self._set_speedup(m))
            b.pack(side="left", padx=3)

        self.btn_speed_apply = self._btn(c1, "Apply", self._apply_speedup)
        self.btn_speed_apply.grid(row=3, column=0, columnspan=3, pady=(4,10))

        # ── Battery Simulation ──
        c2 = self._card(sc); c2.pack(fill="x", padx=8, pady=6)
        self._lbl_sys_batt = ctk.CTkLabel(c2, text="Battery Simulation",
                                           font=("Segoe UI",13,"bold"), text_color=C_ACC)
        self._lbl_sys_batt.grid(row=0, column=0, columnspan=3, sticky="w", padx=12, pady=(10,4))

        self.batt_start_v = ctk.DoubleVar(value=12.6)
        self.batt_end_v = ctk.DoubleVar(value=10.5)
        self.batt_time_min = ctk.DoubleVar(value=15.0)
        self.batt_cap_ah = ctk.DoubleVar(value=5.0)

        self._batt_lbls = []
        self._batt_lbls.append(self._slider_row(c2, "Start voltage (V)", self.batt_start_v, 8.0, 25.2, 1))
        self._batt_lbls.append(self._slider_row(c2, "End voltage (V)", self.batt_end_v, 6.0, 20.0, 2))
        self._batt_lbls.append(self._slider_row(c2, "Discharge time (min)", self.batt_time_min, 0.5, 120, 3))
        self._batt_lbls.append(self._slider_row(c2, "Capacity (Ah)", self.batt_cap_ah, 0.5, 50, 4))

        # curve selector
        self.batt_curve = ctk.StringVar(value="lipo")
        cf = ctk.CTkFrame(c2, fg_color="transparent")
        cf.grid(row=5, column=0, columnspan=3, padx=12, pady=6, sticky="w")
        self._lbl_curve = ctk.CTkLabel(cf, text="Curve", font=("Segoe UI",11), text_color=C_DIM)
        self._lbl_curve.pack(side="left", padx=(0,10))
        self._rb_curve = {}
        for v in ("lipo", "linear"):
            rb = ctk.CTkRadioButton(cf, text=v, variable=self.batt_curve, value=v,
                                     fg_color=C_ACC, font=("Segoe UI",11))
            rb.pack(side="left", padx=6); self._rb_curve[v] = rb

        # current voltage display
        self._lbl_batt_now = ctk.CTkLabel(c2, text="Current: —",
                                           font=("JetBrains Mono",14,"bold"), text_color=C_GRN)
        self._lbl_batt_now.grid(row=6, column=0, columnspan=3, pady=(4,2))

        bf = ctk.CTkFrame(c2, fg_color="transparent")
        bf.grid(row=7, column=0, columnspan=3, pady=(4,12))
        self.btn_batt_start = self._btn(bf, "Start Discharge", self._start_batt)
        self.btn_batt_start.pack(side="left", padx=4)
        self.btn_batt_stop = self._btn(bf, "Stop", self._stop_batt, C_RED, "#dc2626")
        self.btn_batt_stop.pack(side="left", padx=4)
        self.btn_batt_reset = self._btn(bf, "Reset", self._reset_batt, C_SURF, C_INP)
        self.btn_batt_reset.pack(side="left", padx=4)

    def _set_speedup(self, m):
        self.sim_speedup.set(m)
        self._apply_speedup()

    def _apply_speedup(self):
        self._safe(lambda: self.conn.sp("SIM_SPEEDUP", self.sim_speedup.get()))

    def _start_batt(self):
        if self._batt_running: return
        if not self.conn.ok:
            messagebox.showwarning("", self._s("no_conn")); return
        try:
            v_start = float(self.batt_start_v.get())
            v_end = float(self.batt_end_v.get())
            t_min = float(self.batt_time_min.get())
            cap = float(self.batt_cap_ah.get())
        except Exception:
            return
        if t_min <= 0 or v_start <= v_end:
            messagebox.showerror("Error", "Time must be > 0 and start > end voltage.")
            return
        self._batt_running = True
        self._lbl_batt_now.configure(text_color=C_RED)
        # set initial voltage and capacity once
        try:
            self.conn.sp("SIM_BATT_CAP_AH", cap)
            self.conn.sp("SIM_BATT_VOLTAGE", v_start)
        except Exception as e:
            messagebox.showerror("Error", str(e)); self._batt_running = False; return
        threading.Thread(target=self._batt_loop, args=(v_start, v_end, t_min), daemon=True).start()

    def _stop_batt(self):
        self._batt_running = False
        self._lbl_batt_now.configure(text_color=C_GRN)

    def _reset_batt(self):
        self._stop_batt()
        self._safe(lambda: self.conn.sp("SIM_BATT_VOLTAGE", 12.6))
        self._lbl_batt_now.configure(text="Current: 12.60 V", text_color=C_GRN)

    def _batt_loop(self, v_start, v_end, t_min):
        """Continuously update SIM_BATT_VOLTAGE so it drops from v_start to v_end over t_min real minutes.
        Uses a simple LiPo-like curve (3 phases) or linear depending on selection."""
        t_total = t_min * 60.0
        t0 = time.time()
        tick = 0.5  # seconds
        while self._batt_running and self.conn.ok:
            elapsed = time.time() - t0
            frac = min(elapsed / t_total, 1.0)
            if self.batt_curve.get() == "linear":
                v = v_start - (v_start - v_end) * frac
            else:
                # LiPo-like: fast initial drop, long plateau, sharp end drop
                # three-segment: 0-10% drops 25%, 10-85% drops 40%, 85-100% drops 35%
                if frac < 0.10:
                    p = frac / 0.10
                    v = v_start - (v_start - v_end) * 0.25 * p
                elif frac < 0.85:
                    p = (frac - 0.10) / 0.75
                    v = v_start - (v_start - v_end) * (0.25 + 0.40 * p)
                else:
                    p = (frac - 0.85) / 0.15
                    v = v_start - (v_start - v_end) * (0.65 + 0.35 * p)
            try:
                self.conn.sp("SIM_BATT_VOLTAGE", v)
                self.after(0, lambda vv=v: self._lbl_batt_now.configure(text=f"Current: {vv:.2f} V"))
            except Exception:
                self._batt_running = False; break
            if frac >= 1.0:
                self._batt_running = False
                self.after(0, lambda: self._lbl_batt_now.configure(text_color=C_RED))
                break
            time.sleep(tick)

    # ── Connection ──────────────────────────────────────────
    def _toggle_conn(self):
        if self.conn.ok:
            self._stop_spoof(); self._stop_complex(); self.conn.close()
            self.status_dot.configure(text_color=C_RED); self.status_lbl.configure(text=self._s("disconnected"))
            self.conn_btn.configure(text=self._s("connect"))
        else:
            a = self.addr.get().strip()
            self.status_lbl.configure(text=self._s("connecting")); self.status_dot.configure(text_color=C_YEL)
            threading.Thread(target=self._do_conn, args=(a,), daemon=True).start()
    def _do_conn(self, a):
        try:
            self.conn.connect(a)
            self.after(0, lambda: [self.status_dot.configure(text_color=C_GRN),
                self.status_lbl.configure(text=self._s("connected")), self.conn_btn.configure(text=self._s("disconnect"))])
        except Exception as e:
            self.after(0, lambda: [self.status_dot.configure(text_color=C_RED),
                self.status_lbl.configure(text=self._s("failed")), messagebox.showerror("Error",str(e))])

    # ── Language ────────────────────────────────────────────
    def _toggle_lang(self):
        self.lang = "ru" if self.lang=="en" else "en"; self._lang_apply()

    def _lang_apply(self):
        s = L[self.lang]; self.title(s["title"]); self.lang_btn.configure(text=s["lang"])
        if self.conn.ok: self.status_lbl.configure(text=s["connected"]); self.conn_btn.configure(text=s["disconnect"])
        else: self.status_lbl.configure(text=s["disconnected"]); self.conn_btn.configure(text=s["connect"])
        # tabs - rename by recreating names
        for i, k in enumerate(self._tab_keys):
            try: self.tabview.rename(self.tabview._tab_dict[list(self.tabview._tab_dict.keys())[i]], s[k])
            except: pass
        # wind
        wk = ["wind_spd","wind_dir","wind_turb","wind_dir_z"]
        for lbl, k in zip(self._wl, wk): lbl.configure(text=s[k])
        self.btn_wa.configure(text=s["apply"]); self.btn_wr.configure(text=s["reset"])
        # gps
        gk = ["gps_lat","gps_lon","gps_alt","gps_vel_n","gps_vel_e","gps_vel_d","gps_alt_ofs","gps_alt_drift","gps_numsats","gps_noise"]
        for lbl,k in zip(self._gl, gk): lbl.configure(text=s[k])
        self.chk_jam.configure(text=s["gps_jam"])
        self.btn_ga.configure(text=s["apply"]); self.btn_gr.configure(text=s["reset"])
        self._lbl_mode.configure(text=s["mode"]); self._lbl_int.configure(text=s["intensity"]); self._lbl_sp.configure(text=s["speed"])
        for v in ["hold","drift","circle"]: self._rb_modes[v].configure(text=s[v])
        for v in ["weak","medium","strong","extreme"]: self._rb_int[v].configure(text=s[v])
        for v in ["slow","fast"]: self._rb_sp[v].configure(text=s[v])
        self.chk_sp_noise.configure(text=s["add_noise"])
        self.btn_sp_start.configure(text=s["start"]); self.btn_sp_stop.configure(text=s["stop"])
        self.sp_status.configure(text=s["active"] if self._spoof else s["stopped"])
        # baro
        bk = ["baro_glitch","baro_drift","baro_noise"]
        for lbl,k in zip(self._bl, bk): lbl.configure(text=s[k])
        self.chk_bf.configure(text=s["baro_freeze"]); self.chk_bd.configure(text=s["baro_disable"])
        self.btn_ba.configure(text=s["apply"]); self.btn_br.configure(text=s["reset"])
        # pitot
        self.btn_fix.configure(text=s["pitot_fix"]); self._lbl_pm.configure(text=s["pitot_mode"])
        for v in ["blocked","stuck","reversed","noisy"]: self._rb_pitot[v].configure(text=s[v])
        self._pl[0].configure(text=s["stuck_val"]); self._pl[1].configure(text=s["noise_pa"])
        self.btn_pa.configure(text=s["activate"]); self.btn_pr.configure(text=s["reset"])
        # sensors
        self._lbl_imu.configure(text=s["imu"]); self._lbl_comp.configure(text=s["compass"])
        for i,c in enumerate(self.accel_chks): c.configure(text=f"{s['accel']} {i+1}")
        for i,c in enumerate(self.mag_chks): c.configure(text=f"{s['mag']} {i+1}")
        sk = ["gyro_drift","vib_x","vib_y","vib_z"]
        for lbl,k in zip(self._sl, sk): lbl.configure(text=s[k])
        self.btn_sa.configure(text=s["apply"]); self.btn_sr.configure(text=s["reset"])
        # complex
        self._lbl_cx.configure(text=s["scenarios"])
        for v in ["gps_denied","sensor_deg","full_spoof","icing"]: self._rb_cx[v].configure(text=s[v])
        self.btn_cxs.configure(text=s["start"]); self.btn_cxr.configure(text=s["stop"])
        self.cx_status.configure(text=s["active"] if self._complex else s["stopped"])
        # system
        self._lbl_sys_speed.configure(text=s["sys_sim_speed"])
        self._sys_sl[0].configure(text=s["sys_speedup"])
        self._lbl_presets.configure(text=s["sys_speed_presets"])
        self.btn_speed_apply.configure(text=s["apply"])
        self._lbl_sys_batt.configure(text=s["sys_batt"])
        bk = ["sys_batt_start_v","sys_batt_end_v","sys_batt_time","sys_batt_cap"]
        for lbl, k in zip(self._batt_lbls, bk): lbl.configure(text=s[k])
        self._lbl_curve.configure(text=s["sys_batt_curve"])
        self._rb_curve["lipo"].configure(text=s["sys_batt_lipo"])
        self._rb_curve["linear"].configure(text=s["sys_batt_linear"])
        self.btn_batt_start.configure(text=s["sys_batt_start"])
        self.btn_batt_stop.configure(text=s["sys_batt_stop"])
        self.btn_batt_reset.configure(text=s["sys_batt_reset"])
        # tooltips
        for tip,k in self.tips: tip.set(s.get(k,k))


if __name__ == "__main__":
    App().mainloop()

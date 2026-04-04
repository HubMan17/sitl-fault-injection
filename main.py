import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from pymavlink import mavutil


class SITLConnection:
    def __init__(self):
        self.master = None
        self.connected = False

    def connect(self, address="tcp:127.0.0.1:5760"):
        try:
            self.master = mavutil.mavlink_connection(address)
            self.master.wait_heartbeat(timeout=5)
            self.connected = True
            return True
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
            raise RuntimeError("Not connected to SITL")
        self.master.param_set_send(name, value)
        # wait for ACK
        time.sleep(0.1)

    def get_param(self, name):
        if not self.connected:
            raise RuntimeError("Not connected to SITL")
        self.master.param_fetch_one(name)
        msg = self.master.recv_match(type="PARAM_VALUE", blocking=True, timeout=3)
        if msg and msg.param_id.replace('\x00', '') == name:
            return msg.param_value
        return None


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SITL Fault Injection")
        self.geometry("620x520")
        self.resizable(False, False)

        self.conn = SITLConnection()

        self._build_connection_frame()
        self._build_notebook()

    # ── Connection ──────────────────────────────────────────────
    def _build_connection_frame(self):
        fr = ttk.LabelFrame(self, text="Connection")
        fr.pack(fill="x", padx=8, pady=(8, 4))

        ttk.Label(fr, text="Address:").grid(row=0, column=0, padx=4, pady=4)
        self.addr_var = tk.StringVar(value="tcp:127.0.0.1:5760")
        ttk.Entry(fr, textvariable=self.addr_var, width=30).grid(row=0, column=1, padx=4)

        self.conn_btn = ttk.Button(fr, text="Connect", command=self._toggle_connection)
        self.conn_btn.grid(row=0, column=2, padx=8, pady=4)

        self.status_var = tk.StringVar(value="Disconnected")
        ttk.Label(fr, textvariable=self.status_var, foreground="red").grid(row=0, column=3, padx=4)

    def _toggle_connection(self):
        if self.conn.connected:
            self.conn.disconnect()
            self.status_var.set("Disconnected")
            self.conn_btn.config(text="Connect")
        else:
            addr = self.addr_var.get().strip()
            self.status_var.set("Connecting...")
            self.update_idletasks()
            threading.Thread(target=self._do_connect, args=(addr,), daemon=True).start()

    def _do_connect(self, addr):
        try:
            self.conn.connect(addr)
            self.after(0, lambda: self.status_var.set("Connected"))
            self.after(0, lambda: self.conn_btn.config(text="Disconnect"))
        except Exception as e:
            self.after(0, lambda: self.status_var.set("Failed"))
            self.after(0, lambda: messagebox.showerror("Connection error", str(e)))

    # ── Notebook with tabs ──────────────────────────────────────
    def _build_notebook(self):
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=8)

        nb.add(self._build_wind_tab(nb), text="Wind")
        nb.add(self._build_gps_tab(nb), text="GPS Spoofing")
        nb.add(self._build_pitot_tab(nb), text="Pitot Failure")

    # ── Wind ────────────────────────────────────────────────────
    def _build_wind_tab(self, parent):
        fr = ttk.Frame(parent, padding=12)

        row = 0
        ttk.Label(fr, text="Wind speed (m/s):").grid(row=row, column=0, sticky="w", pady=4)
        self.wind_spd = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.wind_spd, from_=0, to=50, orient="horizontal",
                 length=300, resolution=0.5).grid(row=row, column=1, pady=4)

        row += 1
        ttk.Label(fr, text="Wind direction (deg):").grid(row=row, column=0, sticky="w", pady=4)
        self.wind_dir = tk.DoubleVar(value=180)
        tk.Scale(fr, variable=self.wind_dir, from_=0, to=360, orient="horizontal",
                 length=300, resolution=1).grid(row=row, column=1, pady=4)

        row += 1
        ttk.Label(fr, text="Turbulence (m/s):").grid(row=row, column=0, sticky="w", pady=4)
        self.wind_turb = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.wind_turb, from_=0, to=20, orient="horizontal",
                 length=300, resolution=0.5).grid(row=row, column=1, pady=4)

        row += 1
        ttk.Label(fr, text="Vertical angle (deg):").grid(row=row, column=0, sticky="w", pady=4)
        self.wind_dir_z = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.wind_dir_z, from_=-90, to=90, orient="horizontal",
                 length=300, resolution=1).grid(row=row, column=1, pady=4)

        row += 1
        ttk.Button(fr, text="Apply Wind", command=self._apply_wind).grid(
            row=row, column=0, columnspan=2, pady=12)

        row += 1
        ttk.Button(fr, text="Reset Wind", command=self._reset_wind).grid(
            row=row, column=0, columnspan=2)

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

    # ── GPS Spoofing ────────────────────────────────────────────
    def _build_gps_tab(self, parent):
        fr = ttk.Frame(parent, padding=12)

        row = 0
        ttk.Label(fr, text="Latitude offset (deg):").grid(row=row, column=0, sticky="w", pady=4)
        self.gps_lat = tk.DoubleVar(value=0)
        e1 = ttk.Entry(fr, textvariable=self.gps_lat, width=15)
        e1.grid(row=row, column=1, pady=4, sticky="w")

        row += 1
        ttk.Label(fr, text="Longitude offset (deg):").grid(row=row, column=0, sticky="w", pady=4)
        self.gps_lon = tk.DoubleVar(value=0)
        ttk.Entry(fr, textvariable=self.gps_lon, width=15).grid(row=row, column=1, pady=4, sticky="w")

        row += 1
        ttk.Label(fr, text="Altitude offset (m):").grid(row=row, column=0, sticky="w", pady=4)
        self.gps_alt = tk.DoubleVar(value=0)
        ttk.Entry(fr, textvariable=self.gps_alt, width=15).grid(row=row, column=1, pady=4, sticky="w")

        row += 1
        self.gps_jam_var = tk.IntVar(value=0)
        ttk.Checkbutton(fr, text="Enable GPS jamming", variable=self.gps_jam_var).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=4)

        row += 1
        ttk.Label(fr, text="GPS noise amplitude (m):").grid(row=row, column=0, sticky="w", pady=4)
        self.gps_noise = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.gps_noise, from_=0, to=100, orient="horizontal",
                 length=300, resolution=1).grid(row=row, column=1, pady=4)

        row += 1
        ttk.Button(fr, text="Apply GPS Spoofing", command=self._apply_gps).grid(
            row=row, column=0, columnspan=2, pady=12)

        row += 1
        ttk.Button(fr, text="Reset GPS", command=self._reset_gps).grid(
            row=row, column=0, columnspan=2)

        return fr

    def _apply_gps(self):
        # SIM_GPS1_GLTCH is a Vector3f — set each axis via indexed param name
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

    # ── Pitot / Airspeed failure ────────────────────────────────
    def _build_pitot_tab(self, parent):
        fr = ttk.Frame(parent, padding=12)

        row = 0
        ttk.Label(fr, text="Airspeed fail value (m/s):").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Label(fr, text="0 = normal, >0 = stuck at this value").grid(
            row=row, column=1, sticky="w", padx=(0, 0))

        row += 1
        self.arspd_fail = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.arspd_fail, from_=0, to=80, orient="horizontal",
                 length=300, resolution=0.5).grid(row=row, column=0, columnspan=2, pady=4, sticky="w")

        row += 1
        ttk.Label(fr, text="Pitot failure pressure (Pa):").grid(row=row, column=0, sticky="w", pady=4)
        ttk.Label(fr, text="0 = normal").grid(row=row, column=1, sticky="w")

        row += 1
        self.arspd_failp = tk.DoubleVar(value=0)
        tk.Scale(fr, variable=self.arspd_failp, from_=0, to=500, orient="horizontal",
                 length=300, resolution=1).grid(row=row, column=0, columnspan=2, pady=4, sticky="w")

        row += 1
        self.arspd_sign_var = tk.IntVar(value=0)
        ttk.Checkbutton(fr, text="Reverse pitot/static connections",
                        variable=self.arspd_sign_var).grid(
            row=row, column=0, columnspan=2, sticky="w", pady=8)

        row += 1
        ttk.Button(fr, text="Apply Pitot Failure", command=self._apply_pitot).grid(
            row=row, column=0, columnspan=2, pady=12)

        row += 1
        ttk.Button(fr, text="Reset Pitot", command=self._reset_pitot).grid(
            row=row, column=0, columnspan=2)

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

    # ── Helper ──────────────────────────────────────────────────
    def _run_safe(self, fn):
        if not self.conn.connected:
            messagebox.showwarning("Not connected", "Connect to SITL first.")
            return
        try:
            fn()
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = App()
    app.mainloop()

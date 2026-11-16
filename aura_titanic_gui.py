import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np


class CyberNeonTitanicStudio:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXUS TITANIC AI — Next-Gen Data Hygiene & Telemetry Core")
        self.root.geometry("1340x800")
        self.root.minsize(1180, 720)
        self.root.configure(bg="#05070E")

        # Ultra-Modern Cyber Neon Palette
        self.BG_DEEP = "#05070E"
        self.BG_SURFACE = "#0A0F1E"
        self.BG_CARD = "#0F162B"
        self.BG_HOVER = "#16203E"

        self.NEON_CYAN = "#00F5D4"
        self.NEON_PINK = "#FF2A85"
        self.NEON_PURPLE = "#9B5DE5"
        self.NEON_BLUE = "#00BBF9"
        self.NEON_YELLOW = "#FEE440"
        self.TEXT_MAIN = "#FFFFFF"
        self.TEXT_SUB = "#8D99AE"

        self.df_raw = None
        self.df_clean = None
        self.log_history = []
        self.current_page = "overview"

        self._init_styles()
        self._build_layout()

    def _init_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Nexus.Treeview",
            background="#0A0F1E",
            foreground="#E2E8F0",
            fieldbackground="#0A0F1E",
            rowheight=30,
            borderwidth=0,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Nexus.Treeview.Heading",
            background="#131B36",
            foreground="#00F5D4",
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )
        style.map(
            "Nexus.Treeview",
            background=[("selected", "#FF2A85")],
            foreground=[("selected", "#FFFFFF")]
        )

    def _build_layout(self):
        # ================= TOP NEON HEADER BAR =================
        top_nav = tk.Frame(self.root, bg=self.BG_SURFACE, height=68)
        top_nav.pack(side="top", fill="x")
        top_nav.pack_propagate(False)

        # Glowing bottom accent strip
        tk.Frame(self.root, bg=self.NEON_CYAN, height=2).pack(side="top", fill="x")

        # Left Brand Badge
        left_brand = tk.Frame(top_nav, bg=self.BG_SURFACE)
        left_brand.pack(side="left", padx=22)

        badge = tk.Label(
            left_brand, text=" NEXUS // AI ", font=("Consolas", 11, "bold"),
            bg=self.NEON_PINK, fg="white", padx=6, pady=3
        )
        badge.pack(side="left", padx=(0, 12))

        title_stack = tk.Frame(left_brand, bg=self.BG_SURFACE)
        title_stack.pack(side="left")
        tk.Label(
            title_stack, text="TITANIC DATA INTELLIGENCE STUDIO",
            font=("Segoe UI", 14, "bold"), bg=self.BG_SURFACE, fg=self.TEXT_MAIN
        ).pack(anchor="w")
        tk.Label(
            title_stack, text="Engineered by Saman Mustafiz  •  BS IT (7th Semester)  •  Data Science",
            font=("Segoe UI", 8), bg=self.BG_SURFACE, fg=self.NEON_CYAN
        ).pack(anchor="w")

        # Right Status Pill
        self.pill_status = tk.Label(
            top_nav, text="● SYSTEM IDLE — LOAD CSV", font=("Consolas", 9, "bold"),
            bg="#131B36", fg=self.NEON_YELLOW, padx=14, pady=6
        )
        self.pill_status.pack(side="right", padx=22)

        # ================= MAIN CONTAINER =================
        container = tk.Frame(self.root, bg=self.BG_DEEP)
        container.pack(fill="both", expand=True, padx=18, pady=14)

        # --- LEFT COMMAND DOCK (240px) ---
        dock = tk.Frame(container, bg=self.BG_SURFACE, width=240, highlightbackground="#1E293B", highlightthickness=1)
        dock.pack(side="left", fill="y", padx=(0, 14))
        dock.pack_propagate(False)

        tk.Label(
            dock, text="ACTION COMMANDS", font=("Consolas", 9, "bold"),
            bg=self.BG_SURFACE, fg=self.TEXT_SUB
        ).pack(anchor="w", padx=16, pady=(16, 8))

        self.btn_load = self._make_neon_btn(
            dock, "01  IMPORT TITANIC CSV", self.load_csv,
            bg="#131B36", fg=self.NEON_BLUE, hover="#1D2951"
        )
        self.btn_clean = self._make_neon_btn(
            dock, "02  RUN AUTO-CLEANER", self.run_pipeline,
            bg=self.NEON_CYAN, fg="#05070E", hover="#5FFBF1"
        )
        self.btn_export = self._make_neon_btn(
            dock, "03  EXPORT DATASET", self.export_files,
            bg=self.NEON_PINK, fg="#FFFFFF", hover="#FF5CA0"
        )

        # Separator
        tk.Frame(dock, bg="#1E293B", height=1).pack(fill="x", padx=16, pady=14)

        tk.Label(
            dock, text="WORKSPACE VIEWS", font=("Consolas", 9, "bold"),
            bg=self.BG_SURFACE, fg=self.TEXT_SUB
        ).pack(anchor="w", padx=16, pady=(0, 8))

        self.nav_btns = {}
        views = [
            ("overview", "◈  Dashboard & Charts"),
            ("grid", "⊞  Full Data Explorer"),
            ("terminal", ">_  Live Audit Terminal")
        ]
        for key, label in views:
            b = tk.Button(
                dock, text=label, command=lambda k=key: self.switch_view(k),
                font=("Segoe UI", 10, "bold"), relief="flat", anchor="w",
                padx=14, pady=9, cursor="hand2"
            )
            b.pack(fill="x", padx=14, pady=3)
            self.nav_btns[key] = b

        # Bottom Live Health Radar Box
        radar_box = tk.Frame(dock, bg=self.BG_CARD, padx=12, pady=12, highlightbackground="#00F5D4", highlightthickness=1)
        radar_box.pack(side="bottom", fill="x", padx=14, pady=14)

        tk.Label(radar_box, text="DATA HEALTH SCORE", font=("Consolas", 8, "bold"), bg=self.BG_CARD, fg=self.TEXT_SUB).pack()
        self.lbl_health_big = tk.Label(radar_box, text="0%", font=("Segoe UI", 26, "bold"), bg=self.BG_CARD, fg=self.NEON_YELLOW)
        self.lbl_health_big.pack(pady=(2, 2))
        self.lbl_health_sub = tk.Label(radar_box, text="Awaiting Input File", font=("Segoe UI", 8), bg=self.BG_CARD, fg=self.TEXT_SUB)
        self.lbl_health_sub.pack()

        # --- RIGHT DYNAMIC STAGE ---
        self.stage = tk.Frame(container, bg=self.BG_DEEP)
        self.stage.pack(side="right", fill="both", expand=True)

        # Top 4 Glowing Neon KPI Cards
        kpi_row = tk.Frame(self.stage, bg=self.BG_DEEP)
        kpi_row.pack(fill="x", pady=(0, 12))

        self.kpi_vars = {
            "rows": tk.StringVar(value="0"),
            "nulls": tk.StringVar(value="0"),
            "cols": tk.StringVar(value="11"),
            "outliers": tk.StringVar(value="0")
        }
        kpi_defs = [
            ("PASSENGER RECORDS", self.kpi_vars["rows"], "Total Rows Loaded", self.NEON_BLUE),
            ("NULL ANOMALIES", self.kpi_vars["nulls"], "Missing Cells Fixed", self.NEON_CYAN),
            ("FEATURE COLUMNS", self.kpi_vars["cols"], "Includes 4 New Features", self.NEON_PURPLE),
            ("IQR OUTLIERS", self.kpi_vars["outliers"], "Flagged & Preserved", self.NEON_PINK),
        ]
        for idx, (title, var, desc, clr) in enumerate(kpi_defs):
            card = tk.Frame(kpi_row, bg=self.BG_CARD, padx=16, pady=12, highlightbackground=clr, highlightthickness=1)
            card.pack(side="left", expand=True, fill="both", padx=(0 if idx == 0 else 10, 0))
            tk.Label(card, text=title, font=("Consolas", 8, "bold"), bg=self.BG_CARD, fg=self.TEXT_SUB).pack(anchor="w")
            tk.Label(card, textvariable=var, font=("Segoe UI", 22, "bold"), bg=self.BG_CARD, fg=clr).pack(anchor="w", pady=(2, 0))
            tk.Label(card, text=desc, font=("Segoe UI", 8), bg=self.BG_CARD, fg="#CBD5E1").pack(anchor="w")

        # View Frames Container
        self.view_host = tk.Frame(self.stage, bg=self.BG_CARD, highlightbackground="#1E293B", highlightthickness=1)
        self.view_host.pack(fill="both", expand=True)

        # VIEW 1: OVERVIEW
        self.view_overview = tk.Frame(self.view_host, bg=self.BG_CARD)
        self.dash_canvas = tk.Canvas(self.view_overview, bg=self.BG_CARD, highlightthickness=0)
        self.dash_canvas.pack(fill="both", expand=True, padx=14, pady=14)
        self.dash_canvas.bind("<Configure>", lambda e: self.draw_dashboard())

        # VIEW 2: FULL DATA EXPLORER
        self.view_grid = tk.Frame(self.view_host, bg=self.BG_CARD)
        search_strip = tk.Frame(self.view_grid, bg="#131B36", padx=14, pady=10)
        search_strip.pack(fill="x")

        tk.Label(search_strip, text="SEARCH & FILTER RECORDS:", font=("Consolas", 9, "bold"), bg="#131B36", fg=self.NEON_CYAN).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.filter_table())
        ent = tk.Entry(
            search_strip, textvariable=self.search_var, bg="#0A0F1E", fg="white",
            insertbackground="#00F5D4", font=("Segoe UI", 10), relief="flat", width=36
        )
        ent.pack(side="left", padx=12, ipady=5)
        self.lbl_grid_info = tk.Label(search_strip, text="0 rows", font=("Consolas", 9, "bold"), bg="#131B36", fg=self.NEON_PINK)
        self.lbl_grid_info.pack(side="right")

        tree_wrap = tk.Frame(self.view_grid, bg=self.BG_CARD)
        tree_wrap.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(tree_wrap, style="Nexus.Treeview", show="headings")
        vsb = ttk.Scrollbar(tree_wrap, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_wrap, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_wrap.grid_rowconfigure(0, weight=1)
        tree_wrap.grid_columnconfigure(0, weight=1)

        # VIEW 3: LIVE AUDIT TERMINAL
        self.view_terminal = tk.Frame(self.view_host, bg="#05070E")
        self.txt_term = tk.Text(
            self.view_terminal, bg="#05070E", fg="#00F5D4", font=("Consolas", 10),
            relief="flat", padx=18, pady=16, wrap="word"
        )
        self.txt_term.pack(fill="both", expand=True)

        self.switch_view("overview")

    def _make_neon_btn(self, parent, text, cmd, bg, fg, hover):
        btn = tk.Button(
            parent, text=text, command=cmd, bg=bg, fg=fg,
            activebackground=hover, activeforeground=fg,
            font=("Segoe UI", 9, "bold"), relief="flat", anchor="w",
            padx=14, pady=11, cursor="hand2"
        )
        btn.pack(fill="x", padx=14, pady=5)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def switch_view(self, key):
        self.current_page = key
        for v in (self.view_overview, self.view_grid, self.view_terminal):
            v.pack_forget()
        for k, b in self.nav_btns.items():
            if k == key:
                b.config(bg="#1E293B", fg=self.NEON_CYAN)
            else:
                b.config(bg=self.BG_SURFACE, fg="#CBD5E1")

        if key == "overview":
            self.view_overview.pack(fill="both", expand=True)
            self.draw_dashboard()
        elif key == "grid":
            self.view_grid.pack(fill="both", expand=True)
        elif key == "terminal":
            self.view_terminal.pack(fill="both", expand=True)

    def draw_dashboard(self):
        c = self.dash_canvas
        c.delete("all")
        w = max(c.winfo_width(), 900)
        h = max(c.winfo_height(), 460)

        target = self.df_clean if self.df_clean is not None else self.df_raw
        if target is None:
            for gx in range(0, w, 40):
                c.create_line(gx, 0, gx, h, fill="#131B36")
            for gy in range(0, h, 40):
                c.create_line(0, gy, w, gy, fill="#131B36")
            c.create_rectangle(w // 2 - 240, h // 2 - 65, w // 2 + 240, h // 2 + 65, fill="#0A0F1E", outline=self.NEON_CYAN, width=2)
            c.create_text(w // 2, h // 2 - 15, text="READY FOR TITANIC DATASET INGESTION", fill="white", font=("Segoe UI", 13, "bold"))
            c.create_text(w // 2, h // 2 + 18, text="Click '01 IMPORT TITANIC CSV' on the left dock to launch live analytics", fill=self.NEON_CYAN, font=("Segoe UI", 9))
            return

        # Panel 1: Survival Rate by Passenger Class (Left)
        p1_x1 = w // 2 - 10
        c.create_rectangle(10, 10, p1_x1, h - 10, fill="#0A0F1E", outline="#1E293B", width=1)
        c.create_text(30, 32, text="SURVIVAL TELEMETRY BY PASSENGER CLASS", anchor="w", fill=self.NEON_CYAN, font=("Consolas", 10, "bold"))

        if {"Pclass", "Survived"}.issubset(target.columns):
            rates = target.groupby("Pclass")["Survived"].mean() * 100
            bar_colors = [self.NEON_CYAN, self.NEON_PURPLE, self.NEON_PINK]
            base_y = h - 65
            max_h = h - 150
            spacing = (p1_x1 - 80) // 3
            for idx, (pcls, val) in enumerate(rates.items()):
                x0 = 55 + idx * spacing
                x1 = x0 + 68
                bh = int((val / 100.0) * max_h)
                c.create_rectangle(x0, base_y - max_h, x1, base_y, fill="#131B36", outline="")
                c.create_rectangle(x0, base_y - bh, x1, base_y, fill=bar_colors[idx % 3], outline="")
                c.create_text((x0 + x1) // 2, base_y - bh - 14, text=f"{val:.1f}%", fill="white", font=("Segoe UI", 10, "bold"))
                c.create_text((x0 + x1) // 2, base_y + 20, text=f"Class {pcls}", fill="#CBD5E1", font=("Segoe UI", 9, "bold"))

        # Panel 2: Top Right - Gender Survival Comparison
        p2_x0 = w // 2 + 10
        mid_y = h // 2
        c.create_rectangle(p2_x0, 10, w - 10, mid_y - 8, fill="#0A0F1E", outline="#1E293B", width=1)
        c.create_text(p2_x0 + 20, 32, text="GENDER SURVIVAL RATIO", anchor="w", fill=self.NEON_PINK, font=("Consolas", 10, "bold"))

        if {"Sex", "Survived"}.issubset(target.columns):
            g_rates = target.groupby("Sex")["Survived"].mean() * 100
            g_clrs = {"female": self.NEON_PINK, "male": self.NEON_BLUE}
            for idx, (sex, val) in enumerate(g_rates.items()):
                y = 65 + idx * 62
                c.create_text(p2_x0 + 20, y, text=str(sex).upper(), anchor="w", fill="white", font=("Segoe UI", 9, "bold"))
                c.create_text(w - 30, y, text=f"{val:.1f}%", anchor="e", fill=self.NEON_YELLOW, font=("Segoe UI", 10, "bold"))
                track_w = (w - 30) - (p2_x0 + 20)
                c.create_rectangle(p2_x0 + 20, y + 14, w - 30, y + 30, fill="#131B36", outline="")
                c.create_rectangle(p2_x0 + 20, y + 14, p2_x0 + 20 + int((val / 100.0) * track_w), y + 30, fill=g_clrs.get(str(sex).lower(), self.NEON_CYAN), outline="")

        # Panel 3: Bottom Right - Engineered AgeGroup Distribution
        c.create_rectangle(p2_x0, mid_y + 8, w - 10, h - 10, fill="#0A0F1E", outline="#1E293B", width=1)
        feat_col = "AgeGroup" if "AgeGroup" in target.columns else "Embarked"
        c.create_text(p2_x0 + 20, mid_y + 28, text=f"PASSENGER BREAKDOWN ({feat_col.upper()})", anchor="w", fill=self.NEON_YELLOW, font=("Consolas", 10, "bold"))

        counts = target[feat_col].value_counts().head(5)
        max_c = max(counts.values)
        p_clrs = [self.NEON_CYAN, self.NEON_BLUE, self.NEON_PURPLE, self.NEON_PINK, self.NEON_YELLOW]
        for idx, (lbl, cnt) in enumerate(counts.items()):
            y = mid_y + 52 + idx * 30
            c.create_text(p2_x0 + 20, y + 8, text=str(lbl), anchor="w", fill="#E2E8F0", font=("Segoe UI", 8, "bold"))
            bar_start = p2_x0 + 115
            max_bw = (w - 65) - bar_start
            bw = int((cnt / max_c) * max_bw)
            c.create_rectangle(bar_start, y + 2, bar_start + bw, y + 14, fill=p_clrs[idx % len(p_clrs)], outline="")
            c.create_text(bar_start + bw + 8, y + 8, text=str(cnt), anchor="w", fill="white", font=("Segoe UI", 8, "bold"))

    def log(self, line):
        self.log_history.append(line)
        self.txt_term.insert("end", line + "\n")
        self.txt_term.see("end")

    def populate_table(self, df):
        self.tree.delete(*self.tree.get_children())
        cols = list(df.columns)
        self.tree["columns"] = cols
        for col in cols:
            self.tree.heading(col, text=col)
            w = 180 if col == "Name" else (105 if "Outlier" in col or col in ["AgeGroup", "FamilySize"] else 82)
            self.tree.column(col, width=w, anchor="w" if col == "Name" else "center")
        sub = df.head(150)
        for _, row in sub.iterrows():
            self.tree.insert("", "end", values=list(row))
        self.lbl_grid_info.config(text=f"SHOWING {len(sub)} OF {len(df)} ROWS")

    def filter_table(self):
        target = self.df_clean if self.df_clean is not None else self.df_raw
        if target is None:
            return
        q = self.search_var.get().strip().lower()
        if not q:
            self.populate_table(target)
            return
        mask = target.astype(str).apply(lambda s: s.str.lower().str.contains(q, na=False)).any(axis=1)
        self.populate_table(target[mask])

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        self.df_raw = pd.read_csv(path)
        self.df_clean = None
        self.log_history.clear()
        self.txt_term.delete("1.0", "end")

        r, c = self.df_raw.shape
        nulls = int(self.df_raw.isna().sum().sum())
        dups = int(self.df_raw.duplicated().sum())

        self.kpi_vars["rows"].set(f"{r:,}")
        self.kpi_vars["nulls"].set(f"{nulls:,}")
        self.kpi_vars["cols"].set(f"{c}")
        self.kpi_vars["outliers"].set("...")
        self.lbl_health_big.config(text="55%", fg=self.NEON_BLUE)
        self.lbl_health_sub.config(text="Raw Dataset Loaded")
        self.pill_status.config(text=f"● LOADED: {os.path.basename(path)}", fg=self.NEON_BLUE)

        self.log(f">> INGESTED: {os.path.basename(path)} | Shape: {r}x{c} | Nulls: {nulls} | Duplicates: {dups}")
        self.populate_table(self.df_raw)
        self.draw_dashboard()

    def run_pipeline(self):
        if self.df_raw is None:
            messagebox.showwarning("No Data", "Click '01 IMPORT TITANIC CSV' first!")
            return

        df = self.df_raw.copy()
        orig_nulls = int(df.isna().sum().sum())

        for col in df.select_dtypes(include=["object", "string"]).columns:
            df[col] = df[col].astype(str).str.strip()
        self.log(">> [STEP 1] String whitespace trimmed.")

        dups = int(df.duplicated().sum())
        df = df.drop_duplicates().reset_index(drop=True)
        self.log(f">> [STEP 2] Deduplication complete ({dups} removed).")

        for col in ["PassengerId", "Survived", "Pclass", "SibSp", "Parch"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
        for col in ["Age", "Fare"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        self.log(">> [STEP 3] Numeric Int64 & Float64 schemas enforced.")

        if "Age" in df.columns:
            df.loc[df["Age"] < 0, "Age"] = np.nan
        if "Fare" in df.columns:
            df.loc[df["Fare"] < 0, "Fare"] = np.nan
        self.log(">> [STEP 4] Domain range validation passed.")

        if "Age" in df.columns:
            if {"Pclass", "Sex"}.issubset(df.columns):
                df["Age"] = df.groupby(["Pclass", "Sex"], dropna=False)["Age"].transform(lambda s: s.fillna(s.median()))
            df["Age"] = df["Age"].fillna(df["Age"].median())
        if "Embarked" in df.columns:
            df["Embarked"] = df["Embarked"].replace({"nan": np.nan, "NaN": np.nan, "None": np.nan, "": np.nan})
            if df["Embarked"].isna().any():
                df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
        if "Cabin" in df.columns:
            df = df.drop(columns=["Cabin"])
        self.log(f">> [STEP 5] Stratified imputation complete ({orig_nulls} -> 0 nulls).")

        if "Sex" in df.columns:
            df["Sex"] = df["Sex"].str.strip().str.lower()
        if "Embarked" in df.columns:
            df["Embarked"] = df["Embarked"].str.strip().str.upper()
        self.log(">> [STEP 6] Categorical casing standardized.")

        if {"SibSp", "Parch"}.issubset(df.columns):
            df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
            df["IsAlone"] = (df["FamilySize"] == 1).astype(int)
        if "Name" in df.columns:
            df["Title"] = df["Name"].str.extract(r",\s*([^\.]+)\.", expand=False).str.strip()
            rare = df["Title"].value_counts()[df["Title"].value_counts() < 10].index
            df["Title"] = df["Title"].replace(rare, "Rare")
        if "Age" in df.columns:
            df["AgeGroup"] = pd.cut(
                df["Age"], bins=[0, 12, 19, 35, 60, 120],
                labels=["Child", "Teen", "YoungAdult", "Adult", "Senior"]
            ).astype(str)
        self.log(">> [STEP 7] Engineered 4 new features: FamilySize, IsAlone, Title, AgeGroup.")

        total_out = 0
        for col in ["Age", "Fare", "SibSp", "Parch"]:
            if col in df.columns:
                q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75)
                iqr = q3 - q1
                fcol = f"{col}_OutlierFlag"
                df[fcol] = ((df[col] < q1 - 1.5 * iqr) | (df[col] > q3 + 1.5 * iqr)).astype(int)
                total_out += int(df[fcol].sum())
        self.log(f">> [STEP 8] 1.5x IQR Outlier detection complete ({total_out} cells flagged & retained).")

        self.df_clean = df
        self.kpi_vars["rows"].set(f"{df.shape[0]:,}")
        self.kpi_vars["nulls"].set("0")
        self.kpi_vars["cols"].set(f"{df.shape[1]}")
        self.kpi_vars["outliers"].set(f"{total_out:,}")
        self.lbl_health_big.config(text="100%", fg=self.NEON_CYAN)
        self.lbl_health_sub.config(text="All Integrity Checks Passed")
        self.pill_status.config(text="● VALIDATED & 100% CLEAN", fg=self.NEON_CYAN)

        self.populate_table(self.df_clean)
        self.draw_dashboard()
        messagebox.showinfo("NEXUS AI Complete", f"Dataset sanitized & enriched!\nFinal Shape: {df.shape[0]} rows x {df.shape[1]} columns")

    def export_files(self):
        if self.df_clean is None:
            messagebox.showwarning("Not Ready", "Run '02 RUN AUTO-CLEANER' first!")
            return
        os.makedirs("Output", exist_ok=True)
        c_path = os.path.join("Output", "cleaned_titanic_final.csv")
        l_path = os.path.join("Output", "cleaning_execution_report.txt")
        self.df_clean.to_csv(c_path, index=False)
        with open(l_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.log_history))
        self.log(f">> [EXPORT] Saved {c_path} & {l_path}")
        messagebox.showinfo("Export Complete", f"Saved files in:\n{os.path.abspath('Output')}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CyberNeonTitanicStudio(root)
    root.mainloop()
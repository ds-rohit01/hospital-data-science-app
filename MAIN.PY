import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import os

# =========================================================
# COLORS / THEME
# =========================================================

BG = "#F4F8FB"
HEADER = "#0B3954"
PRIMARY = "#087EA4"
ACCENT = "#20A39E"
CARD = "#FFFFFF"
TEXT = "#17324D"
SECONDARY = "#64748B"
SUCCESS = "#2EAD70"
WARNING = "#F4A261"
ERROR = "#D9534F"
BORDER = "#D9E4EC"


# =========================================================
# GLOBAL VARIABLES
# =========================================================

df = None
content_frame = None
status_var = None


# =========================================================
# BASIC HELPERS
# =========================================================

def clear_content():
    """Remove everything from main content area."""
    for widget in content_frame.winfo_children():
        widget.destroy()


def update_status(text):
    status_var.set(text)


def clean_number(series):
    """
    Convert values like:
    1000
    ₹1000
    1,000
    into numbers.
    """
    return pd.to_numeric(
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("₹", "", regex=False),
        errors="coerce"
    )


def find_column(names):
    """
    Automatically find a column even if its name is slightly different.
    """
    if df is None:
        return None

    normalized = {
        str(c).strip().lower(): c
        for c in df.columns
    }

    # Exact match
    for name in names:
        key = str(name).strip().lower()

        if key in normalized:
            return normalized[key]

    # Partial match
    for column in df.columns:
        column_name = str(column).strip().lower()

        for name in names:
            if str(name).strip().lower() in column_name:
                return column

    return None


def create_card(parent, title, value, color=PRIMARY):
    frame = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#D9E4EC",
        highlightthickness=1,
        padx=18,
        pady=15
    )

    tk.Label(
        frame,
        text=title,
        bg=CARD,
        fg=SECONDARY,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w")

    tk.Label(
        frame,
        text=value,
        bg=CARD,
        fg=color,
        font=("Segoe UI", 18, "bold")
    ).pack(anchor="w", pady=(5, 0))

    return frame


# =========================================================
# BACK BUTTON
# =========================================================

def back_button(parent):
    """
    Common Back button.
    It always returns to Dashboard.
    """

    button = tk.Button(
        parent,
        text="← Back",
        command=show_dashboard,
        bg=HEADER,
        fg="white",
        activebackground=PRIMARY,
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=16,
        pady=7,
        cursor="hand2"
    )

    button.pack(
        anchor="w",
        padx=20,
        pady=(12, 5)
    )

    return button


# =========================================================
# PAGE TITLE
# =========================================================

def page_title(parent, title, subtitle=""):

    tk.Label(
        parent,
        text=title,
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 22, "bold")
    ).pack(
        anchor="w",
        padx=25,
        pady=(10, 2)
    )

    if subtitle:

        tk.Label(
            parent,
            text=subtitle,
            bg=BG,
            fg=SECONDARY,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            padx=25,
            pady=(0, 12)
        )


# =========================================================
# NO DATA PAGE
# =========================================================

def show_no_data():

    clear_content()

    page_title(
        content_frame,
        "No Data Loaded",
        "Please load a CSV or Excel file first."
    )

    box = tk.Frame(
        content_frame,
        bg=CARD,
        padx=30,
        pady=30,
        highlightbackground="#D9E4EC",
        highlightthickness=1
    )

    box.pack(
        fill="x",
        padx=25,
        pady=20
    )

    tk.Label(
        box,
        text="📂",
        bg=CARD,
        fg=PRIMARY,
        font=("Segoe UI Emoji", 35)
    ).pack()

    tk.Label(
        box,
        text="No hospital dataset is currently loaded.",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    ).pack(pady=8)

    tk.Label(
        box,
        text="Go to Dashboard → Load Data",
        bg=CARD,
        fg=SECONDARY,
        font=("Segoe UI", 10)
    ).pack()


# =========================================================
# HOME PAGE
# =========================================================
def show_home():
    clear_content()
    update_status("Home")

    # =====================================================
    # HERO SECTION - matching the requested Home design
    # =====================================================

    hero_wrap = tk.Frame(
        content_frame,
        bg=BG
    )
    hero_wrap.pack(
        fill="x",
        padx=34,
        pady=(18, 22)
    )

    hero = tk.Frame(
        hero_wrap,
        bg=HEADER,
        height=278,
        highlightbackground="#C8DCE8",
        highlightthickness=1
    )
    hero.pack(fill="x")
    hero.pack_propagate(False)

    # -----------------------------------------------------
    # LEFT HERO CONTENT
    # -----------------------------------------------------

    left = tk.Frame(
        hero,
        bg=HEADER
    )
    left.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(46, 12),
        pady=25
    )

    # Accent line
    tk.Frame(
        left,
        bg="#59D6D8",
        width=5,
        height=98
    ).pack(
        side="left",
        anchor="n",
        pady=(14, 0),
        padx=(0, 22)
    )

    text_area = tk.Frame(
        left,
        bg=HEADER
    )
    text_area.pack(
        side="left",
        fill="both",
        expand=True
    )

    # Title with separate colors
    title_line = tk.Frame(
        text_area,
        bg=HEADER
    )
    title_line.pack(
        anchor="w",
        pady=(13, 0)
    )

    tk.Label(
        title_line,
        text="Hospital ",
        bg=HEADER,
        fg="white",
        font=("Segoe UI", 30, "bold")
    ).pack(side="left")

    tk.Label(
        title_line,
        text="Analysis",
        bg=HEADER,
        fg="#63D7EA",
        font=("Segoe UI", 30, "bold")
    ).pack(side="left")

    tk.Label(
        text_area,
        text="Trusted Care for Every Stage of Life",
        bg=HEADER,
        fg="#F2F8FC",
        font=("Segoe UI", 15, "bold")
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    tk.Label(
        text_area,
        text=(
            "A Python Tkinter dashboard for analysing patients, doctors, diseases,\n"
            "departments, revenue and Hospital performance."
        ),
        bg=HEADER,
        fg="#DCEAF2",
        justify="left",
        font=("Segoe UI", 10)
    ).pack(
        anchor="w",
        pady=(12, 15)
    )

    pill = tk.Frame(
        text_area,
        bg="#1A5874"
    )
    pill.pack(anchor="w")

    tk.Label(
        pill,
        text="♡  Better Data   →   Better Decisions   →   Better Healthcare",
        bg="#1A5874",
        fg="white",
        font=("Segoe UI", 9, "bold"),
        padx=14,
        pady=7
    ).pack()

    # -----------------------------------------------------
    # RIGHT HERO IMAGE
    # -----------------------------------------------------

    right = tk.Frame(
        hero,
        bg=HEADER,
        width=900,
        height=278
    )
    right.pack(
        side="right",
        fill="y"
    )
    right.pack_propagate(False)

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # Accept the image names used during the project.
        candidates = [
            # Cropped hospital-building image only.
            # This prevents the reference screenshot's header/buttons
            # from appearing again inside the hero section.
            "hospital_hero.png",
            "hospital.jpg(4).png",
            "hospital.jpg(3).png",
            "hospital.jpg.png"
        ]

        image_path = None
        for filename in candidates:
            candidate = os.path.join(base_dir, filename)
            if os.path.exists(candidate):
                image_path = candidate
                break

        if image_path is None:
            raise FileNotFoundError("Hospital hero image not found")

        image = Image.open(image_path).convert("RGB")
        image = image.resize((900, 278), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            right,
            image=photo,
            bg=HEADER,
            bd=0,
            highlightthickness=0
        )
        image_label.pack(
            fill="both",
            expand=True
        )
        image_label.image = photo

    except Exception:
        # Keep the page usable if the image is not beside MAIN.PY.
        tk.Label(
            right,
            text="🏥",
            bg=HEADER,
            fg="white",
            font=("Segoe UI Emoji", 78)
        ).pack(expand=True)

    # =====================================================
    # THREE FEATURE CARDS
    # =====================================================

    features = tk.Frame(
        content_frame,
        bg=BG
    )
    features.pack(
        fill="x",
        padx=34,
        pady=(0, 22)
    )

    for i in range(3):
        features.columnconfigure(i, weight=1)

    cards = [
        (
            "PROJECT",
            "Hospital Analytics",
            "Complete hospital data analysis & reporting",
            "#087EA4",
            "▱",
            "#E7F5FC"
        ),
        (
            "TECHNOLOGY",
            "Python + Tkinter",
            "Powerful • Simple • Efficient",
            "#20A39E",
            "⌘",
            "#E8F8F5"
        ),
        (
            "VISUALS",
            "Matplotlib Charts",
            "Clear Insights • Beautiful Visuals",
            "#6C63D9",
            "▥",
            "#F0EDFF"
        )
    ]

    for i, (small, title, subtitle, color, icon, icon_bg) in enumerate(cards):

        card = tk.Frame(
            features,
            bg=CARD,
            highlightbackground="#D2E1EB",
            highlightthickness=1,
            height=132
        )
        card.grid(
            row=0,
            column=i,
            sticky="nsew",
            padx=(0 if i == 0 else 8, 8 if i < 2 else 0)
        )
        card.grid_propagate(False)

        icon_box = tk.Label(
            card,
            text=icon,
            bg=icon_bg,
            fg=color,
            font=("Segoe UI", 23, "bold"),
            width=3,
            height=2
        )
        icon_box.pack(
            side="left",
            padx=18,
            pady=22
        )

        info = tk.Frame(
            card,
            bg=CARD
        )
        info.pack(
            side="left",
            fill="both",
            expand=True,
            pady=19
        )

        tk.Label(
            info,
            text=small,
            bg=CARD,
            fg="#7C9AB7",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            info,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            info,
            text=subtitle,
            bg=CARD,
            fg="#7692AD",
            font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(3, 0))

        tk.Label(
            card,
            text="›",
            bg=CARD,
            fg=color,
            font=("Segoe UI", 27)
        ).pack(
            side="right",
            padx=15
        )

    # =====================================================
    # WHAT YOU CAN DO
    # =====================================================

    what_box = tk.Frame(
        content_frame,
        bg=CARD,
        highlightbackground="#D2E1EB",
        highlightthickness=1
    )
    what_box.pack(
        fill="x",
        padx=34,
        pady=(0, 18)
    )

    heading = tk.Frame(
        what_box,
        bg=CARD
    )
    heading.pack(
        fill="x",
        padx=32,
        pady=(20, 12)
    )

    tk.Label(
        heading,
        text="▣",
        bg="#E2F3F8",
        fg="#147B9B",
        font=("Segoe UI", 18, "bold"),
        width=3,
        height=2
    ).pack(side="left")

    tk.Label(
        heading,
        text="What You Can Do",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 20, "bold")
    ).pack(
        side="left",
        padx=16
    )

    grid = tk.Frame(
        what_box,
        bg=CARD
    )
    grid.pack(
        fill="x",
        padx=50,
        pady=(0, 22)
    )

    columns = [
        [
            "Load CSV or Excel hospital data",
            "View complete patient records"
        ],
        [
            "Analyse hospital statistics",
            "Find top doctors and diseases"
        ],
        [
            "Analyse departments and procedures",
            "Generate real charts from the loaded data"
        ]
    ]

    for col in range(3):
        grid.columnconfigure(col, weight=1)

        if col < 2:
            divider = tk.Frame(
                grid,
                bg="#E1EAF0",
                width=1
            )
            divider.grid(
                row=0,
                column=col,
                rowspan=2,
                sticky="ns",
                padx=(0, 0)
            )

        for row, item in enumerate(columns[col]):

            cell = tk.Frame(
                grid,
                bg=CARD
            )
            cell.grid(
                row=row,
                column=col,
                sticky="w",
                padx=(18 if col else 0, 28),
                pady=5
            )

            tk.Label(
                cell,
                text="✓",
                bg="#D8F4EC",
                fg="#128A7C",
                font=("Segoe UI", 10, "bold"),
                width=2
            ).pack(side="left")

            tk.Label(
                cell,
                text=item,
                bg=CARD,
                fg="#426B8F",
                font=("Segoe UI", 10)
            ).pack(
                side="left",
                padx=9
            )

# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    global df

    file_path = filedialog.askopenfilename(
        title="Select Hospital Dataset",
        filetypes=[
            ("CSV Files", "*.csv"),
            ("Excel Files", "*.xlsx *.xls"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:

        if file_path.lower().endswith(".csv"):

            new_df = pd.read_csv(file_path)

        else:

            new_df = pd.read_excel(file_path)

        if new_df.empty:

            messagebox.showwarning(
                "Empty File",
                "The selected file contains no data."
            )

            return

        df = new_df

        update_status(
            f"Loaded: {len(df):,} rows | {len(df.columns)} columns"
        )

        messagebox.showinfo(
            "Data Loaded",
            f"Successfully loaded:\n\n"
            f"Rows: {len(df):,}\n"
            f"Columns: {len(df.columns)}"
        )

        show_dashboard()

    except Exception as error:

        messagebox.showerror(
            "Load Error",
            f"Could not load the file.\n\n{error}"
        )


# =========================================================
# SHOW ALL DATA
# =========================================================

def show_all_data():

    if df is None:
        show_no_data()
        return

    clear_content()

    back_button(content_frame)

    page_title(
        content_frame,
        "All Hospital Data",
        f"{len(df):,} records • {len(df.columns)} columns"
    )

    wrapper = tk.Frame(
        content_frame,
        bg=BG
    )

    wrapper.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    table_frame = tk.Frame(
        wrapper,
        bg=CARD
    )

    table_frame.pack(
        fill="both",
        expand=True
    )

    y_scroll = ttk.Scrollbar(
        table_frame,
        orient="vertical"
    )

    x_scroll = ttk.Scrollbar(
        table_frame,
        orient="horizontal"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=list(df.columns),
        show="headings",
        yscrollcommand=y_scroll.set,
        xscrollcommand=x_scroll.set
    )

    y_scroll.config(
        command=tree.yview
    )

    x_scroll.config(
        command=tree.xview
    )

    y_scroll.pack(
        side="right",
        fill="y"
    )

    x_scroll.pack(
        side="bottom",
        fill="x"
    )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )

    for column in df.columns:

        tree.heading(
            column,
            text=str(column)
        )

        tree.column(
            column,
            width=140,
            minwidth=90,
            anchor="center"
        )

    for _, row in df.iterrows():

        values = []

        for value in row:

            if pd.isna(value):
                values.append("")
            else:
                values.append(str(value))

        tree.insert(
            "",
            "end",
            values=values
        )


# =========================================================
# STATISTICS PAGE
# =========================================================

def statistics_page():

    if df is None:
        show_no_data()
        return

    clear_content()

    back_button(content_frame)

    page_title(
        content_frame,
        "Hospital Statistics",
        "Key performance indicators from the loaded dataset"
    )

    # Find columns
    patient_col = find_column(
        ["Patient_ID", "Patient ID", "Patient"]
    )

    cost_col = find_column(
        ["Cost", "Revenue", "Total Revenue"]
    )

    doctor_col = find_column(
        ["Doctor_Name", "Doctor Name", "Doctor"]
    )

    disease_col = find_column(
        ["Condition", "Disease"]
    )

    age_col = find_column(
        ["Age"]
    )

    stay_col = find_column(
        ["Length_of_Stay", "Length of Stay", "Stay"]
    )

    satisfaction_col = find_column(
        ["Satisfaction"]
    )

    outcome_col = find_column(
        ["Outcome", "Status"]
    )

    readmission_col = find_column(
        ["Readmission", "Readmitted"]
    )

    # Calculations
    total_patients = (
        df[patient_col].nunique()
        if patient_col
        else len(df)
    )

    total_revenue = (
        clean_number(df[cost_col]).sum()
        if cost_col
        else None
    )

    total_doctors = (
        df[doctor_col].nunique()
        if doctor_col
        else None
    )

    total_diseases = (
        df[disease_col].nunique()
        if disease_col
        else None
    )

    average_age = (
        clean_number(df[age_col]).mean()
        if age_col
        else None
    )

    average_stay = (
        clean_number(df[stay_col]).mean()
        if stay_col
        else None
    )

    average_satisfaction = (
        clean_number(df[satisfaction_col]).mean()
        if satisfaction_col
        else None
    )

    # Cards
    cards_frame = tk.Frame(
        content_frame,
        bg=BG
    )

    cards_frame.pack(
        fill="x",
        padx=25,
        pady=10
    )

    statistics = [
        (
            "Total Patients",
            f"{total_patients:,}",
            PRIMARY
        ),

        (
            "Total Revenue",
            f"₹{total_revenue:,.2f}"
            if total_revenue is not None
            else "N/A",
            SUCCESS
        ),

        (
            "Total Doctors",
            f"{total_doctors:,}"
            if total_doctors is not None
            else "N/A",
            ACCENT
        ),

        (
            "Total Diseases",
            f"{total_diseases:,}"
            if total_diseases is not None
            else "N/A",
            WARNING
        ),

        (
            "Average Age",
            f"{average_age:.1f}"
            if pd.notna(average_age)
            else "N/A",
            PRIMARY
        ),

        (
            "Average Stay",
            f"{average_stay:.1f}"
            if pd.notna(average_stay)
            else "N/A",
            ACCENT
        ),

        (
            "Avg Satisfaction",
            f"{average_satisfaction:.1f}"
            if pd.notna(average_satisfaction)
            else "N/A",
            SUCCESS
        )
    ]

    for index, (title, value, color) in enumerate(statistics):

        row = index // 4
        column = index % 4

        create_card(
            cards_frame,
            title,
            value,
            color
        ).grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=5,
            pady=5
        )

    for i in range(4):
        cards_frame.columnconfigure(
            i,
            weight=1
        )

    # Additional analysis
    detail = tk.Frame(
        content_frame,
        bg=CARD,
        padx=20,
        pady=18,
        highlightbackground="#D9E4EC",
        highlightthickness=1
    )

    detail.pack(
        fill="x",
        padx=25,
        pady=15
    )

    tk.Label(
        detail,
        text="Additional Analysis",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 14, "bold")
    ).pack(anchor="w")

    if outcome_col:

        outcomes = (
            df[outcome_col]
            .astype(str)
            .value_counts()
        )

        text = "Outcome: " + " | ".join(
            f"{name}: {count}"
            for name, count in outcomes.items()
        )

        tk.Label(
            detail,
            text=text,
            bg=CARD,
            fg=SECONDARY,
            font=("Segoe UI", 10),
            wraplength=1000,
            justify="left"
        ).pack(
            anchor="w",
            pady=5
        )

    if readmission_col:

        read_values = (
            df[readmission_col]
            .astype(str)
            .str.lower()
            .str.strip()
        )

        read_count = read_values.isin(
            ["yes", "true", "1", "readmitted"]
        ).sum()

        tk.Label(
            detail,
            text=f"Readmissions detected: {read_count:,}",
            bg=CARD,
            fg=SECONDARY,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w",
            pady=3
        )


# =========================================================
# TOP RANKER
# =========================================================

def top_ranker():

    if df is None:
        show_no_data()
        return

    clear_content()

    back_button(content_frame)

    page_title(
        content_frame,
        "Top Ranker",
        "Doctor, disease, department and procedure performance"
    )

    outer = tk.Frame(
        content_frame,
        bg=BG
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=(0, 20)
    )

    canvas = tk.Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )

    scroll_frame = tk.Frame(
        canvas,
        bg=BG
    )

    scroll_frame.bind(
        "<Configure>",
        lambda event:
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=scroll_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    def rank_card(
        parent,
        title,
        value,
        subtitle,
        color
    ):

        box = tk.Frame(
            parent,
            bg=CARD,
            padx=18,
            pady=15,
            highlightbackground="#D9E4EC",
            highlightthickness=1
        )

        tk.Label(
            box,
            text=title,
            bg=CARD,
            fg=SECONDARY,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        tk.Label(
            box,
            text=str(value),
            bg=CARD,
            fg=color,
            font=("Segoe UI", 15, "bold")
        ).pack(
            anchor="w",
            pady=(5, 2)
        )

        tk.Label(
            box,
            text=subtitle,
            bg=CARD,
            fg=SECONDARY,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        return box

    # -----------------------------------------------------
    # DOCTOR
    # -----------------------------------------------------

    doctor_col = find_column(
        ["Doctor_Name", "Doctor Name", "Doctor"]
    )

    cost_col = find_column(
        ["Cost", "Revenue", "Total Revenue"]
    )

    satisfaction_col = find_column(
        ["Satisfaction"]
    )

    stay_col = find_column(
        ["Length_of_Stay", "Length of Stay", "Stay"]
    )

    if doctor_col:

        doctor_box = tk.LabelFrame(
            scroll_frame,
            text=" Doctor Performance ",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )

        doctor_box.pack(
            fill="x",
            pady=10
        )

        doctor_summary = (
            df.groupby(doctor_col)
            .size()
            .reset_index(name="Patients")
        )

        # Revenue
        if cost_col:

            temp = df.copy()

            temp["_cost_"] = clean_number(
                temp[cost_col]
            )

            revenue = (
                temp.groupby(doctor_col)["_cost_"]
                .sum()
                .reset_index(name="Revenue")
            )

            doctor_summary = doctor_summary.merge(
                revenue,
                on=doctor_col,
                how="left"
            )

        # Satisfaction
        if satisfaction_col:

            temp = df.copy()

            temp["_satisfaction_"] = clean_number(
                temp[satisfaction_col]
            )

            satisfaction = (
                temp.groupby(doctor_col)["_satisfaction_"]
                .mean()
                .reset_index(name="Avg Satisfaction")
            )

            doctor_summary = doctor_summary.merge(
                satisfaction,
                on=doctor_col,
                how="left"
            )

        # Stay
        if stay_col:

            temp = df.copy()

            temp["_stay_"] = clean_number(
                temp[stay_col]
            )

            stay = (
                temp.groupby(doctor_col)["_stay_"]
                .mean()
                .reset_index(name="Avg Stay")
            )

            doctor_summary = doctor_summary.merge(
                stay,
                on=doctor_col,
                how="left"
            )

        doctor_summary = doctor_summary.sort_values(
            "Patients",
            ascending=False
        )

        highest_patient = doctor_summary.iloc[0]

        lowest_patient = doctor_summary.iloc[-1]

        rank_card(
            doctor_box,
            "Highest Patient Count",
            highest_patient[doctor_col],
            f"{int(highest_patient['Patients'])} patients",
            PRIMARY
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        rank_card(
            doctor_box,
            "Lowest Patient Count",
            lowest_patient[doctor_col],
            f"{int(lowest_patient['Patients'])} patients",
            WARNING
        ).grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        if cost_col:

            highest_revenue = (
                doctor_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            lowest_revenue = (
                doctor_summary
                .sort_values(
                    "Revenue",
                    ascending=True
                )
                .iloc[0]
            )

            rank_card(
                doctor_box,
                "Highest Revenue",
                highest_revenue[doctor_col],
                f"₹{highest_revenue['Revenue']:,.2f}",
                SUCCESS
            ).grid(
                row=1,
                column=0,
                sticky="nsew",
                padx=5,
                pady=5
            )

            rank_card(
                doctor_box,
                "Lowest Revenue",
                lowest_revenue[doctor_col],
                f"₹{lowest_revenue['Revenue']:,.2f}",
                ERROR
            ).grid(
                row=1,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

        if satisfaction_col:

            highest_satisfaction = (
                doctor_summary
                .sort_values(
                    "Avg Satisfaction",
                    ascending=False
                )
                .iloc[0]
            )

            rank_card(
                doctor_box,
                "Highest Avg Satisfaction",
                highest_satisfaction[doctor_col],
                f"{highest_satisfaction['Avg Satisfaction']:.2f}",
                ACCENT
            ).grid(
                row=2,
                column=0,
                sticky="nsew",
                padx=5,
                pady=5
            )

        if stay_col:

            highest_stay = (
                doctor_summary
                .sort_values(
                    "Avg Stay",
                    ascending=False
                )
                .iloc[0]
            )

            rank_card(
                doctor_box,
                "Highest Avg Stay",
                highest_stay[doctor_col],
                f"{highest_stay['Avg Stay']:.2f} days",
                PRIMARY
            ).grid(
                row=2,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

        doctor_box.columnconfigure(
            0,
            weight=1
        )

        doctor_box.columnconfigure(
            1,
            weight=1
        )

        # Doctor table
        table_columns = [
            "Rank",
            "Doctor",
            "Patients"
        ]

        if cost_col:
            table_columns.append("Revenue")

        if satisfaction_col:
            table_columns.append("Avg Satisfaction")

        if stay_col:
            table_columns.append("Avg Stay")

        tree = ttk.Treeview(
            doctor_box,
            columns=table_columns,
            show="headings",
            height=12
        )

        for column in table_columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=160,
                anchor="center"
            )

        for rank, (_, row) in enumerate(
            doctor_summary.iterrows(),
            start=1
        ):

            values = [
                rank,
                row[doctor_col],
                int(row["Patients"])
            ]

            if cost_col:

                values.append(
                    f"₹{row['Revenue']:,.2f}"
                )

            if satisfaction_col:

                values.append(
                    f"{row['Avg Satisfaction']:.2f}"
                )

            if stay_col:

                values.append(
                    f"{row['Avg Stay']:.2f}"
                )

            tree.insert(
                "",
                "end",
                values=values
            )

        tree.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=10
        )

    # -----------------------------------------------------
    # DISEASE
    # -----------------------------------------------------

    disease_col = find_column(
        ["Condition", "Disease"]
    )

    if disease_col:

        disease_box = tk.LabelFrame(
            scroll_frame,
            text=" Disease Performance ",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )

        disease_box.pack(
            fill="x",
            pady=10
        )

        disease_summary = (
            df.groupby(disease_col)
            .size()
            .reset_index(name="Patients")
        )

        if cost_col:

            temp = df.copy()

            temp["_cost_"] = clean_number(
                temp[cost_col]
            )

            revenue = (
                temp.groupby(disease_col)["_cost_"]
                .sum()
                .reset_index(name="Revenue")
            )

            disease_summary = disease_summary.merge(
                revenue,
                on=disease_col,
                how="left"
            )

        common = (
            disease_summary
            .sort_values(
                "Patients",
                ascending=False
            )
            .iloc[0]
        )

        least = (
            disease_summary
            .sort_values(
                "Patients",
                ascending=True
            )
            .iloc[0]
        )

        rank_card(
            disease_box,
            "Most Common Disease",
            common[disease_col],
            f"{int(common['Patients'])} patients",
            PRIMARY
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        rank_card(
            disease_box,
            "Least Common Disease",
            least[disease_col],
            f"{int(least['Patients'])} patients",
            WARNING
        ).grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=5,
            pady=5
        )

        if cost_col:

            high = (
                disease_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            low = (
                disease_summary
                .sort_values(
                    "Revenue",
                    ascending=True
                )
                .iloc[0]
            )

            rank_card(
                disease_box,
                "Highest Revenue Disease",
                high[disease_col],
                f"₹{high['Revenue']:,.2f}",
                SUCCESS
            ).grid(
                row=1,
                column=0,
                sticky="nsew",
                padx=5,
                pady=5
            )

            rank_card(
                disease_box,
                "Lowest Revenue Disease",
                low[disease_col],
                f"₹{low['Revenue']:,.2f}",
                ERROR
            ).grid(
                row=1,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

        disease_box.columnconfigure(
            0,
            weight=1
        )

        disease_box.columnconfigure(
            1,
            weight=1
        )

        disease_columns = [
            "Rank",
            "Disease",
            "Patients"
        ]

        if cost_col:
            disease_columns.append("Revenue")

        tree = ttk.Treeview(
            disease_box,
            columns=disease_columns,
            show="headings",
            height=8
        )

        for column in disease_columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=180,
                anchor="center"
            )

        for rank, (_, row) in enumerate(
            disease_summary
            .sort_values(
                "Patients",
                ascending=False
            )
            .iterrows(),
            start=1
        ):

            values = [
                rank,
                row[disease_col],
                int(row["Patients"])
            ]

            if cost_col:

                values.append(
                    f"₹{row['Revenue']:,.2f}"
                )

            tree.insert(
                "",
                "end",
                values=values
            )

        tree.grid(
            row=2,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=5,
            pady=10
        )

    # -----------------------------------------------------
    # DEPARTMENT
    # -----------------------------------------------------

    department_col = find_column(
        ["Department", "Dept"]
    )

    if department_col:

        department_box = tk.LabelFrame(
            scroll_frame,
            text=" Department Performance ",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )

        department_box.pack(
            fill="x",
            pady=10
        )

        department_summary = (
            df.groupby(department_col)
            .size()
            .reset_index(name="Patients")
        )

        if cost_col:

            temp = df.copy()

            temp["_cost_"] = clean_number(
                temp[cost_col]
            )

            revenue = (
                temp.groupby(department_col)["_cost_"]
                .sum()
                .reset_index(name="Revenue")
            )

            department_summary = department_summary.merge(
                revenue,
                on=department_col,
                how="left"
            )

        highest_department = (
            department_summary
            .sort_values(
                "Patients",
                ascending=False
            )
            .iloc[0]
        )

        rank_card(
            department_box,
            "Highest Patient Department",
            highest_department[department_col],
            f"{int(highest_department['Patients'])} patients",
            PRIMARY
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        if cost_col:

            highest_revenue_department = (
                department_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            rank_card(
                department_box,
                "Highest Revenue Department",
                highest_revenue_department[department_col],
                f"₹{highest_revenue_department['Revenue']:,.2f}",
                SUCCESS
            ).grid(
                row=0,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

        department_box.columnconfigure(
            0,
            weight=1
        )

        department_box.columnconfigure(
            1,
            weight=1
        )

    # -----------------------------------------------------
    # PROCEDURE
    # -----------------------------------------------------

    procedure_col = find_column(
        ["Procedure", "Treatment"]
    )

    if procedure_col:

        procedure_box = tk.LabelFrame(
            scroll_frame,
            text=" Procedure Performance ",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 12, "bold"),
            padx=10,
            pady=10
        )

        procedure_box.pack(
            fill="x",
            pady=10
        )

        procedure_summary = (
            df.groupby(procedure_col)
            .size()
            .reset_index(name="Patients")
        )

        if cost_col:

            temp = df.copy()

            temp["_cost_"] = clean_number(
                temp[cost_col]
            )

            revenue = (
                temp.groupby(procedure_col)["_cost_"]
                .sum()
                .reset_index(name="Revenue")
            )

            procedure_summary = procedure_summary.merge(
                revenue,
                on=procedure_col,
                how="left"
            )

        common_procedure = (
            procedure_summary
            .sort_values(
                "Patients",
                ascending=False
            )
            .iloc[0]
        )

        rank_card(
            procedure_box,
            "Most Common Procedure",
            common_procedure[procedure_col],
            f"{int(common_procedure['Patients'])} patients",
            PRIMARY
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=5,
            pady=5
        )

        if cost_col:

            highest_procedure_revenue = (
                procedure_summary
                .sort_values(
                    "Revenue",
                    ascending=False
                )
                .iloc[0]
            )

            rank_card(
                procedure_box,
                "Highest Revenue Procedure",
                highest_procedure_revenue[procedure_col],
                f"₹{highest_procedure_revenue['Revenue']:,.2f}",
                SUCCESS
            ).grid(
                row=0,
                column=1,
                sticky="nsew",
                padx=5,
                pady=5
            )

        procedure_box.columnconfigure(
            0,
            weight=1
        )

        procedure_box.columnconfigure(
            1,
            weight=1
        )


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    clear_content()

    page_title(
        content_frame,
        "Dashboard",
        "Choose an analysis module"
    )

    grid = tk.Frame(
        content_frame,
        bg=BG
    )

    grid.pack(
        fill="both",
        expand=True,
        padx=25,
        pady=10
    )

    buttons = [
        ("📂  Load Data", load_data, PRIMARY),
        ("📋  Show All Data", show_all_data, ACCENT),
        ("📊  Statistics", statistics_page, SUCCESS),
        ("🏆  Top Ranker", top_ranker, WARNING),
        ("📈  Graphics Visuals", graphics_page, PRIMARY),
        ("ℹ  About", show_about, ACCENT),
        ("🗑  Clear Data", clear_data, ERROR)
    ]

    for index, (text, command, color) in enumerate(buttons):

        row = index // 3
        column = index % 3

        button = tk.Button(
            grid,
            text=text,
            command=command,
            bg=color,
            fg="white",
            activebackground=HEADER,
            activeforeground="white",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=22
        )

        button.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8
        )

    for i in range(3):

        grid.columnconfigure(
            i,
            weight=1
        )

    for i in range(3):

        grid.rowconfigure(
            i,
            weight=1
        )


# =========================================================
# CHART HELPER
# =========================================================

def create_chart(parent, figure, title):

    box = tk.Frame(
        parent,
        bg=CARD,
        highlightbackground="#D9E4EC",
        highlightthickness=1
    )

    box.pack(
        fill="x",
        padx=5,
        pady=10
    )

    tk.Label(
        box,
        text=title,
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 13, "bold")
    ).pack(
        anchor="w",
        padx=12,
        pady=8
    )

    chart = FigureCanvasTkAgg(
        figure,
        master=box
    )

    chart.draw()

    chart.get_tk_widget().pack(
        fill="both",
        expand=True,
        padx=8,
        pady=8
    )


# =========================================================
# GRAPHICS PAGE
# =========================================================

def graphics_page():

    if df is None:
        show_no_data()
        return

    clear_content()

    back_button(content_frame)

    page_title(
        content_frame,
        "Graphics Visuals",
        "Charts generated from the actual loaded dataset"
    )

    outer = tk.Frame(
        content_frame,
        bg=BG
    )

    outer.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=(0, 20)
    )

    canvas = tk.Canvas(
        outer,
        bg=BG,
        highlightthickness=0
    )

    scrollbar = ttk.Scrollbar(
        outer,
        orient="vertical",
        command=canvas.yview
    )

    chart_frame = tk.Frame(
        canvas,
        bg=BG
    )

    chart_frame.bind(
        "<Configure>",
        lambda event:
        canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window(
        (0, 0),
        window=chart_frame,
        anchor="nw"
    )

    canvas.configure(
        yscrollcommand=scrollbar.set
    )

    canvas.pack(
        side="left",
        fill="both",
        expand=True
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )

    # -----------------------------------------------------
    # FIND COLUMNS
    # -----------------------------------------------------

    doctor_col = find_column(
        ["Doctor_Name", "Doctor Name", "Doctor"]
    )

    disease_col = find_column(
        ["Condition", "Disease"]
    )

    cost_col = find_column(
        ["Cost", "Revenue", "Total Revenue"]
    )

    gender_col = find_column(
        ["Gender", "Sex"]
    )

    outcome_col = find_column(
        ["Outcome", "Status"]
    )

    readmission_col = find_column(
        ["Readmission", "Readmitted"]
    )

    age_col = find_column(
        ["Age"]
    )

    satisfaction_col = find_column(
        ["Satisfaction"]
    )

    stay_col = find_column(
        ["Length_of_Stay", "Length of Stay", "Stay"]
    )

    department_col = find_column(
        ["Department", "Dept"]
    )

    procedure_col = find_column(
        ["Procedure", "Treatment"]
    )

    date_col = find_column(
        ["Admission_Date", "Admission Date", "Date"]
    )

    # -----------------------------------------------------
    # DOCTOR PATIENT COUNT
    # -----------------------------------------------------

    if doctor_col:

        values = (
            df[doctor_col]
            .value_counts()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(9, 5)
        )

        ax.barh(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel("Patients")
        ax.set_ylabel("Doctor")
        ax.set_title("Doctor-wise Patient Count")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Doctor-wise Patient Count"
        )

    # -----------------------------------------------------
    # DOCTOR REVENUE
    # -----------------------------------------------------

    if doctor_col and cost_col:

        temp = df.copy()

        temp["_cost_"] = clean_number(
            temp[cost_col]
        )

        values = (
            temp.groupby(doctor_col)["_cost_"]
            .sum()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(9, 5)
        )

        ax.barh(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel("Revenue")
        ax.set_ylabel("Doctor")
        ax.set_title("Doctor-wise Revenue")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Doctor-wise Revenue"
        )

    # -----------------------------------------------------
    # DISEASE PATIENT COUNT
    # -----------------------------------------------------

    if disease_col:

        values = df[disease_col].value_counts()

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel("Disease / Condition")
        ax.set_ylabel("Patients")
        ax.set_title("Disease-wise Patient Count")

        plt.setp(
            ax.get_xticklabels(),
            rotation=35,
            ha="right"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Disease-wise Patient Count"
        )

    # -----------------------------------------------------
    # DISEASE REVENUE
    # -----------------------------------------------------

    if disease_col and cost_col:

        temp = df.copy()

        temp["_cost_"] = clean_number(
            temp[cost_col]
        )

        values = (
            temp.groupby(disease_col)["_cost_"]
            .sum()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel("Disease / Condition")
        ax.set_ylabel("Revenue")
        ax.set_title("Disease-wise Revenue")

        plt.setp(
            ax.get_xticklabels(),
            rotation=35,
            ha="right"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Disease-wise Revenue"
        )

    # -----------------------------------------------------
    # DISEASE DISTRIBUTION
    # -----------------------------------------------------

    if disease_col:

        values = df[disease_col].value_counts()

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.pie(
            values.values,
            labels=values.index.astype(str),
            autopct="%1.1f%%"
        )

        ax.set_title(
            "Disease Distribution"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Disease Distribution"
        )

    # -----------------------------------------------------
    # GENDER
    # -----------------------------------------------------

    if gender_col:

        values = (
            df[gender_col]
            .astype(str)
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.bar(
            values.index,
            values.values
        )

        ax.set_xlabel("Gender")
        ax.set_ylabel("Patients")
        ax.set_title("Gender Distribution")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Gender Distribution"
        )

    # -----------------------------------------------------
    # OUTCOME
    # -----------------------------------------------------

    if outcome_col:

        values = (
            df[outcome_col]
            .astype(str)
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.bar(
            values.index,
            values.values
        )

        ax.set_xlabel("Outcome")
        ax.set_ylabel("Patients")
        ax.set_title("Patient Outcome Distribution")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Patient Outcome Distribution"
        )

    # -----------------------------------------------------
    # READMISSION
    # -----------------------------------------------------

    if readmission_col:

        values = (
            df[readmission_col]
            .astype(str)
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(7, 5)
        )

        ax.bar(
            values.index,
            values.values
        )

        ax.set_xlabel("Readmission")
        ax.set_ylabel("Patients")
        ax.set_title("Readmission Analysis")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Readmission Analysis"
        )

    # -----------------------------------------------------
    # AGE
    # -----------------------------------------------------

    if age_col:

        values = (
            clean_number(
                df[age_col]
            )
            .dropna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        ax.hist(
            values,
            bins=12
        )

        ax.set_xlabel("Age")
        ax.set_ylabel("Patients")
        ax.set_title("Age Distribution")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Age Distribution"
        )

    # -----------------------------------------------------
    # SATISFACTION
    # -----------------------------------------------------

    if satisfaction_col:

        values = (
            clean_number(
                df[satisfaction_col]
            )
            .dropna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        ax.hist(
            values,
            bins=10
        )

        ax.set_xlabel("Satisfaction")
        ax.set_ylabel("Patients")
        ax.set_title("Satisfaction Distribution")

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Satisfaction Distribution"
        )

    # -----------------------------------------------------
    # LENGTH OF STAY VS COST
    # -----------------------------------------------------

    if stay_col and cost_col:

        x = clean_number(
            df[stay_col]
        )

        y = clean_number(
            df[cost_col]
        )

        valid = (
            x.notna()
            & y.notna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.scatter(
            x[valid],
            y[valid],
            alpha=0.6
        )

        ax.set_xlabel(
            "Length of Stay"
        )

        ax.set_ylabel(
            "Cost / Revenue"
        )

        ax.set_title(
            "Length of Stay vs Cost"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Length of Stay vs Cost"
        )

    # -----------------------------------------------------
    # AGE VS SATISFACTION
    # -----------------------------------------------------

    if age_col and satisfaction_col:

        x = clean_number(
            df[age_col]
        )

        y = clean_number(
            df[satisfaction_col]
        )

        valid = (
            x.notna()
            & y.notna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.scatter(
            x[valid],
            y[valid],
            alpha=0.6
        )

        ax.set_xlabel("Age")
        ax.set_ylabel("Satisfaction")
        ax.set_title(
            "Age vs Satisfaction"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Age vs Satisfaction"
        )

    # -----------------------------------------------------
    # DOCTOR PATIENTS VS REVENUE
    # -----------------------------------------------------

    if doctor_col and cost_col:

        temp = df.copy()

        temp["_cost_"] = clean_number(
            temp[cost_col]
        )

        summary = temp.groupby(
            doctor_col
        ).agg(
            Patients=(doctor_col, "size"),
            Revenue=("_cost_", "sum")
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.scatter(
            summary["Patients"],
            summary["Revenue"],
            s=70
        )

        for name, row in summary.iterrows():

            ax.annotate(
                str(name),
                (
                    row["Patients"],
                    row["Revenue"]
                ),
                fontsize=7,
                xytext=(4, 4),
                textcoords="offset points"
            )

        ax.set_xlabel(
            "Total Patients"
        )

        ax.set_ylabel(
            "Total Revenue"
        )

        ax.set_title(
            "Doctor Patients vs Revenue"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Doctor Patients vs Revenue"
        )

    # -----------------------------------------------------
    # DEPARTMENT PATIENT COUNT
    # -----------------------------------------------------

    if department_col:

        values = (
            df[department_col]
            .value_counts()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.barh(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel(
            "Patients"
        )

        ax.set_ylabel(
            "Department"
        )

        ax.set_title(
            "Department-wise Patient Count"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Department-wise Patient Count"
        )

    # -----------------------------------------------------
    # DEPARTMENT REVENUE
    # -----------------------------------------------------

    if department_col and cost_col:

        temp = df.copy()

        temp["_cost_"] = clean_number(
            temp[cost_col]
        )

        values = (
            temp.groupby(department_col)["_cost_"]
            .sum()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.barh(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel(
            "Revenue"
        )

        ax.set_ylabel(
            "Department"
        )

        ax.set_title(
            "Department-wise Revenue"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Department-wise Revenue"
        )

    # -----------------------------------------------------
    # PROCEDURE PATIENT COUNT
    # -----------------------------------------------------

    if procedure_col:

        values = (
            df[procedure_col]
            .value_counts()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel(
            "Procedure"
        )

        ax.set_ylabel(
            "Patients"
        )

        ax.set_title(
            "Procedure-wise Patient Count"
        )

        plt.setp(
            ax.get_xticklabels(),
            rotation=35,
            ha="right"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Procedure-wise Patient Count"
        )

    # -----------------------------------------------------
    # PROCEDURE REVENUE
    # -----------------------------------------------------

    if procedure_col and cost_col:

        temp = df.copy()

        temp["_cost_"] = clean_number(
            temp[cost_col]
        )

        values = (
            temp.groupby(procedure_col)["_cost_"]
            .sum()
            .sort_values()
        )

        fig, ax = plt.subplots(
            figsize=(8, 5)
        )

        ax.bar(
            values.index.astype(str),
            values.values
        )

        ax.set_xlabel(
            "Procedure"
        )

        ax.set_ylabel(
            "Revenue"
        )

        ax.set_title(
            "Procedure-wise Revenue"
        )

        plt.setp(
            ax.get_xticklabels(),
            rotation=35,
            ha="right"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Procedure-wise Revenue"
        )

    # -----------------------------------------------------
    # LENGTH OF STAY
    # -----------------------------------------------------

    if stay_col:

        values = (
            clean_number(
                df[stay_col]
            )
            .dropna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        ax.hist(
            values,
            bins=10
        )

        ax.set_xlabel(
            "Length of Stay"
        )

        ax.set_ylabel(
            "Patients"
        )

        ax.set_title(
            "Length of Stay Distribution"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Length of Stay Distribution"
        )

    # -----------------------------------------------------
    # COST DISTRIBUTION
    # -----------------------------------------------------

    if cost_col:

        values = (
            clean_number(
                df[cost_col]
            )
            .dropna()
        )

        fig, ax = plt.subplots(
            figsize=(8, 4.5)
        )

        ax.hist(
            values,
            bins=12
        )

        ax.set_xlabel(
            "Cost / Revenue"
        )

        ax.set_ylabel(
            "Patients"
        )

        ax.set_title(
            "Cost Distribution"
        )

        fig.tight_layout()

        create_chart(
            chart_frame,
            fig,
            "Cost Distribution"
        )

    # -----------------------------------------------------
    # MONTHLY TRENDS
    # -----------------------------------------------------

    if date_col:

        temp = df.copy()

        temp["_date_"] = pd.to_datetime(
            temp[date_col],
            errors="coerce"
        )

        valid = temp.dropna(
            subset=["_date_"]
        )

        if not valid.empty:

            monthly_patients = (
                valid.groupby(
                    valid["_date_"].dt.to_period("M")
                )
                .size()
            )

            fig, ax = plt.subplots(
                figsize=(9, 4.5)
            )

            ax.plot(
                monthly_patients.index.astype(str),
                monthly_patients.values,
                marker="o"
            )

            ax.set_xlabel(
                "Month"
            )

            ax.set_ylabel(
                "Patients"
            )

            ax.set_title(
                "Monthly Patient Trend"
            )

            plt.setp(
                ax.get_xticklabels(),
                rotation=45,
                ha="right"
            )

            fig.tight_layout()

            create_chart(
                chart_frame,
                fig,
                "Monthly Patient Trend"
            )

            # Monthly revenue
            if cost_col:

                valid = valid.copy()

                valid["_cost_"] = clean_number(
                    valid[cost_col]
                )

                monthly_revenue = (
                    valid.groupby(
                        valid["_date_"].dt.to_period("M")
                    )["_cost_"]
                    .sum()
                )

                fig, ax = plt.subplots(
                    figsize=(9, 4.5)
                )

                ax.plot(
                    monthly_revenue.index.astype(str),
                    monthly_revenue.values,
                    marker="o"
                )

                ax.set_xlabel(
                    "Month"
                )

                ax.set_ylabel(
                    "Revenue"
                )

                ax.set_title(
                    "Monthly Revenue Trend"
                )

                plt.setp(
                    ax.get_xticklabels(),
                    rotation=45,
                    ha="right"
                )

                fig.tight_layout()

                create_chart(
                    chart_frame,
                    fig,
                    "Monthly Revenue Trend"
                )

    # No chart
    if not chart_frame.winfo_children():

        tk.Label(
            chart_frame,
            text="No suitable columns were found for graphics.",
            bg=BG,
            fg=SECONDARY,
            font=("Segoe UI", 12)
        ).pack(
            pady=40
        )


# =========================================================
# ABOUT
# =========================================================

def show_about():

    clear_content()

    back_button(content_frame)

    page_title(
        content_frame,
        "About This Project",
        "Hospital Management & Data Analysis Dashboard"
    )

    box = tk.Frame(
        content_frame,
        bg=CARD,
        padx=30,
        pady=25,
        highlightbackground="#D9E4EC",
        highlightthickness=1
    )

    box.pack(
        fill="x",
        padx=25,
        pady=15
    )

    sections = [
        (
            "Project Purpose",
            "This project analyses hospital data and converts "
            "patient records into useful statistics, rankings and "
            "visual insights."
        ),

        (
            "Technology",
            "Python, Tkinter, Pandas and Matplotlib."
        ),

        (
            "Main Features",
            "CSV/Excel loading, patient data table, statistics, "
            "doctor rankings, disease analysis, department analysis, "
            "procedure analysis and graphical visualisation."
        ),

        (
            "Data Analysis",
            "The dashboard uses the actual dataset loaded by the user. "
            "Charts are generated only when the required columns are available."
        )
    ]

    for title, description in sections:

        tk.Label(
            box,
            text=title,
            bg=CARD,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(
            anchor="w",
            pady=(5, 3)
        )

        tk.Label(
            box,
            text=description,
            bg=CARD,
            fg=SECONDARY,
            font=("Segoe UI", 10),
            wraplength=1000,
            justify="left"
        ).pack(
            anchor="w",
            pady=(0, 12)
        )


# =========================================================
# CLEAR DATA
# =========================================================

def clear_data():

    global df

    if df is None:

        messagebox.showinfo(
            "Clear Data",
            "No data is currently loaded."
        )

        return

    answer = messagebox.askyesno(
        "Clear Data",
        "Are you sure you want to remove the currently loaded dataset?"
    )

    if answer:

        df = None

        update_status(
            "No dataset loaded"
        )

        messagebox.showinfo(
            "Cleared",
            "Dataset cleared successfully."
        )

        show_dashboard()


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "Hospital Analysis Dashboard"
)

root.geometry(
    "1250x780"
)

root.minsize(
    1000,
    650
)

root.configure(
    bg=BG
)


# =========================================================
# HEADER
# =========================================================

header = tk.Frame(
    root,
    bg=HEADER,
    height=75
)

header.pack(
    fill="x"
)

header.pack_propagate(
    False
)


# Header title
title_box = tk.Frame(
    header,
    bg=HEADER
)

title_box.pack(
    side="left",
    padx=25
)

tk.Label(
    title_box,
    text="Hospital Analysis",
    bg=HEADER,
    fg="white",
    font=("Segoe UI", 20, "bold")
).pack(
    anchor="w",
    pady=(10, 0)
)

tk.Label(
    title_box,
    text="Trusted Care for Every Stage of Life",
    bg=HEADER,
    fg="#D8F3F0",
    font=("Segoe UI", 9)
).pack(
    anchor="w"
)


# =========================================================
# NAVIGATION
# =========================================================

nav = tk.Frame(
    header,
    bg=HEADER
)

nav.pack(
    side="right",
    padx=20
)


def navigation_button(text, command):

    return tk.Button(
        nav,
        text=text,
        command=command,
        bg=HEADER,
        fg="white",
        activebackground=PRIMARY,
        activeforeground="white",
        font=("Segoe UI", 10, "bold"),
        relief="flat",
        bd=0,
        padx=13,
        pady=8,
        cursor="hand2"
    )


navigation_button(
    "Home",
    show_home
).pack(
    side="left",
    padx=2
)

navigation_button(
    "Dashboard",
    show_dashboard
).pack(
    side="left",
    padx=2
)

navigation_button(
    "About",
    show_about
).pack(
    side="left",
    padx=2
)


# =========================================================
# MAIN CONTENT
# =========================================================

content_frame = tk.Frame(
    root,
    bg=BG
)

content_frame.pack(
    fill="both",
    expand=True
)


# =========================================================
# STATUS BAR
# =========================================================

status_var = tk.StringVar(
    value="No dataset loaded"
)

status = tk.Label(
    root,
    textvariable=status_var,
    bg="#E8F0F5",
    fg=SECONDARY,
    font=("Segoe UI", 9),
    anchor="w",
    padx=15,
    pady=6
)

status.pack(
    fill="x",
    side="bottom"
)


# =========================================================
# START APPLICATION
# =========================================================

show_home()

root.mainloop()
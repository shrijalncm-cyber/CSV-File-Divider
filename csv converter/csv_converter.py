import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from pathlib import Path

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class UnifiedCSVApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("CSV Converter & Breaker Pro")
        self.geometry("850x900")
        self.resizable(True, True)
        self.minsize(750, 700)
        
        # Variables - Converter
        self.selected_file = None
        self.csv_path_var = ctk.StringVar(value="No file selected")
        self.quantity_var = ctk.StringVar(value="100")
        self.weight_var = ctk.StringVar(value="1")
        self.moq_var = ctk.StringVar(value="1")
        self.selling_unit_var = ctk.StringVar(value="Piece")
        
        # Variables - Breaker
        self.rows_per_file_var = ctk.StringVar(value="200")
        self.header_row_var = ctk.StringVar(value="1")
        self.breaker_folder_var = ctk.StringVar(value="split_files")
        
        # Mode variable
        self.mode_var = ctk.StringVar(value="convert_only")
        
        # Track converted file
        self.converted_file = None
        
        # Selling unit options
        self.selling_units = [
            "Piece", "Kilogram", "Gram", "Litre", "Millilitre",
            "Meter", "Centimeter", "Inch", "Foot", "Dozen",
            "Pair", "Bundle", "Set", "Sheet", "Roll", "Tube"
        ]
        
        # Build UI
        self.create_ui()
        
    def create_ui(self):
        """Create the modern compact UI layout"""
        
        # Main scrollable container with smooth scrolling
        self.main_container = ctk.CTkScrollableFrame(
            self,
            fg_color=("#0F172A", "#0F172A"),
            scrollbar_button_color=("#475569", "#64748B"),
            scrollbar_button_hover_color=("#64748B", "#94A3B8")
        )
        self.main_container.pack(fill="both", expand=True)
        
        # === COMPACT HEADER ===
        header_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        header_frame.pack(fill="x", padx=35, pady=(30, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="✨ CSV Pro Tools",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#F8FAFC", "#F8FAFC")
        )
        title_label.pack()
        
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="Convert • Filter • Split - All in One Place",
            font=ctk.CTkFont(size=14),
            text_color=("#94A3B8", "#CBD5E1")
        )
        subtitle_label.pack(pady=(5, 15))
        
        # Decorative line
        ctk.CTkFrame(
            header_frame,
            height=2,
            fg_color=("#8B5CF6", "#A78BFA"),
            corner_radius=10
        ).pack(fill="x", padx=180)
        
        # === MODE SELECTOR ===
        mode_card = ctk.CTkFrame(
            self.main_container,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=16,
            border_width=2,
            border_color=("#334155", "#475569")
        )
        mode_card.pack(fill="x", padx=35, pady=(0, 18))
        
        ctk.CTkLabel(
            mode_card,
            text=" Mode Selection",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#F8FAFC", "#F8FAFC")
        ).pack(anchor="w", padx=25, pady=(18, 12))
        
        mode_buttons_frame = ctk.CTkFrame(mode_card, fg_color="transparent")
        mode_buttons_frame.pack(fill="x", padx=25, pady=(0, 18))
        
        # Mode buttons
        modes = [
            ("🔄 Convert Only", "convert_only", "#3B82F6"),
            ("✂️ Break Only", "break_only", "#F59E0B"),
            ("⚡ Convert & Break", "both", "#10B981")
        ]
        
        for i, (text, value, color) in enumerate(modes):
            btn = ctk.CTkRadioButton(
                mode_buttons_frame,
                text=text,
                variable=self.mode_var,
                value=value,
                command=self.update_ui_visibility,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#E2E8F0", "#F8FAFC"),
                fg_color=color,
                hover_color=color,
                radiobutton_width=22,
                radiobutton_height=22
            )
            btn.pack(side="left", padx=(0, 25))
        
        # === FILE SELECTION ===
        file_card = self.create_card("📂 Select Your CSV File")
        file_card.pack(fill="x", padx=35, pady=(0, 18))
        
        file_display = ctk.CTkFrame(
            file_card,
            fg_color=("#0F172A", "#0F172A"),
            corner_radius=10,
            height=50
        )
        file_display.pack(fill="x", padx=25, pady=(0, 12))
        
        self.file_path_label = ctk.CTkLabel(
            file_display,
            textvariable=self.csv_path_var,
            font=ctk.CTkFont(size=12),
            text_color=("#94A3B8", "#CBD5E1"),
            anchor="w"
        )
        self.file_path_label.pack(fill="both", expand=True, padx=15, pady=12)
        
        ctk.CTkButton(
            file_card,
            text="📁 Browse Files",
            command=self.browse_file,
            height=42,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#8B5CF6", "#A78BFA"),
            hover_color=("#7C3AED", "#9333EA")
        ).pack(padx=25, pady=(0, 18))
        
        # === CONVERTER SECTION ===
        self.converter_card = self.create_card("⚙️ Product Configuration")
        self.converter_card.pack(fill="x", padx=35, pady=(0, 18))
        
        inputs_grid = ctk.CTkFrame(self.converter_card, fg_color="transparent")
        inputs_grid.pack(fill="x", padx=25, pady=(0, 18))
        
        # Compact 2-column grid
        self.create_compact_input(inputs_grid, "💯 Quantity", self.quantity_var, row=0, col=0)
        self.create_compact_input(inputs_grid, "⚖️ Weight", self.weight_var, row=0, col=1)
        self.create_compact_input(inputs_grid, "📦 MOQ", self.moq_var, row=1, col=0)
        
        # Selling unit dropdown (full width)
        unit_frame = ctk.CTkFrame(inputs_grid, fg_color="transparent")
        unit_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(12, 0))
        
        ctk.CTkLabel(
            unit_frame,
            text="📏 Selling Unit",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#E2E8F0", "#F8FAFC")
        ).pack(anchor="w", pady=(0, 6))
        
        ctk.CTkOptionMenu(
            unit_frame,
            variable=self.selling_unit_var,
            values=self.selling_units,
            width=280,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=("#0F172A", "#0F172A"),
            button_color=("#8B5CF6", "#A78BFA"),
            button_hover_color=("#7C3AED", "#9333EA")
        ).pack(anchor="w")
        
        # === BREAKER SECTION ===
        self.breaker_card = self.create_card("✂️ File Splitting Configuration")
        self.breaker_card.pack(fill="x", padx=35, pady=(0, 18))
        
        breaker_inputs = ctk.CTkFrame(self.breaker_card, fg_color="transparent")
        breaker_inputs.pack(fill="x", padx=25, pady=(0, 18))
        
        self.create_compact_input(breaker_inputs, "📄 Rows per File", self.rows_per_file_var, row=0, col=0)
        self.create_compact_input(breaker_inputs, "🔢 Header Row", self.header_row_var, row=0, col=1)
        self.create_compact_input(breaker_inputs, "📁 Output Folder", self.breaker_folder_var, row=1, col=0, colspan=2)
        
        # === INFO CARD (compact) ===
        self.info_card = ctk.CTkFrame(
            self.main_container,
            fg_color=("#1E3A5F", "#1E3A5F"),
            corner_radius=16,
            border_width=2,
            border_color=("#3B82F6", "#60A5FA")
        )
        self.info_card.pack(fill="x", padx=35, pady=(0, 18))
        
        ctk.CTkLabel(
            self.info_card,
            text="ℹ️ Auto Filters: variant_index=0 • available=TRUE",
            font=ctk.CTkFont(size=12),
            text_color=("#93C5FD", "#BFDBFE")
        ).pack(padx=25, pady=15)
        
        # === PROGRESS ===
        progress_card = ctk.CTkFrame(
            self.main_container,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=16,
            border_width=2,
            border_color=("#334155", "#475569")
        )
        progress_card.pack(fill="x", padx=35, pady=(0, 18))
        
        self.progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=12,
            corner_radius=8,
            mode="determinate",
            progress_color=("#10B981", "#34D399")
        )
        self.progress_bar.pack(fill="x", padx=25, pady=(18, 10))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_card,
            text="Ready to process",
            font=ctk.CTkFont(size=12),
            text_color=("#94A3B8", "#CBD5E1")
        )
        self.status_label.pack(padx=25, pady=(0, 18))
        
        # === PROCESS BUTTON ===
        self.process_btn = ctk.CTkButton(
            self.main_container,
            text="⚡ CONVERT NOW",
            command=self.process_all,
            height=55,
            corner_radius=12,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color=("#10B981", "#34D399"),
            hover_color=("#059669", "#10B981")
        )
        self.process_btn.pack(fill="x", padx=35, pady=(0, 35))
        
        # Initial UI state
        self.update_ui_visibility()
        
    def create_card(self, title):
        """Helper to create a card with title"""
        card = ctk.CTkFrame(
            self.main_container,
            fg_color=("#1E293B", "#1E293B"),
            corner_radius=16,
            border_width=2,
            border_color=("#334155", "#475569")
        )
        
        ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#F8FAFC", "#F8FAFC")
        ).pack(anchor="w", padx=25, pady=(18, 12))
        
        return card
    
    def create_compact_input(self, parent, label, variable, row, col, colspan=1):
        """Create compact input field in grid"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=(0, 15), pady=(0, 12))
        
        if colspan > 1:
            parent.grid_columnconfigure(0, weight=1)
        else:
            parent.grid_columnconfigure(col, weight=1)
        
        ctk.CTkLabel(
            frame,
            text=label,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=("#E2E8F0", "#F8FAFC")
        ).pack(anchor="w", pady=(0, 6))
        
        ctk.CTkEntry(
            frame,
            textvariable=variable,
            width=280 if colspan == 1 else 575,
            height=38,
            corner_radius=10,
            font=ctk.CTkFont(size=13),
            fg_color=("#0F172A", "#0F172A"),
            border_color=("#475569", "#64748B"),
            border_width=2
        ).pack(fill="x")
    
    def update_ui_visibility(self):
        """Update UI based on selected mode"""
        mode = self.mode_var.get()
        
        # Hide all first
        self.converter_card.pack_forget()
        self.breaker_card.pack_forget()
        self.info_card.pack_forget()
        
        # Get the progress card position (it's always visible)
        # We'll pack cards before it
        
        if mode == "convert_only":
            self.converter_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.info_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.process_btn.configure(
                text="⚡ CONVERT NOW",
                fg_color=("#3B82F6", "#60A5FA"),
                hover_color=("#2563EB", "#3B82F6")
            )
        
        elif mode == "break_only":
            self.breaker_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.process_btn.configure(
                text="✂️ SPLIT NOW",
                fg_color=("#F59E0B", "#FBBF24"),
                hover_color=("#D97706", "#F59E0B")
            )
        
        else:  # both
            self.converter_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.info_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.breaker_card.pack(fill="x", padx=35, pady=(0, 18), before=self.main_container.winfo_children()[-2])
            self.process_btn.configure(
                text="⚡ CONVERT & SPLIT NOW",
                fg_color=("#10B981", "#34D399"),
                hover_color=("#059669", "#10B981")
            )
    
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            display_path = file_path
            if len(display_path) > 75:
                display_path = "..." + display_path[-72:]
            self.csv_path_var.set(display_path)
            self.status_label.configure(
                text=f"✓ File selected: {Path(file_path).name}",
                text_color=("#10B981", "#34D399")
            )
    
    def validate_inputs(self):
        """Validate all user inputs"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a CSV file first!")
            return False
        
        mode = self.mode_var.get()
        
        # Validate converter inputs
        if mode in ["convert_only", "both"]:
            try:
                float(self.quantity_var.get())
                float(self.weight_var.get())
                float(self.moq_var.get())
            except ValueError:
                messagebox.showerror("Error", "Quantity, Weight, and MOQ must be valid numbers!")
                return False
        
        # Validate breaker inputs
        if mode in ["break_only", "both"]:
            try:
                rows = int(self.rows_per_file_var.get())
                if rows <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Rows per file must be a positive integer!")
                return False
            
            try:
                header = int(self.header_row_var.get())
                if header <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror("Error", "Header row must be a positive integer!")
                return False
            
            if not self.breaker_folder_var.get().strip():
                messagebox.showerror("Error", "Please provide an output folder name!")
                return False
        
        return True
    
    def process_all(self):
        """Main processing function"""
        if not self.validate_inputs():
            return
        
        mode = self.mode_var.get()
        
        try:
            self.process_btn.configure(state="disabled")
            self.progress_bar.set(0)
            self.update()
            
            if mode == "convert_only":
                self.status_label.configure(text="📖 Converting CSV...", text_color=("#3B82F6", "#60A5FA"))
                self.update()
                self.convert_csv(show_success=True)
                self.progress_bar.set(1.0)
                
            elif mode == "break_only":
                self.status_label.configure(text="✂️ Splitting CSV...", text_color=("#F59E0B", "#FBBF24"))
                self.update()
                self.split_csv(self.selected_file, show_success=True)
                self.progress_bar.set(1.0)
                
            else:  # both
                self.status_label.configure(text="📖 Step 1/2: Converting...", text_color=("#3B82F6", "#60A5FA"))
                self.update()
                converted_file = self.convert_csv(show_success=False)
                
                if converted_file:
                    self.progress_bar.set(0.5)
                    self.status_label.configure(text="✂️ Step 2/2: Splitting...", text_color=("#F59E0B", "#FBBF24"))
                    self.update()
                    self.split_csv(converted_file, show_success=True, is_final=True)
                    self.progress_bar.set(1.0)
            
            self.status_label.configure(
                text="✅ Processing complete!",
                text_color=("#10B981", "#34D399")
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_label.configure(
                text="❌ Error occurred",
                text_color=("#EF4444", "#F87171")
            )
        finally:
            self.process_btn.configure(state="normal")
    
    def convert_csv(self, show_success=True):
        """Convert and filter CSV"""
        try:
            df = pd.read_csv(self.selected_file)
            initial_rows = len(df)
            
            # Apply filters
            if 'variant_index' in df.columns:
                df = df[df['variant_index'] == 0]
            if 'available' in df.columns:
                df = df[df['available'].astype(str).str.upper().isin(['TRUE', 'T', '1', 'YES'])]
            
            filtered_rows = len(df)
            
            if filtered_rows == 0:
                messagebox.showwarning("No Data", "No rows matched the filter criteria!")
                return None
            
            # Create output DataFrame with exact column names as specified
            output_df = pd.DataFrame({
                'productName': df['product_title'].values if 'product_title' in df.columns else [''] * len(df),
                'productSku': [''] * len(df),
                'sellingPrice': df['price'].values if 'price' in df.columns else [''] * len(df),
                'crossed_price': df['crossed_price'].values if 'crossed_price' in df.columns else [''] * len(df),
                'quantity': [self.quantity_var.get()] * len(df),
                'weight': [self.weight_var.get()] * len(df),
                'productDescription': [''] * len(df),
                'moq': [self.moq_var.get()] * len(df),
                'sellingUnit': [self.selling_unit_var.get()] * len(df),
                'image_temp1': df['image_1'].values if 'image_1' in df.columns else [''] * len(df),
                'image_temp2': df['image_2'].values if 'image_2' in df.columns else [''] * len(df),
                'image_temp3': df['image_3'].values if 'image_3' in df.columns else [''] * len(df)
            })
            
            # Rename image columns to all have the same name 'image'
            output_df.columns = [
                'productName', 'productSku', 'sellingPrice', 'crossed_price',
                'quantity', 'weight', 'productDescription', 'moq', 'sellingUnit',
                'image', 'image', 'image'
            ]
            
            input_path = Path(self.selected_file)
            output_file = input_path.parent / f"{input_path.stem}_converted.csv"
            
            # Explicitly write with headers
            output_df.to_csv(output_file, index=False, header=True)
            
            if show_success:
                messagebox.showinfo(
                    "✅ Success!",
                    f"Converted: {initial_rows} → {filtered_rows} rows\n"
                    f"Skipped: {initial_rows - filtered_rows} rows\n\n"
                    f"📁 {output_file.name}"
                )
            
            return output_file
            
        except KeyError as e:
            messagebox.showerror("Error", f"Missing column: {str(e)}")
            return None
    
    def split_csv(self, file_path, show_success=True, is_final=False):
        """Split CSV into multiple files"""
        try:
            rows_per_file = int(self.rows_per_file_var.get())
            header_row_num = int(self.header_row_var.get()) - 1
            folder_name = self.breaker_folder_var.get().strip()
            
            df = pd.read_csv(file_path, header=None)
            
            if header_row_num >= len(df):
                messagebox.showerror("Error", f"Header row exceeds file length!")
                return
            
            header = df.iloc[header_row_num]
            data_rows = df[df.index != header_row_num]
            
            output_dir = Path(file_path).parent / folder_name
            output_dir.mkdir(exist_ok=True)
            
            num_files = (len(data_rows) + rows_per_file - 1) // rows_per_file
            
            for i in range(num_files):
                start_idx = i * rows_per_file
                end_idx = min((i + 1) * rows_per_file, len(data_rows))
                
                chunk = data_rows.iloc[start_idx:end_idx]
                output_df = pd.concat([pd.DataFrame([header]), chunk], ignore_index=True)
                
                output_file = output_dir / f"Bulk upload {i + 1}.csv"
                output_df.to_csv(output_file, index=False, header=False)
            
            if show_success:
                msg = f"✂️ Split into {num_files} files\n📁 {folder_name}/"
                if is_final:
                    msg = f"✅ Converted & split!\n📂 {num_files} files in {folder_name}/"
                messagebox.showinfo("Success!", msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error splitting:\n{str(e)}")


def main():
    """Main entry point"""
    app = UnifiedCSVApp()
    app.mainloop()


if __name__ == "__main__":
    main()

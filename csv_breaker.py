import customtkinter as ctk
from tkinter import filedialog, messagebox
import pandas as pd
import os
from pathlib import Path

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CSVBreakerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("CSV Breaker")
        self.geometry("700x750")
        self.resizable(False, False)
        
        # Variables
        self.selected_file = None
        self.csv_path_var = ctk.StringVar(value="No file selected")
        self.rows_per_file_var = ctk.StringVar(value="1000")
        self.header_row_var = ctk.StringVar(value="1")
        self.folder_name_var = ctk.StringVar(value="output")
        
        # Build UI
        self.create_ui()
        
    def create_ui(self):
        """Create the modern UI layout"""
        
        # Main container
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 CSV Breaker",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Split large CSV files into smaller chunks",
            font=ctk.CTkFont(size=14),
            text_color=("#666666", "#999999")
        )
        subtitle_label.pack(pady=(0, 30))
        
        # File Selection Section
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.pack(fill="x", pady=(0, 20))
        
        file_label = ctk.CTkLabel(
            file_frame,
            text="Select CSV File",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        file_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # File path display
        self.file_path_label = ctk.CTkLabel(
            file_frame,
            textvariable=self.csv_path_var,
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#AAAAAA"),
            anchor="w"
        )
        self.file_path_label.pack(fill="x", padx=20, pady=(0, 10))
        
        # Browse button
        browse_btn = ctk.CTkButton(
            file_frame,
            text="📁 Browse File",
            command=self.browse_file,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color=("#3B8ED0", "#1F6AA5"),
            hover_color=("#2B7FC0", "#0F5A95")
        )
        browse_btn.pack(padx=20, pady=(0, 20))
        
        # Configuration Section
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill="x", pady=(0, 20))
        
        config_label = ctk.CTkLabel(
            config_frame,
            text="Configuration",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        config_label.pack(anchor="w", padx=20, pady=(20, 15))
        
        # Rows per file
        rows_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        rows_container.pack(fill="x", padx=20, pady=(0, 15))
        
        rows_label = ctk.CTkLabel(
            rows_container,
            text="Rows per file:",
            font=ctk.CTkFont(size=14)
        )
        rows_label.pack(side="left", padx=(0, 15))
        
        rows_entry = ctk.CTkEntry(
            rows_container,
            textvariable=self.rows_per_file_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        rows_entry.pack(side="left")
        
        # Header row number
        header_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        header_container.pack(fill="x", padx=20, pady=(0, 15))
        
        header_label = ctk.CTkLabel(
            header_container,
            text="Header row number:",
            font=ctk.CTkFont(size=14)
        )
        header_label.pack(side="left", padx=(0, 15))
        
        header_entry = ctk.CTkEntry(
            header_container,
            textvariable=self.header_row_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        header_entry.pack(side="left")
        
        # Output folder name
        folder_container = ctk.CTkFrame(config_frame, fg_color="transparent")
        folder_container.pack(fill="x", padx=20, pady=(0, 20))
        
        folder_label = ctk.CTkLabel(
            folder_container,
            text="Output folder name:",
            font=ctk.CTkFont(size=14)
        )
        folder_label.pack(side="left", padx=(0, 15))
        
        folder_entry = ctk.CTkEntry(
            folder_container,
            textvariable=self.folder_name_var,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13)
        )
        folder_entry.pack(side="left")
        
        # Progress Section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=(0, 20))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=10,
            mode="determinate"
        )
        self.progress_bar.pack(fill="x", padx=20, pady=(20, 10))
        self.progress_bar.set(0)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Ready to process",
            font=ctk.CTkFont(size=12),
            text_color=("#888888", "#AAAAAA")
        )
        self.status_label.pack(padx=20, pady=(0, 20))
        
        # Process Button
        self.process_btn = ctk.CTkButton(
            main_frame,
            text="⚡ Process CSV",
            command=self.process_csv,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#10B981", "#059669"),
            hover_color=("#0A9F6E", "#047857")
        )
        self.process_btn.pack(fill="x", pady=(0, 10))
        
    def browse_file(self):
        """Open file dialog to select CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self.selected_file = file_path
            # Show shortened path if too long
            display_path = file_path
            if len(display_path) > 60:
                display_path = "..." + display_path[-57:]
            self.csv_path_var.set(display_path)
            self.status_label.configure(text=f"File selected: {Path(file_path).name}")
    
    def validate_inputs(self):
        """Validate all user inputs"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select a CSV file first!")
            return False
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Error", "Selected file does not exist!")
            return False
        
        # Validate rows per file
        try:
            rows_per_file = int(self.rows_per_file_var.get())
            if rows_per_file <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Rows per file must be a positive integer!")
            return False
        
        # Validate header row
        try:
            header_row = int(self.header_row_var.get())
            if header_row <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Header row must be a positive integer!")
            return False
        
        # Validate folder name
        folder_name = self.folder_name_var.get().strip()
        if not folder_name:
            messagebox.showerror("Error", "Please provide an output folder name!")
            return False
        
        # Check for invalid characters in folder name
        invalid_chars = '<>:"/\\|?*'
        if any(char in folder_name for char in invalid_chars):
            messagebox.showerror("Error", f"Folder name contains invalid characters: {invalid_chars}")
            return False
        
        return True
    
    def process_csv(self):
        """Main processing function to split CSV"""
        if not self.validate_inputs():
            return
        
        try:
            # Disable button during processing
            self.process_btn.configure(state="disabled", text="Processing...")
            self.progress_bar.set(0)
            self.update()
            
            # Get parameters
            rows_per_file = int(self.rows_per_file_var.get())
            header_row_num = int(self.header_row_var.get()) - 1  # Convert to 0-indexed
            folder_name = self.folder_name_var.get().strip()
            
            # Update status
            self.status_label.configure(text="Reading CSV file...")
            self.update()
            
            # Read the CSV file
            df = pd.read_csv(self.selected_file, header=None)
            
            # Validate header row number
            if header_row_num >= len(df):
                messagebox.showerror("Error", f"Header row {header_row_num + 1} exceeds file length ({len(df)} rows)!")
                return
            
            # Extract header
            header = df.iloc[header_row_num]
            
            # Remove header row from data
            data_rows = df[df.index != header_row_num]
            
            # Create output directory
            output_dir = Path(self.selected_file).parent / folder_name
            output_dir.mkdir(exist_ok=True)
            
            # Calculate number of files needed
            num_files = (len(data_rows) + rows_per_file - 1) // rows_per_file
            
            self.status_label.configure(text=f"Creating {num_files} files...")
            self.update()
            
            # Split and save
            for i in range(num_files):
                start_idx = i * rows_per_file
                end_idx = min((i + 1) * rows_per_file, len(data_rows))
                
                # Get chunk
                chunk = data_rows.iloc[start_idx:end_idx]
                
                # Create DataFrame with header
                output_df = pd.concat([pd.DataFrame([header]), chunk], ignore_index=True)
                
                # Save to file
                output_file = output_dir / f"Bulk upload {i + 1}.csv"
                output_df.to_csv(output_file, index=False, header=False)
                
                # Update progress
                progress = (i + 1) / num_files
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Processing file {i + 1} of {num_files}...")
                self.update()
            
            # Success
            self.progress_bar.set(1.0)
            self.status_label.configure(
                text=f"✅ Success! Created {num_files} files in '{folder_name}' folder",
                text_color=("#10B981", "#059669")
            )
            
            messagebox.showinfo(
                "Success",
                f"CSV file split successfully!\n\n"
                f"Created {num_files} files in:\n{output_dir}\n\n"
                f"Files named: Bulk upload 1.csv to Bulk upload {num_files}.csv"
            )
            
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "The CSV file is empty!")
        except pd.errors.ParserError as e:
            messagebox.showerror("Error", f"Error parsing CSV file:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
            self.status_label.configure(
                text="❌ Error occurred during processing",
                text_color=("#EF4444", "#DC2626")
            )
        finally:
            # Re-enable button
            self.process_btn.configure(state="normal", text="⚡ Process CSV")


def main():
    """Main entry point"""
    app = CSVBreakerApp()
    app.mainloop()


if __name__ == "__main__":
    main()

import os
import shutil
import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog

class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.current_path = os.getcwd()
        self.previous_paths = [self.current_path]  # Initialize with current path

        self.create_widgets()

    def create_widgets(self):
    # Set the default font to Courier and embolden all text
        default_font = ("Courier", 10, "bold")

        self.navigation_frame = tk.Frame(self.root, bg="black", highlightbackground="black", highlightthickness=1)  
        self.navigation_frame.pack(side=tk.TOP, fill=tk.X)

        self.back_button = tk.Button(self.navigation_frame, text="Back", command=self.navigate_back, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.back_button.pack(side=tk.LEFT)

        self.current_folder_label = tk.Label(self.navigation_frame, text="Current Folder:", font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.current_folder_label.pack(side=tk.LEFT)

        self.current_folder_entry = tk.Entry(self.navigation_frame, width=10, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.current_folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.file_listbox = tk.Listbox(self.root, width=70, height=20, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")
        self.file_listbox.pack(fill=tk.X, expand=True)

        # Bind double click event to listbox items
        self.file_listbox.bind("<Double-Button-1>", self.double_click_event)

        self.buttons_frame = tk.Frame(self.root, bg="black", highlightbackground="black", highlightthickness=1)  
        self.buttons_frame.pack()

        self.create_directory_button = tk.Button(self.buttons_frame, text="Create Directory", command=self.create_directory, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")
        self.create_directory_button.pack(side=tk.LEFT)

        self.move_button = tk.Button(self.buttons_frame, text="Move", command=self.move_file, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")
        self.move_button.pack(side=tk.LEFT)

        # Expand and fill options to stretch the buttons horizontally
        self.refresh_button = tk.Button(self.buttons_frame, text="Refresh", command=self.refresh_files, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.refresh_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.rename_button = tk.Button(self.buttons_frame, text="Rename", command=self.rename_file, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.rename_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.copy_button = tk.Button(self.buttons_frame, text="Copy", command=self.copy_file, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black") 
        self.copy_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.delete_button = tk.Button(self.buttons_frame, text="Delete", command=self.delete_file, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black") 
        self.delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.create_button = tk.Button(self.buttons_frame, text="Create File", command=self.create_file, font=default_font, bg="black", fg="#D3D3D3", highlightbackground="black")  
        self.create_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.refresh_files()



    def refresh_files(self):
        self.file_listbox.delete(0, tk.END)
        for file in os.listdir(self.current_path):
            if os.path.isdir(os.path.join(self.current_path, file)):
                self.file_listbox.insert(tk.END, file)
                self.file_listbox.itemconfig(tk.END, {'fg': '#1E90FF'}) # Set text color to blue for directories
            else:
                self.file_listbox.insert(tk.END, file)
                self.file_listbox.itemconfig(tk.END, {'fg': '#D3D3D3'})  
        # Update the current folder entry
        self.current_folder_entry.delete(0, tk.END)
        self.current_folder_entry.insert(0, self.current_path)


    def double_click_event(self, event):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            if os.path.isdir(os.path.join(self.current_path, selected_file)):
                self.previous_paths.append(self.current_path)
                self.current_path = os.path.join(self.current_path, selected_file)
                self.refresh_files()

    def navigate_back(self):
        parent_directory = os.path.dirname(self.current_path)
        if parent_directory and parent_directory != self.current_path:  # Ensure not at root or initial directory
            self.current_path = parent_directory
            self.refresh_files()
        else:
            print("Already at the root directory.")

    def rename_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            new_name = simpledialog.askstring("Rename File", "Enter new name for {}:".format(selected_file))
            if new_name:
                try:
                    os.rename(os.path.join(self.current_path, selected_file), os.path.join(self.current_path, new_name))
                    self.refresh_files()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def copy_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            destination_folder = filedialog.askdirectory(title="Select Destination Folder")
            if destination_folder:
                try:
                    shutil.copy(os.path.join(self.current_path, selected_file), destination_folder)
                    self.refresh_files()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def delete_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            file_path = os.path.join(self.current_path, selected_file)
            if os.path.isdir(file_path):
                confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the directory {} and its contents?".format(selected_file))
                if confirmation:
                    try:
                        shutil.rmtree(file_path)
                        self.refresh_files()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            else:
                confirmation = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete {}?".format(selected_file))
                if confirmation:
                    try:
                        os.remove(file_path)
                        self.refresh_files()
                    except Exception as e:
                        messagebox.showerror("Error", str(e))

    def create_file(self):
        new_file_name = simpledialog.askstring("Create File", "Enter name for the new file:")
        if new_file_name:
            try:
                with open(os.path.join(self.current_path, new_file_name), 'w'):
                    pass
                self.refresh_files()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def create_directory(self):
        new_directory_name = simpledialog.askstring("Create Directory", "Enter name for the new directory:")
        if new_directory_name:
            try:
                os.mkdir(os.path.join(self.current_path, new_directory_name))
                self.refresh_files()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def move_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            source_file = os.path.join(self.current_path, selected_file)
            destination_folder = filedialog.askdirectory(title="Select Destination Folder")
            if destination_folder:
                try:
                    shutil.move(source_file, destination_folder)
                    self.refresh_files()
                except Exception as e:
                    messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorerApp(root)
    root.mainloop()

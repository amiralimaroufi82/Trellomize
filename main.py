import tkinter as tk
import argparse

class AdminInfoInput:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Information")
        self.root.geometry("300x150")

        self.username_label = tk.Label(root, text="Username:")
        self.username_entry = tk.Entry(root)
        self.password_label = tk.Label(root, text="Password:")
        self.password_entry = tk.Entry(root, show="*")

        self.ok_button = tk.Button(root, text="OK", command=self.get_admin_info)

        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        self.ok_button.grid(row=2, column=0, columnspan=2, pady=10)

    def get_admin_info(self):
        username = self.username_entry.get()
        password = self.password_entry.get()


        print(f"Admin username: {username}")
        print(f"Admin password: {password}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminInfoInput(root)
    root.mainloop()

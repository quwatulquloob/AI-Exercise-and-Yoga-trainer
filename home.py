import tkinter as tk
from PIL import Image, ImageTk  # Import PIL modules for image handling
import subprocess
import sys


class Home:
    def __init__(self, root):
        self.root = root
        self.root.title("Physiotherapist Trainer Home page")
        self.root.geometry("1280x700")

        # Load the background image
        self.original_image = Image.open("screens/homebg.png")
        self.update_background()

        # Button setup
        self.signup_button = tk.Button(root, text="Signup", font=("Arial", 17, 'bold'), fg="white", bg="#2b1ae0",
                                       highlightcolor="#000000", highlightbackground="#000000",
                                       highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_signup)
        self.signup_button.place(relx=0.75, rely=0.45, width=200, height=50)

        self.signin_button = tk.Button(root, text="Signin", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                       highlightcolor="#000000", highlightbackground="#000000",
                                       highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_signin)
        self.signin_button.place(relx=0.75, rely=0.55, width=200, height=50)

        # Bind the resize event
        self.root.bind("<Configure>", self.on_resize)

        self.title_label = tk.Label(root, text="Physiotherapist Trainer", font=("Arial", 24, 'bold'), bg="#ffffff")
        self.title_label.place(relx=0.5, rely=0.05, anchor='n')

    def update_background(self):
        # Resize the image to fit the window size
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        resized_image = self.original_image.resize((window_width, window_height), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Update the label with the resized image
        if hasattr(self, 'background_label'):
            self.background_label.config(image=self.background_image)
        else:
            self.background_label = tk.Label(self.root, image=self.background_image)
            self.background_label.place(relwidth=1, relheight=1)

    def on_resize(self, event):
        # Update background image on window resize
        self.update_background()

    def run_signup(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'signup.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run_signin(self):
        self.root.destroy()
        try:
            # Execute the signin.py script
            subprocess.run([sys.executable, 'signin.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signin script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Home(root)
    root.mainloop()

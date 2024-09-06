import tkinter as tk
from tkinter import PhotoImage
import subprocess
# from signup import login_page
from AudioCommSys import text_to_speech
from Exercises import simulate_target_exercies
import sys
global z
import json
import yagmail
# from signin import *
import sys
import json

if len(sys.argv) > 1:
    user_data_json = sys.argv[1]
    user_data = json.loads(user_data_json)
    print(f"Received user data: {user_data}")
else:
    user_data = [0, "", "", ""]


class WorkoutAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Physiotherapist Trainer")
        self.root.geometry("1200x700")
        self.background_image = PhotoImage(file="screens/1.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.yoga_button = tk.Button(root, text="Yoga Trainer", font=("Arial", 19, 'bold'), fg="white", bg="#da2626",
                                     highlightcolor="#da2626", highlightbackground="#da2626", highlightthickness="1",
                                     bd="0", relief=tk.SUNKEN, command=self.run_yoga_trainer)
        self.yoga_button.place(relx=0.665, rely=0.80, width=205, height=55)

        self.pain_button = tk.Button(root, text="Physiotherapy exercises", font=("Arial", 17, 'bold'), fg="white",
                                     bg="#000000", highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.show_physio_screen)
        self.pain_button.place(relx=0.36, rely=0.80, width=288, height=55)

        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                       highlightcolor="#000000", highlightbackground="#000000",
                                       highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.18, rely=0.80, width=130, height=55)


    def run_yoga_trainer(self):
        import os  # Import the required module here

        # Read the script code from "webcam_pose.py"
        with open("webcam_pose.py", "r") as script_file:
            script_code = script_file.read()

        # Create a globals dictionary that includes the necessary modules
        script_globals = globals().copy()
        script_globals['os'] = os  # Add 'os' to the globals dictionary

        # Execute the script code with the modified globals
        exec(script_code, script_globals)

    def run_signup(self):
        root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'signup.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run_home(self):
        root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def run_signin(self):
        root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'signin.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    def show_physio_screen(self):
        self.background_image = None
        self.root.update()
        self.root.destroy()

        physio_screen = tk.Tk()
        PhysioScreen(physio_screen)
        physio_screen.mainloop()

    def show_exercisepain_screen(self):
        self.background_image = None
        self.root.destroy()

        next_screen = tk.Tk()
        nexts_screen(next_screen)
        next_screen.mainloop()

    # def show_ExerciseGUI(self):
    #     self.background_image = None
    #     if hasattr(self, 'root') and self.root is not None:
    #         self.root.destroy()
    #
    #     exercise_gui = tk.Tk()
    #     ExerciseGUI(exercise_gui)
    #     exercise_gui.mainloop()

class PhysioScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Physiotherapist Trainer")
        self.root.geometry("1280x700")

        self.background_image = PhotoImage(file="screens/2.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)


        self.next_button = tk.Button(root, text="Next",font=("Arial", 21),fg ="white", bg= "#4b60cd", highlightcolor="#4b60cd",highlightbackground="#4b60cd", highlightthickness="1",bd="0",relief=tk.SUNKEN, command=self.show_pain_level_screen)
        self.next_button.place(relx=0.3223, rely=0.82, relwidth=0.170, relheight=0.075)
        self.next_button.place(x=350, y=1)

        self.back_button = tk.Button(root, text="Back", fg="white", font=("Arial", 19), bg="#000000",
                                     highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                     bd="0", relief=tk.SUNKEN, command=self.show_WorkoutAPPGUI)
        self.back_button.place(relx=0.35, rely=0.82, relwidth=0.150, relheight=0.075)

        self.root.after(50, self.play_audio)

        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.12, rely=0.82,  relwidth=0.150,  relheight=0.075)



    def play_audio(self):
            # Your text-to-speech implementation here
            ins = "Where are you feeling pain"
            text_to_speech(ins)

    def show_pain_level_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()

        pain_level_screen = tk.Tk()
        PainLevelScreen(pain_level_screen)
        pain_level_screen.mainloop()

    def show_WorkoutAPPGUI(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()

        WorkoutAPP_GUI = tk.Tk()
        WorkoutAppGUI(WorkoutAPP_GUI)
        WorkoutAPP_GUI.mainloop()

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


class PainLevelScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Pain Level")
        self.root.geometry("1280x700")

        self.background_image = PhotoImage(file="screens/3.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.low_button = tk.Button(root, text="Low", font=("Arial", 19), fg="white", bg="#8388a6",
                                    highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                    bd="0", relief=tk.SUNKEN, command=lambda: self.show_next_screen("Low"))
        self.low_button.place(relx=0.725, rely=0.85, relwidth=0.15, relheight=0.059)


        self.medium_button = tk.Button(root, text="Medium", font=("Arial", 19), fg="white", bg="#dc0505",
                                       highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                       bd="0", relief=tk.SUNKEN, command=lambda: self.show_next_screen("Medium"))
        self.medium_button.place(relx=0.53, rely=0.66, relwidth=0.15, relheight=0.069, x=250, y=50)

        self.high_button = tk.Button(root, text="High", font=("Arial", 19), fg="white", bg="#4b60cd",
                                     highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                     bd="0", relief=tk.SUNKEN, command=lambda: self.show_next_screen("High"))
        self.high_button.place(relx=0.53, rely=0.52, relwidth=0.15, relheight=0.070, x=250, y=50)

        self.back_button = tk.Button(root, text="Back", fg="white", font=("Arial", 19), bg="#000000",
                                     highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                     bd="0", relief=tk.SUNKEN, command=self.show_physio_screen)
        self.back_button.place(relx=0.13, rely=0.85, relwidth=0.150, relheight=0.069)

        self.root.after(50, self.play_audio)
        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.38, rely=0.85, width=178, height=49)


    def play_audio(self):
            # Your text-to-speech implementation here
            ins = "How much your feeling pain"
            text_to_speech(ins)

    def show_physio_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        physio_screen = tk.Tk()
        PhysioScreen(physio_screen)
        physio_screen.mainloop()

    def show_next_screen(self, pain_level):
        self.back_screeground_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        next_screen = tk.Tk()
        Screen7(next_screen, pain_level)
        next_screen.mainloop()

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

class Screen7:
    def __init__(self, root, pain_level):
        self.root = root
        self.root.title("Pain experiencing")
        self.root.geometry("1280x700")
        self.pain_level = pain_level

        self.background_image = PhotoImage(file="screens/8.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.button_1_month = tk.Button(root, text="1 Month", font=("Arial", 19), fg="white", bg="#4b60cd",
                                        highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                        bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("1 Month"))
        self.button_1_month.place(relx=0.685, rely=0.16, relwidth=0.15, relheight=0.070)

        self.button_2_months = tk.Button(root, text="2 Months", font=("Arial", 19), fg="white", bg="#68bb4a",
                                         highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                         bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("2 Months"))
        self.button_2_months.place(relx=0.688, rely=0.3, relwidth=0.15, relheight=0.070)

        self.button_3_months = tk.Button(root, text="3 Months", font=("Arial", 19), fg="white", bg="#6d749d",
                                         highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                         bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("3 Months"))
        self.button_3_months.place(relx=0.688, rely=0.44, relwidth=0.15, relheight=0.070)

        self.button_4_months = tk.Button(root, text="4 Months", font=("Arial", 19), fg="white", bg="#389c36",
                                         highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                         bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("4 Months"))
        self.button_4_months.place(relx=0.688, rely=0.57, relwidth=0.15, relheight=0.070)

        self.button_5_months = tk.Button(root, text="5 Months", font=("Arial", 19), fg="white", bg="#dc0505",
                                         highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                         bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("5 Months"))
        self.button_5_months.place(relx=0.688, rely=0.71, relwidth=0.15, relheight=0.070)

        self.button_6_months = tk.Button(root, text="6 Months", font=("Arial", 19), fg="white", bg="#8388a6",
                                         highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                         bd="0", relief=tk.SUNKEN, command=lambda: self.show_painperiod_screen("6 Months"))
        self.button_6_months.place(relx=0.688, rely=0.84, relwidth=0.15, relheight=0.070)

        self.back_button = tk.Button(root, text="Back", fg=("white"), font=("Arial", 23), bg="#000000",
                                     highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                     bd="0", relief=tk.SUNKEN, command=self.show_pain_level_screen)
        self.back_button.place(relx=0.13, rely=0.83, relwidth=0.12, relheight=0.070)

        self.root.after(50, self.play_audio)
        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.35, rely=0.83, width=129, height=50)

    def play_audio(self):
        # Your text-to-speech implementation here
        ins = "How long your feeling pain"
        text_to_speech(ins)

    def show_pain_level_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        pain_level_screen = tk.Tk()
        PainLevelScreen(pain_level_screen)
        pain_level_screen.mainloop()

    def show_painperiod_screen(self, duration):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        next_screen = tk.Tk()
        Screen8(next_screen, self.pain_level, duration)
        next_screen.mainloop()

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
class Screen8:
    def __init__(self, root,pain_level, duration):
        self.root = root
        self.pain_level = pain_level
        self.root.title("Person type")
        self.root.geometry("1280x700")
        self.duration = duration
        self.background_image = PhotoImage(file="screens/9.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.button_injured = tk.Button(root, text="Injured person", font=("Arial", 18), fg="white", bg="#4b60cd",
                                        highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                        bd="0", relief=tk.SUNKEN,
                                        command=lambda: self.show_exercisepain_screen("Injured person"))
        self.button_injured.place(relx=0.73, rely=0.58, relwidth=0.150, relheight=0.078)

        self.button_normal = tk.Button(root, text="Normal person", font=("Arial", 19), fg="white", bg="#dc0505",
                                       highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                       bd="0", relief=tk.SUNKEN,
                                       command=lambda: self.show_exercisepain_screen("Normal person"))
        self.button_normal.place(relx=0.73, rely=0.715, relwidth=0.150, relheight=0.080)

        self.button_athlete = tk.Button(root, text="Athlete", font=("Arial", 19), fg="white", bg="#8388a6",
                                        highlightcolor="#4b60cd", highlightbackground="#4b60cd", highlightthickness="1",
                                        bd="0", relief=tk.SUNKEN,
                                        command=lambda: self.show_exercisepain_screen("Athlete"))
        self.button_athlete.place(relx=0.73, rely=0.837, relwidth=0.150, relheight=0.080)

        self.back_button = tk.Button(root, text="Back", font=("Arial", 23), fg="white",
                                     bg="#000000", highlightcolor="#4b60cd", highlightbackground="#4b60cd",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.show_next_screen)
        self.back_button.place(relx=0.110, rely=0.85, relwidth=0.140, relheight=0.075)

        self.root.after(50, self.play_audio)
        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.330, rely=0.82, width=130, height=60)

    def play_audio(self):
        # Your text-to-speech implementation here
        ins = "What is your status"
        text_to_speech(ins)

    def show_next_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        next_screen = tk.Tk()
        Screen7(next_screen, self.pain_level)  # Pass the pain level to the next screen
        next_screen.mainloop()

    def show_exercisepain_screen(self, status):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        next_screen = tk.Tk()
        Screen9(next_screen, self.pain_level, self.duration, status)  # Pass the pain level, duration, and status
        next_screen.mainloop()

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
class Screen9:
    def __init__(self, root, pain_level, duration, status):
        self.root = root
        self.pain_level = pain_level
        self.duration = duration
        self.status = status
        self.root.title("Enter Weight and Height")
        self.root.geometry("1280x700")

        self.background_image = PhotoImage(file="screens/11.png")  # Replace with your image
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.weight_label = tk.Label(root, text="Enter Weight in kg ", font=("Arial", 13,'bold'), fg="#FF6EC7", bg="WHITE")
        self.weight_label.place(relx=0.708, rely=0.4, relwidth=0.15, relheight=0.1)

        self.weight_entry = tk.Entry(root, font=("Arial", 20, 'bold'),highlightcolor="black",highlightthickness="2")
        self.weight_entry.place(relx=0.725, rely=0.5, relwidth=0.1, relheight=0.05)

        self.height_label = tk.Label(root, text="Enter Height (f): ", font=("Arial", 13,'bold'), fg="#FF6EC7", bg="WHITE")
        self.height_label.place(relx=0.725, rely=0.6, relwidth=0.1, relheight=0.02)

        self.height_entry = tk.Entry(root, font=("Arial", 20 ,'bold'),highlightcolor="black",highlightthickness="2")
        self.height_entry.place(relx=0.725, rely=0.7, relwidth=0.1, relheight=0.05)

        self.calculate_bmi_button = tk.Button(root, text="Calculate BMI", font=("Arial", 15,'bold'), fg="#FF6EC7", bg="white",
                                              highlightcolor="#FF6EC7", highlightbackground="#FF6EC7",
                                              highlightthickness="2", bd="0", relief=tk.SUNKEN,
                                              command=self.calculate_bmi)
        self.calculate_bmi_button.place(relx=0.725, rely=0.8, relwidth=0.1, relheight=0.05)

        self.back_button = tk.Button(root, text="Back", font=("Arial", 30, 'bold'), fg="#FF6EC7",
                                     bg="gray", highlightcolor="#FF6EC7", highlightbackground="#FF6EC7",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.show_previous_screen)
        self.back_button.place(relx=0.15, rely=0.82, relwidth=0.100, relheight=0.09)

        self.root.after(50, self.play_audio)
        self.home_button = tk.Button(root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        self.home_button.place(relx=0.35, rely=0.65, relwidth=0.130, relheight=0.09)

    def play_audio(self):
        # Your text-to-speech implementation here
        ins = "Get you BMI."
        text_to_speech(ins)

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / ((height*0.3048) ** 2)
            self.show_next_screen(bmi)
        except ValueError:
            # Handle the case where the input is not a valid number
            print("Invalid input. Please enter valid numbers for weight and height.")

    def show_previous_screen(self):
        # self.background_image = None
        # if hasattr(self, 'root') and self.root is not None:
        self.root.destroy()
        next_screen = tk.Tk()
        Screen8(next_screen, self.pain_level, self.duration)  # Pass the pain level and duration to the previous screen
        next_screen.mainloop()

    def show_next_screen(self, bmi):
        # Determine BMI category
        if bmi < 18.5:
            bmi_category = "Underweight"
        elif 18.5 <= bmi <= 25:
            bmi_category = "Normal Weight"
        elif 25 <= bmi <= 30:
            bmi_category = "Overweight"
        else:
            bmi_category = "Obese"
        print(bmi)
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
         self.root.destroy()
        next_screen = tk.Tk()
        # Pass the pain level, duration, status, BMI, and BMI category to the nexts_screen
        nexts_screen(next_screen, self.pain_level, self.duration, self.status, bmi, bmi_category,user_data)
        next_screen.mainloop()

class nexts_screen:
    def __init__(self, root,duration, status, pain_level,bmi,bmi_category,user_data):
        self.root = root
        self.root.title("Exercise Simulationsr")
        self.root.geometry("1280x700")

        self.background_image = PhotoImage(file="screens/1.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        self.exercise_var1 = tk.StringVar(value="Select exercise")

        # Automatically set difficulty level based on status, pain level, and bmi_category
        self.difficulty_var = tk.StringVar(value=self.calculate_difficulty(status, pain_level, duration, bmi_category))


        # Additional attributes
        self.duration = duration
        self.status = status
        self.pain_level = pain_level
        self.bmi_category = bmi_category
        self.user_data = user_data


        self.create_widgets()


    def calculate_difficulty(self, status, pain_level, duration, bmi_category):
        difficulty_mapping = {"easy": 8, "medium": 9, "hard": 12, "other": 6}
        print(status)
        print(duration)
        print(pain_level)

        if status == "1 Months" and pain_level == "Normal person" and duration == "Low" and bmi_category == "Under weight":
            return difficulty_mapping["hard"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "Low" and bmi_category == "Normal Weight":
            return difficulty_mapping["Hard"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "Low" and bmi_category == "Over Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Noraml person" and duration == "Low" and bmi_category == "Obese ":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "Medium" and bmi_category == "Normal Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "Medium" and bmi_category == "Over Weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Noraml person" and duration == "Medium" and bmi_category == "Under weight":
            return difficulty_mapping["hard"]
        elif status == "1 Months" and pain_level == "Noraml person" and duration == "Medium" and bmi_category == "Obese ":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "High" and bmi_category == "Normal Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Normal person" and duration == "High" and bmi_category == "Over Weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Noraml person" and duration == "High" and bmi_category == "Under weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Noraml person" and duration == "High" and bmi_category == "Obese ":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Injured person" and duration == "High" and bmi_category == "Normal Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Injured person" and duration == "High" and bmi_category == "Over Weight":
            return difficulty_mapping["easy "]
        elif status == "1 Months" and pain_level == "Injured person" and duration == "High" and bmi_category == "Under weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Injured person" and duration == "High" and bmi_category == "Obese ":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Athlete" and duration == "High" and bmi_category == "Normal Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Athlete" and duration == "High" and bmi_category == "Over Weight":
            return difficulty_mapping["medium"]
        elif status == "1 Months" and pain_level == "Athlete" and duration == "High" and bmi_category == "Under weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months" and pain_level == "Athlete" and duration == "High" and bmi_category == "Obese ":
            return difficulty_mapping["easy"]
        elif status == "1 Months"or "2 Months"or "3 Months" or "4 Months" or "5 Months" or "6 Months" and pain_level == "Athlete" or "Normal person"or "Injured person" and duration=="High" or "Low" or "medium" and bmi_category =="Obese":
            return difficulty_mapping["easy"]
        elif status == "1 Months"or "2 Months"or "3 Months" or "4 Months" or "5 Months" or "6 Months" and pain_level == "Injured person" and duration=="High" or "Low" or "medium" and bmi_category =="Obese" or "Under weight"or "Over Weight" or "Normal Weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months"or "2 Months"or "3 Months" or "4 Months" or "5 Months" or "6 Months" and pain_level == "Injured person" and duration=="High" and bmi_category =="Obese" or "Under weight"or "Over Weight" or "Normal Weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months"or "2 Months"or "3 Months" or "4 Months" or "5 Months" or "6 Months" and pain_level == "Athlete" and duration=="High"or "medium" or "Low" and bmi_category =="Obese" or "Over Weight":
            return difficulty_mapping["easy"]
        elif status == "1 Months"or "2 Months"or "3 Months" or "4 Months" or "5 Months" or "6 Months" and pain_level == "Athlete" and duration=="High" and bmi_category =="Under weight" or "Normal Weight":
            return difficulty_mapping["easy"]
        elif status == "6 Months" and pain_level == "Athlete" or "Normal person" or "Injured person" and duration=="High" or "Low" or "medium" and bmi_category =="Under weight" or "Normal Weight" or "Obese" or "Over Weight":
            return difficulty_mapping["easy"]

        # Default to medium if none of the conditions are met
        return difficulty_mapping["other"]

    def create_widgets(self):
        # Display the recommended difficulty level
        difficulty_label = tk.Label(self.root, text=f"Recomended Difficulitay Level: {self.difficulty_var.get()}",
                                    font=("Arial", 14), fg="black", bg="pink")
        difficulty_label.place(relx=0.64, rely=0.25, relwidth=0.27, relheight=0.05)

        exercise_choices = [
            "squats", "bicep_curls", "mountain_climbers", "push_ups", "Dead_Bugs", "Heal_Slides", "Straight_Leg_Raise",
            "Glutebridge", "Siting_Leg_raise", "Wall_Pushup", "Tricep_Dips", "Lunges", "Side_Laying", "Arms_Raise",
            "Clam_Shells", "Situps"
        ]

        exercise_dropdown1 = tk.OptionMenu(self.root, self.exercise_var1, *exercise_choices)
        exercise_dropdown1.config(bg="#8388a6", fg="white", font=("Arial", 14))
        exercise_dropdown1.pack()
        exercise_dropdown1.place(relx=0.36, rely=0.83, relwidth=0.150, relheight=0.070)

        # Exercise selection button
        select_exercise_button = tk.Button(self.root, text="Start Exercise", font=("Arial", 19), fg="white",
                                           bg="#4b60cd", highlightcolor="#4b60cd", highlightbackground="#4b60cd",
                                           highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.pain_exercise)
        select_exercise_button.place(relx=0.655, rely=0.82, relwidth=0.170, relheight=0.070)


        back_button = tk.Button(self.root, text="Back", font=("Arial", 30, 'bold'), fg="white",
                                     bg="#000000", highlightcolor="#4b60cd", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN,
                                     command=self.show_weight_screen)
        back_button.place(relx=0.15, rely=0.82, relwidth=0.100, relheight=0.09)


        home_button = tk.Button(self.root, text="Home", font=("Arial", 17, 'bold'), fg="white", bg="#000000",
                                     highlightcolor="#000000", highlightbackground="#000000",
                                     highlightthickness="1", bd="0", relief=tk.SUNKEN, command=self.run_home)
        home_button.place(relx=0.77, rely=0.05, width=150, height=69)

        self.appointment_button = tk.Button(self.root, text="Take appointment", font=("Arial", 17, 'bold'), fg="white",
                                            bg="#000000", highlightcolor="#000000", highlightbackground="#000000",
                                            highlightthickness="1", bd="0", relief=tk.SUNKEN,
                                            command=self.Take_appointment)
        self.appointment_button.place(relx=0.715, rely=0.15, width=220, height=50)

    def show_weight_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
            self.root.destroy()
        next_screen = tk.Tk()
        Screen9(next_screen, self.pain_level, self.duration, self.status)
        next_screen.mainloop()

    def show_WorkoutAPPGUI(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
            self.root.destroy()

        WorkoutAPP_GUI = tk.Tk()
        WorkoutAppGUI(WorkoutAPP_GUI)
        WorkoutAPP_GUI.mainloop()

    def show_exercise_screen(self):
        self.background_image = None
        if hasattr(self, 'root') and self.root is not None:
            self.root.destroy()
        next_screen = tk.Tk()
        nexts_screen(next_screen, self.duration, self.status, self.pain_level)
        next_screen.mainloop()

    def run_home(self):
        self.root.destroy()
        try:
            # Execute the signup.py script
            subprocess.run([sys.executable, 'home.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running signup script: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

    def Take_appointment(self):
        # Create the data dictionary
        data = {
            "user_data": self.user_data,
            "status": self.status,
            "pain_level": self.pain_level,
            "duration": self.duration,
            "bmi_category": self.bmi_category
        }

        # Save the data to a form.json file
        with open("form.json", "w") as file:
            json.dump(data, file, indent=5)

        # Email credentials
        email = "deepmachine748@gmail.com"
        password = "prtndxpwmblbfemo"

        # Recipient email
        recipient_email = "fariatabassum939@gmail.com"
        subject = "Appointment Details"
        body = "Please find the attached form with appointment details."

        # Initialize yagmail.SMTP
        yag = yagmail.SMTP(email, password)

        # Send the email with the attachment
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body,
            attachments="form.json"
        )

        print("You will be soon informed about the appointment")

    def pain_exercise(self):
        selected_exercise = self.exercise_var1.get()

        # Print values just before calling calculate_difficulty
        print(
            f"Values before calculate_difficulty - status: {self.status}, pain_level: {self.pain_level}, duration: {self.duration}, bmi_category: {self.bmi_category}")

        # Correct the order of parameters passed to calculate_difficulty
        difficulty_level = self.calculate_difficulty(self.status, self.pain_level, self.duration, self.bmi_category)

        print(
            f"Starting exercise: {selected_exercise} with difficulty level: {difficulty_level}, duration: {self.duration}, status: {self.status}, pain level: {self.pain_level}, BMI Category: {self.bmi_category}")

        target_exercises_instance =simulate_target_exercies(difficulty_level)
        if selected_exercise == "squats":
            exercise_generator = target_exercises_instance.squats()
        elif selected_exercise == "bicep_curls":
            exercise_generator = target_exercises_instance.bicep_curls()
        elif selected_exercise == "mountain_climbers":
            exercise_generator = target_exercises_instance.mountain_climbers()
        elif selected_exercise == "push_ups":
            exercise_generator = target_exercises_instance.push_ups()
        elif selected_exercise == "Dead_Bugs":
            exercise_generator = target_exercises_instance.Dead_Bugs()
        elif selected_exercise == "Heal_Slides":
            exercise_generator = target_exercises_instance.Heal_Slides()
        elif selected_exercise == "Straight_Leg_Raise":
            exercise_generator = target_exercises_instance.Straight_Leg_Raise()
        elif selected_exercise == "Glutebridge":
            exercise_generator = target_exercises_instance.Glutebridge()
        elif selected_exercise == "Siting_Leg_raise":
            exercise_generator = target_exercises_instance.Siting_Leg_raise()
        elif selected_exercise == "Wall_Pushup":
            exercise_generator = target_exercises_instance.Wall_Pushup()
        elif selected_exercise == "Tricep_Dips":
            exercise_generator = target_exercises_instance.Tricep_Dips()
        elif selected_exercise == "Lunges":
            exercise_generator = target_exercises_instance.Lunges()
        elif selected_exercise == "Side_Laying":
            exercise_generator = target_exercises_instance.Side_Laying()
        elif selected_exercise == "Arms_Raise":
            exercise_generator = target_exercises_instance.Arms_Raise()
        elif selected_exercise == "Clam_Shells":
            exercise_generator = target_exercises_instance.Clam_Shells()
        elif selected_exercise == "Situps":
            exercise_generator = target_exercises_instance.Situps()
        else:
            print("Invalid exercise selection.")
            return

        for frame in exercise_generator:
            # Process the frame or display it as needed
            pass


    def show_exercise_screen(self):
        self.root.destroy()
        next_screen = tk.Tk()
        nexts_screen(next_screen)
        next_screen.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = WorkoutAppGUI(root)
    root.mainloop()

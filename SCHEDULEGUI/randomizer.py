# randomizer.py

import random

class table_randomizer:
    def __init__(self):
        list_of_processes = [
        "Spotify", "Calculator", "Google Chrome", "Camera", "Bumble", "Microsoft Excel", 
        "Microsoft Edge", "Discord", "Facebook", "Messenger", "Skype", "Steam", "FireFox", 
        "Task Manager", "VLC Media Player", "Microsoft Word", "Microsoft Powerpoint", "Microsoft Office", 
        "Microsoft Outlook", "Microsoft Teams", "Bookworm Adventures", "Adobe Photoshop", 
        "Adobe Premiere Pro", "Adobe Edition", "Adobe Illustrator", "Zoom", "Google Meet", 
        "WPS", "Microsoft OneDrive", "Adobe Reader and Acrobat Manager", "Adobe After Effects", 
        "CheatEngine", "Ibis Paint", "Visual Studio Code", "GitHub Desktop", "CLion", "Sublime Text", 
        "Notepad++", "Notepad", "System Settings", "Command Prompt", "Powershell", "Opera GX", "File Explorer", 
        "PuTTy", "WinRar", "Oracle VM Box", "Team Viewer", "Tindr", "Blender", "SketchUp", "Unity", "PyCharm", 
        "Eclipse", "NetBeans", "MySQL Server", "MySQL Workbench", "XAMPP Control Panel", "PowerPlanner", 
        "Solitaire", "Calendar", "Clock", "Git", "OBS Studio", "Sticky Notes", "Tekken", "Skull Girls", 
        "Stardew Valley" , "Sound Recorder" , "Snipping Tool" , "Terminal" , "Zotero" , "MechaVibes" , 
        "Youtube" , "Instagram" , "Tiktok", "X", "Linkedin", "Capcut", "Netflix", "Honkai Star Rail", 
        "Genshin Impact", "League of Legends", "Dota 2", "Crossfire", "Counter Strike", "Call of Duty", 
        "Last of Us", "The Sims 4", "Grammarly", "Notion", "Trello"
        ]

        self.pick_process = random.choice(list_of_processes)
        self.burst_time = random.randint(1, 15)
        self.memory_size = random.randint(1, 9)
    
# Create an instance of TableRandomizer
randomizer = table_randomizer()

# Use properties and methods from the instance
# print("Process:", randomizer.pick_process)
# print("Burst Time:", randomizer.burst_time, "seconds")
# print("Memory size:", randomizer.memory_size, "bytes")
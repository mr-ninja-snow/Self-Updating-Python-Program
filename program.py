import subprocess
import tkinter as tk
from tkinter import messagebox
from program_version import RELEASE


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.__create_widgets()

        release = RELEASE.rsplit('.', 1)
        self.__majorAndMinoreRelease = release[0]
        self.__maintenanceRelease = int(release[1])

    def __create_widgets(self):
        self.version_lable = tk.Label(self, text="Your running version {}".format(RELEASE))
        self.version_lable.pack()
        self.update_button = tk.Button(self)
        self.update_button["text"] = "Update\n(click me)"
        self.update_button["command"] = self.__update
        self.update_button.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def __update(self):
        self.__fetchLatestChanges()

        if self.__checkForNewRelease():
            return

        if self.__checkForBugfixes():
            return

        messagebox.showinfo("Updater", "You are running the latest version of the application!")

    def __checkForNewRelease(self):
        return False

    def __getTagList(self):
        gitCmd = 'git tag -l "r{}*"'.format(self.__majorAndMinoreRelease)
        output = subprocess.check_output(gitCmd)
        tags = output.decode('utf-8').splitlines()
        return tags

    def __checkForNewMaintenanceReleases(self, tags):
        latestMaintenanceRelease = 0
        for tag in tags:
            tagMaintenanceRelease = int(tag.rsplit('.', 1)[1])
            if self.__maintenanceRelease < tagMaintenanceRelease and tagMaintenanceRelease > latestMaintenanceRelease:
                latestMaintenanceRelease = tagMaintenanceRelease

        if latestMaintenanceRelease:
            latestMaintenanceReleaseTag = 'r{}.{}'.format(self.__maintenanceRelease, latestMaintenanceRelease)
            self.__updateToLatestMaintenanceRelease(latestMaintenanceReleaseTag)
            return True
        return False

    def __updateToLatestMaintenanceRelease(self, latestMaintenanceReleaseTag):
        updateCmd = 'pip install --upgrade --src=".." -e git+https://github.com/mr-ninja-snow/Self-Updating-Python-Program.git@{}#egg=Self-Updating-Python-Program'.format(latestMaintenanceReleaseTag)
        subprocess.Popen(updateCmd)

    def __checkForBugfixes(self):
        tags = self.__getTagList()
        return self.__checkForNewMaintenanceReleases(tags)

    def __fetchLatestChanges(self):
        fetchCmd = "git fetch --all"
        subprocess.Popen(fetchCmd)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
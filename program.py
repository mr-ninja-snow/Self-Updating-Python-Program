import re
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

    def __getBranchList(self):
        gitCmd = 'git branch -a'
        output = subprocess.check_output(gitCmd)
        branches = output.decode('utf-8').splitlines()
        return branches

    def __checkForNewMajorOrMinorRelease(self, branches):
        currentVersion = self.__majorAndMinoreRelease.split('.')
        currentBranchMajorVersion = int(currentVersion[0])
        currentBranchMinorVersion = int(currentVersion[1])
        currentVersion = currentBranchMajorVersion*10 + currentBranchMinorVersion

        latestMajorRelease = 0
        latestMinorRelease = 0
        latestVersion = 0
        for branchName in branches:
            if '*' in branchName or 'HEAD' in branchName:
                continue

            match = re.findall(r'r(\d+)\.(\d+)', branchName)
            if match:
                majorRelease = int(match[0][0])
                minorRelease = int(match[0][1])
                version = majorRelease*10 + minorRelease
                if version > currentVersion and version > latestVersion:
                    latestMajorRelease = majorRelease
                    latestMinorRelease = minorRelease
                    latestVersion = version

        if latestVersion:
            latestReleaseBranchName = 'r{}.{}'.format(latestMajorRelease, latestMinorRelease)
            self.__updateToLatestMajorOrMinorRelease(latestReleaseBranchName)
            return True
        return False

    def __updateToLatestMajorOrMinorRelease(self, latestReleaseBranchName):
        updateCmd = 'git checkout {}'.format(latestReleaseBranchName)
        subprocess.call(updateCmd)

    def __checkForNewRelease(self):
        branches = self.__getBranchList()
        return self.__checkForNewMajorOrMinorRelease(branches)

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
            latestMaintenanceReleaseTag = 'r{}.{}'.format(self.__majorAndMinoreRelease, latestMaintenanceRelease)
            self.__updateToLatestMaintenanceRelease(latestMaintenanceReleaseTag)
            return True
        return False

    def __updateToLatestMaintenanceRelease(self, latestMaintenanceReleaseTag):
        updateCmd = 'git checkout tags/{}'.format(latestMaintenanceReleaseTag)
        subprocess.call(updateCmd)

    def __checkForBugfixes(self):
        tags = self.__getTagList()
        return self.__checkForNewMaintenanceReleases(tags)

    def __fetchLatestChanges(self):
        fetchCmd = "git fetch --all"
        subprocess.call(fetchCmd)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
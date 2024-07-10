import subprocess

# variables
repository=r"https://github.com/xivapi/SaintCoinach.git"
localFolder=r"C:\Users\naupa.LAURENPC2\dev\SaintCoinach"
slnFile=r"C:\Users\naupa.LAURENPC2\dev\SaintCoinach\SaintCoinach.sln"
exeFile=r"C:\Users\naupa.LAURENPC2\dev\SaintCoinach\SaintCoinach.Cmd\bin\Debug\net7.0\SaintCoinach.Cmd.exe"
configFile=r"C:\Users\naupa.LAURENPC2\dev\SaintCoinach\SaintCoinach.Cmd\App.config"
gamePath=r"C:\Games\SquareEnix\FINAL FANTASY XIV - A Realm Reborn"

# delete repository code if it exists
subprocess.run(f'rm -rf "{localFolder}"')

# clone SaintCoinach
subprocess.run(f'git clone "{repository}" "{localFolder}"')

# update the app config file with the appropriate path to game
fileContents = ""
with open(configFile, 'rt') as fh:
    fileContents = fh.read()

fileContents = fileContents.replace(r"<value />", f"<value>{gamePath}</value>")

with open(configFile, 'w') as fh:
    fh.write(fileContents)

subprocess.run(f'dotnet build "{slnFile}"')
# subprocess.call(f'"{exeFile}"')
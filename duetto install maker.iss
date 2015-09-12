; -- duetto install maker.iss --

; SEE THE DOCUMENTATION FOR DETAILS ON CREATING .ISS SCRIPT FILES!

[Setup]
AppName=duetto SoundLab
AppVersion=0.7.2
DefaultDirName={pf}\duetto SoundLab
DefaultGroupName=duetto SoundLab
UninstallDisplayIcon={app}\Duetto_Sound_Lab.exe
Compression=lzma2
SolidCompression=yes
OutputDir=installer
OutputBaseFilename=duetto SoundLab v0.7.2
SetupIconFile=duetto-icon-64x64.png
WizardImageFile=duetto-setup-icon.bmp
WizardSmallImageFile=duetto-setup-icon-small.bmp

[Files]
Source: "dist_cfx_basic\*"; DestDir: "{app}"; Flags: recursesubdirs

[Icons]
Name: "{group}\duetto SoundLab"; Filename: "{app}\Duetto_Sound_Lab.exe"

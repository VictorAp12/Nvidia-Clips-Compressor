#define MyAppName "Nvidia Clips Compressor (NVENC)"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "VictorAp12"
#define MyAppExeName "Nvidia Clips Compressor (NVENC).exe"

[Setup]
AppId={{A4F3C7C2-8F4C-4A10-B7C4-9C2D9A123456}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=Nvidia-Clips-Compressor-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=app.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

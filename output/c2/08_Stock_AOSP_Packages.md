> 翻译：[Ross.Zeng](https://github.com/zengrx)
> 校对：

### AOSP应用包

在大部分安卓设备中，AOSP都会捆绑几个默认的应用包，在之前章节中也有提到过。如地图、油管、Gmail就不能算在AOSP中。表2-5中列举了AOSP中默认的这些包，表2-6中AOSP中的内容提供者，表2-7中则展示了默认输入法。

*表2-5. 安卓应用包*

App in AOSP|Name displayed in Launcher|Description
-|-|-
AccountsAndSettings|N/A|Accounts management app
Bluetooth|N/A|Bluetooth manager
Browser|Browser|Default Android browser, includes bookmark widget
Calculator|Calculator|Calculator app
Camera|Camera|Camera app
Certinstaller|N/A|UI for installing certificates
Contacts|Contacts|Contacts manager app
DeskClock|Clock|Clock and alarm app, including the clock widget
Email|Email|Default Android email app
Development|Dev Tools|Miscellaneous dev tools
Gallery|Gallery|Default gallery app for viewing pictures
Gallery3D|Gallery|Fancy gallery with "sexier" UI
HTMLViewer|N/A|App for viewing HTML files
Launcher2|N/A|Default home screen
Mms|Messaging|SMS/MMS app
Music|Music|Music player
PackageInstaller|N/A|App install/uninstall UI
Phone|Phone|Default phone dialer/UI
Protips|N/A|Home screen tips
Provision|N/A|App for setting a flag indicating whether a device was provisioned
QuickSearchBox|Search|Search app and widget
Settings|Settings|Settings app, also accessible through home screen menu
SoundRecorder|N/A|Sound recording app
SpeechRecorder|Speech Recorder|Speech recording app
SystemUI|N/A|Status bar

*Table 2-6. Stock AOSP Providers*

Provider|Description
-|-
ApplicationProvider|Provider for search installed apps
CalendarProvider|Main Android calendar storage and provider
ContactsProvider|Main Android contacts storage and provider
DownloadProvider|Download management, storage and  access
DmProvider|Management and access of DRM-protected storage
MediaProvider|Media storage and provider
TelephonyProvider|Carrier and SMS/MMS storage and provider
UserDictionnaryProvider|Storage and provider for user-defined words dictionary


*Table 2-7. Stock AOSP Input Methods*

Input Methods|Description
-|-
LatinIME|Latin keyboard
OpenWnn|Japanese keyboard
PinyinIME|Chinese keyboard

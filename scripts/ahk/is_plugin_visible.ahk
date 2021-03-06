#SingleInstance, Force
SendMode Input
SetWorkingDir, %A_ScriptDir%

name := A_Args[1]

exit_if_visible(name)
{
    WinGet, id, list,,, Program Manager
    Loop, %id%
    {
        this_id := id%A_Index%
        WinGetClass, this_class, ahk_id %this_id%
        WinGetTitle, this_title, ahk_id %this_id%
        if (this_class == "AbletonVstPlugClass") {
            if (name) {
                if (InStr(this_title, name, false)) {
                    ExitApp, 1
                }
            } else {
                ExitApp, 1
            }
        }
    }
}

exit_if_visible(name)

ExitApp, 0

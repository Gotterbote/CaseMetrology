param(
    [string]$ReceiverRoot = "C:\CaseMetrologyReceiver",
    [string]$TaskName = "CaseMetrology Office Receiver",
    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction Stop).Source
}

$ReceiverPath = Join-Path $ReceiverRoot "receiver.py"

if (-not (Test-Path $ReceiverPath)) {
    throw "Receiver not found: $ReceiverPath"
}

$Account = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

Write-Host "Installing CaseMetrology receiver task"
Write-Host "Task name:     $TaskName"
Write-Host "Account:       $Account"
Write-Host "Python:        $PythonPath"
Write-Host "Receiver root: $ReceiverRoot"
Write-Host "Receiver:      $ReceiverPath"

$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "-u `"$ReceiverPath`"" `
    -WorkingDirectory $ReceiverRoot

$Trigger = New-ScheduledTaskTrigger `
    -AtLogOn `
    -User $Account

$Principal = New-ScheduledTaskPrincipal `
    -UserId $Account `
    -LogonType Interactive `
    -RunLevel Limited

$Settings = New-ScheduledTaskSettingsSet `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -MultipleInstances IgnoreNew `
    -ExecutionTimeLimit ([TimeSpan]::Zero)

Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Principal $Principal `
    -Settings $Settings `
    -Force | Out-Null

Write-Host
Write-Host "Scheduled task installed."

$Task = Get-ScheduledTask -TaskName $TaskName

Write-Host "State:" $Task.State

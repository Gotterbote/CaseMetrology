param(
    [string]$ReceiverRoot = "C:\CaseMetrologyReceiver",
    [string]$TaskName = "CaseMetrology Engineering Dashboard",
    [string]$PythonPath = ""
)

$ErrorActionPreference = "Stop"

if (-not $PythonPath) {
    $PythonPath = (Get-Command python -ErrorAction Stop).Source
}

$DashboardPath = Join-Path $ReceiverRoot "dashboard.py"

if (-not (Test-Path $DashboardPath)) {
    throw "Dashboard not found: $DashboardPath"
}

$Account = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name

Write-Host "Installing CaseMetrology engineering dashboard task"
Write-Host "Task name:      $TaskName"
Write-Host "Account:        $Account"
Write-Host "Python:         $PythonPath"
Write-Host "Receiver root:  $ReceiverRoot"
Write-Host "Dashboard:      $DashboardPath"
Write-Host "Dashboard URL:  http://127.0.0.1:8767"

$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "-u `"$DashboardPath`"" `
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

## F-Secure Status

$av = Get-WmiObject -Namespace "root/fsecure" -Class AntiVirus2
$bp = Get-WmiObject -Namespace "root/fsecure" -Class Internet2
$cm = Get-WmiObject -Namespace "root/fsecure" -Class CentralManagement2

write-host "<<<fsecure_status:sep(58)>>>"
write-host "RealTimeScanningEnabled:" $av.RealTimeScanningEnabled
write-host "DeepGuardEnabled:" $av.DeepGuardEnabled
write-host "BrowsingProtectionEnabled:" $bp.BrowsingProtectionEnabled

write-host "LastConnectionTimeInHoursAgo:" $cm.LastConnectionTimeInHoursAgo
write-host "AvDefinitionsAgeInHours:" $av.AvDefinitionsAgeInHours
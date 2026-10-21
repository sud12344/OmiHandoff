# dialog_watch.ps1 (2026-10-20, ORFS dry runs): while the dry-run batches run, answer OK on ONE kind of SolidWorks dialog only - the
# design-table insert warning that lists table parameters the part does not have (a #32770 "SOLIDWORKS ..." task dialog whose only
# button is OK and whose text lists name@feature parameters + "Copy all to Clipboard"). Every dialog it answers is logged with its full
# text to dialogs_log.txt. Any other dialog (e.g. the low-memory one) is logged as SEEN and left alone.
# Stops when the file dialog_watch.stop exists or after $Hours.
param([double]$Hours = 4)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$log = Join-Path $here 'dialogs_log.txt'
$stop = Join-Path $here 'dialog_watch.stop'
Add-Type @'
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class DW {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc f, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr p, EnumProc f, IntPtr l);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern IntPtr SendMessage(IntPtr h, int msg, IntPtr w, StringBuilder l);
  [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, int msg, IntPtr w, IntPtr l);
  public static string Txt(IntPtr k) { int n = (int)SendMessage(k, 0x000E, IntPtr.Zero, IntPtr.Zero); var t = new StringBuilder(n + 2); SendMessage(k, 0x000D, (IntPtr)(n + 1), t); return t.ToString(); }
  public static string Cls(IntPtr k) { var c = new StringBuilder(128); GetClassName(k, c, 128); return c.ToString(); }
  public static List<IntPtr> Dialogs(uint pid) { var r = new List<IntPtr>(); EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p); if (p == pid && IsWindowVisible(h) && Cls(h) == "#32770") r.Add(h); return true; }, IntPtr.Zero); return r; }
  public static List<IntPtr> Kids(IntPtr p) { var r = new List<IntPtr>(); EnumChildWindows(p, (k, l) => { r.Add(k); return true; }, IntPtr.Zero); return r; }
}
'@
$seen = @{}
$end = (Get-Date).AddHours($Hours)
"$(Get-Date -Format s) watcher started" | Out-File -Append -Encoding utf8 $log
while ((Get-Date) -lt $end -and -not (Test-Path $stop)) {
  $sw = Get-Process SLDWORKS -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($sw) {
    foreach ($h in [DW]::Dialogs([uint32]$sw.Id)) {
      $kids = [DW]::Kids($h)
      $buttons = @($kids | Where-Object { [DW]::Cls($_) -eq 'Button' })
      $texts = @($kids | ForEach-Object { [DW]::Txt($_) } | Where-Object { $_ })
      $all = ($texts -join ' / ')
      $title = [DW]::Txt($h)
      $isTable = ($title -like 'SOLIDWORKS*') -and ($buttons.Count -eq 1) -and ([DW]::Txt($buttons[0]) -eq 'OK') -and ($all -match 'Copy all to Clipboard') -and ($all -match '\w@\w')
      if ($isTable) {
        "$(Get-Date -Format s) OK on [$title]: $all" | Out-File -Append -Encoding utf8 $log
        [DW]::SendMessage($buttons[0], 0x00F5, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
      } elseif (-not $seen.ContainsKey([string]$h)) {
        $seen[[string]$h] = 1
        "$(Get-Date -Format s) SEEN, left alone [$title]: $all" | Out-File -Append -Encoding utf8 $log
      }
    }
  }
  Start-Sleep -Seconds 2
}
"$(Get-Date -Format s) watcher stopped" | Out-File -Append -Encoding utf8 $log

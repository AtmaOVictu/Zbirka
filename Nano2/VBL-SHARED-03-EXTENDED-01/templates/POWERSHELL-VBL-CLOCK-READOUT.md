# Windows PowerShell 5.1 compatible, read-only clock readout

Zaženi v običajnem promptu, ne v `>>` nadaljevalnem promptu. Ukazi samo berejo lokalno uro in konfiguracijo Windows Time. Ne nastavljajo ure.

```powershell
Get-Date -Format o
(Get-Date).ToUniversalTime().ToString('o')
(Get-TimeZone).Id
w32tm.exe /query /status
w32tm.exe /query /source
```

Shrani celoten izhod in vse napake. Če `w32tm.exe` ne obstaja, ni dostopen ali vrne napako, zabeleži tudi to; ne popravljaj izpisa. Vrednost `Get-Date` je odčitek lokalne sistemske ure. Izpis `w32tm` je poročilo lokalnega Windows Time odjemalca. Noben od njiju sam po sebi ni neodvisen časovni žig ali dokaz avtorstva.

V evidenci loči `observed_local`, pretvorbo UTC, časovni pas, vir, izhodni status in morebitno zunanjo časovno potrditev. Če slednje ni, uporabi `NOT_RECORDED` / `UNVERIFIED`; časa ne dopisuj za nazaj.
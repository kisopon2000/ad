#Requires -Version 4.0

Param(
    [alias("S")]
    [string] $sqlServer = "localhost",

    [Parameter(Mandatory=$True)]
    [alias("I")]
    [string] $sqlInstance,

    [Parameter(Mandatory=$False)]
    [alias("port")]
    [int] $sqlPort = 0,

    [Parameter(Mandatory=$True)]
    [alias("D")]
    [string] $sqlDatabase,

    [Parameter(Mandatory=$True)]
    [alias("U")]
    [string] $sqlUser,

    [Parameter(Mandatory=$True)]
    [alias("P")]
    [string] $sqlPassword,

    [Parameter(Mandatory=$True)]
    [alias("dataDir")]
    [string] $predefineDataDir
)

if (-Not (Test-Path $predefineDataDir)) {
    Write-Host "$($predefineDataDir) Not Found"
    exit 1
}

function Get-SqlServerUrl() {
    $url = "$($sqlServer)\$($sqlInstance)"
    if ($sqlPort -ne 0) {
        $url += ",$($sqlPort)"
    }
    Write-Host "DB URL=$($url)"
    return $url;
}

function Invoke-SqlCmdToDB([string] $query ) {
    Invoke-SqlCmd -Query $query -ServerInstance $sqlUrl -Database $sqlDatabase -Username $sqlUser -Password $sqlPassword
}

$sqlUrl = Get-SqlServerUrl

Set-Location $predefineDataDir

foreach ( $csvFile in Get-ChildItem -Recurse -Filter *.csv | ? {$_ -Is [IO.FileInfo]} | Resolve-Path -Relative ) {
    Write-Host "File Loading... $($csvFile)"
    $allRecordData = Import-Csv -LiteralPath $csvFile -Encoding Default

    $fileBaseName = (Get-Item $csvFile).BaseName
    Write-Host "Inserting records to $($fileBaseName)"

    foreach ( $recordData in $allRecordData ) {
        $columns = ""
        $values = ""

        $keyValues = $recordData | Get-Member -MemberType 'NoteProperty' | `
            ForEach-Object -Process { $_.Definition.Substring($_.Definition.IndexOf(' ')+1) }
        $isFirst = $True
        foreach ( $keyValue in $keyValues ) {
            if ($isFirst) {
                $isFirst = $False
            } else {
                $columns += ","
                $values += ","
            }

            $kv = $keyValue -split '='
            $columns += $kv[0]
            $values += $kv[1]
        }
        $query = "INSERT INTO [$($fileBaseName)] ($($columns)) VALUES ($($values));"
        #Write-Host "$query = $($query)"
        Invoke-SqlCmdToDB $query
    }
    Write-Host "Finish Inserting to $($fileBaseName)"
}

Write-Host "Done"
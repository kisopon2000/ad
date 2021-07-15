#Requires -Version 4.0

Param(
    [alias("S")]
    [string] $sqlServer = "localhost",

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
    [string] $predefineDataDir,

    [Parameter(Mandatory=$True)]
    [alias("dataList")]
    [string] $predefineDataList,

    [Parameter(Mandatory=$False)]
    [alias("R")]
	[switch] $resetAutoIncrement,
	
	[Parameter(Mandatory=$False)]
	[string] $instLang = "ja"
)

if (-Not (Test-Path $predefineDataDir)) {
    Write-Host "$($predefineDataDir) Not Found"
    exit 1
}

if (-Not (Test-Path $predefineDataList)) {
    Write-Host "$($predefineDataList) Not Found"
    exit 1
}

Set-Variable MYSQL_ASSEMBLIES_DIR "C:\Program Files (x86)\MySQL"

#--------------------------------------
# �C�j�V�����C�Y
#--------------------------------------
function Initialize()
{
    # MySQL�ˑ��t�@�C���̃o�C���h
    $mysqlAssemblies = $script:MYSQL_ASSEMBLIES_DIR
    $dir = Get-ChildItem $mysqlAssemblies -Filter * | Where-Object { $_.Name -like "Connector NET *" }
    if(!$dir){
        Write-Host "MySQL assemblies ($mysqlAssemblies) Not Found"
        exit 1
    }
    $mysqlAssemblies = Join-Path $mysqlAssemblies $dir.Name
    $dir = Get-ChildItem $mysqlAssemblies -Filter * | Where-Object { $_.Name -like "Assemblies" }
    if(!$dir){
        Write-Host "MySQL assemblies ($mysqlAssemblies) Not Found"
        exit 1
    }
    $mysqlAssemblies = Join-Path $mysqlAssemblies $dir.Name
    $dir = Get-ChildItem $mysqlAssemblies -Filter * | Where-Object { $_.Name -like "v*" }
    if(!$dir){
        Write-Host "MySQL assemblies ($mysqlAssemblies) Not Found"
        exit 1
    }
    $mysqlAssemblies = Join-Path $mysqlAssemblies $dir.Name

    Add-Type -Path "$mysqlAssemblies\MySQL.Data.dll"
    Add-Type -Path "$mysqlAssemblies\Renci.SshNet.dll"
}

#--------------------------------------
# �t�@�C�i���C�Y
#--------------------------------------
function Finalize()
{
}

#--------------------------------------
# DB�T�[�o�[�ڑ�URL�擾
#--------------------------------------
function Get-DBServerUrl() {
    $url = "server='$sqlServer';port='$sqlPort';uid='$sqlUser';pwd=$sqlPassword;database=$sqlDatabase"
    Write-Host "DB URL=$($url)"
    return $url;
}

#--------------------------------------
# DB�ڑ�
#--------------------------------------
function Connect-DBServer($url)
{
    try{
        $descriptor = New-Object MySql.Data.MySqlClient.MySqlConnection($url)
        $descriptor.ConnectionString = $url
        $descriptor.Open()
    }catch{
        Write-host $error -ForegroundColor Red
        exit 1
    }
    return $descriptor
}

#--------------------------------------
# SQL���s
#--------------------------------------
function Invoke-SqlCmdToDB($descriptor, $query)
{
    $command = $descriptor.CreateCommand()
    $command.CommandText = $query

    try{
        $ret = $command.ExecuteNonQuery();
    }catch{
        Write-host $error -ForegroundColor Red
    }
}

#--------------------------------------
# SQL���s
#--------------------------------------
function Invoke-SqlCmdToDBIgnoreError($descriptor, $query)
{
    $command = $descriptor.CreateCommand()
    $command.CommandText = $query

    try{
        $ret = $command.ExecuteNonQuery();
    }catch{
        # �G���[�͖���
    }
}

#--------------------------------------
# DB�ؒf
#--------------------------------------
function Disconnect-DBServer($descriptor)
{
    $descriptor.Close()
}

#--------------------------------------
# ini�t�@�C���ǂݍ���
# <�ԋp�l>	���� = Ini�t�@�C���n�b�V���e�[�u��
#			���s = $null
#			�ڍ� = INI_LIB_ERRORSTRING�ɂĎ擾
#--------------------------------------
function Read-IniFile(
	[string]$path = $(throw "please input a value for the path parameter")
)
{
	$script:INI_LIB_ERRORSTRING = @()
	Set-Variable iniCommentPattern	"^\s*[#;]" -option constant
	Set-Variable iniSectionPattern	"^\[(.+)\](.+|$)" -option constant
	Set-Variable iniParamPattern	"([\w\s]+)=(.+|$)" -option constant

	# ini�t�@�C�������i�[�����n�b�V���e�[�u�����쐬����
	$ini = @{}

	if (Test-Path -path $path) {
		# switch��file�w���shift-jis���ǂݍ��߂Ȃ��ׁA��U�����ϐ��Ɋi�[���ăG���R�[�h�ϊ�����
		$contents = Get-Content $path -Encoding UTF8
		# �s�P�ʂŃp�^�[���}�b�`���O
		switch -regex ($contents) {
			$iniCommentPattern {
				Write-Debug "<Read-IniFile> found comment. com=$_"
				continue
			}
			$iniSectionPattern {
				$section = $matches[1].Trim()
				# �����t�@�C�����œ����Z�N�V�����������񌻂�邱�Ƃ͂��肦�Ȃ�
				if ($ini.$section) {
					$script:INI_LIB_ERRORSTRING += "<Read-IniFile> section already exists. path=$path, sec=$section"
					return $script:INI_LIB_FALSE
				}
				$ini.$section = @{}
				Write-Debug "<Read-IniFile> found section. sec=$section"
			}
			$iniParamPattern {
				$key = $matches[1].Trim()
				# �l�̌��ɂ���R�����g����菜��
				$removeIndex = $matches[2].IndexOf('#')
				if ($removeIndex -ne -1) {
					$value = ($matches[2].Remove($removeIndex)).Trim()
				} else {
					$value = $matches[2].Trim()
				}
				$ini.$section.$key = $value
				Write-Debug "<Read-IniFile> found param. sec=$section, key=$key, val=$value"
			}
		}
	} else {
		$script:INI_LIB_ERRORSTRING += "<Read-IniFile> not found $path"
		return $script:INI_LIB_FALSE
	}
	$script:INI_LIB_ERRORSTRING += "<Read-IniFile> success"
	return $ini
}

#--------------------------------------
# ini�t�@�C���L�[�ꗗ�擾
# <�ԋp�l>	���� = �L�[������z��
#			���s = INI_LIB_FALSE
#			�ڍ� = INI_LIB_ERRORSTRING�ɂĎ擾
#--------------------------------------
function Get-IniKeyList(
	[string]$path        = $(throw "please input a value for the path parameter"),
	[string]$section     = $(throw "please input a value for the section parameter"),
	[switch]$sort        = $true,
	[hashtable]$iniTable = $null
)
{
	$script:INI_LIB_ERRORSTRING = @()
	if (-not $iniTable) {
		# ini�n�b�V���e�[�u�����擾
		$ini = Read-IniFile -path $path
		if ($ini -eq $INI_LIB_FALSE) {
			$script:INI_LIB_ERRORSTRING += "<Get-IniKeyList> read file error. path=$path"
			return $script:INI_LIB_FALSE
		}
	} else {
		$ini = $iniTable
	}

	# �l���������Ĕz��ɒǉ�
	if ($ini.count) {
		if ($ini.contains($section)) {
			$keyList = @()
			foreach ($key in $ini.$section.Keys) {
				$keyList += $key
			}
			if ($sort) {
				$keyList = $keyList | Sort-Object
			}
			$script:INI_LIB_ERRORSTRING += "<Get-IniKeyList> success"
			return $keyList
		} else {
			$script:INI_LIB_ERRORSTRING += "<Get-IniKeyList> section $section does not exist in $path"
			return $script:INI_LIB_FALSE
		}
	}
	$script:INI_LIB_ERRORSTRING += "<Get-IniKeyList> not found sections in $path"
	return $script:INI_LIB_FALSE
}

#--------------------------------------
# ini�t�@�C���l�擾
# <�ԋp�l>	���� = �L�[������
#			���s = INI_LIB_FALSE
#			�ڍ� = INI_LIB_ERRORSTRING�ɂĎ擾
#--------------------------------------
function Get-IniValue(
	[string]$path        = $(throw "please input a value for the path parameter"),
	[string]$section     = $(throw "please input a value for the section parameter"),
	[string]$key         = $(throw "please input a value for the key parameter"),
	[hashtable]$iniTable = $null
)
{
	$script:INI_LIB_ERRORSTRING = @()
	if (-not $iniTable) {
		# ini�n�b�V���e�[�u�����擾
		$ini = Read-IniFile -path $path
		if ($ini -eq $INI_LIB_FALSE) {
			$script:INI_LIB_ERRORSTRING += "<Get-IniValue> read file error. path=$path"
			return $script:INI_LIB_FALSE
		}
	} else {
		$ini = $iniTable
	}

	# �l���������Ď擾
	if ($ini.count) {
		if ($ini.contains($section)) {
			if ($ini.$section.contains($key)) {
				$script:INI_LIB_ERRORSTRING += "<Get-IniValue> success"
				return $ini.$section.$key
			} else {
				$script:INI_LIB_ERRORSTRING += "<Get-IniValue> $key does not exist in $path, section $section"
				return $script:INI_LIB_FALSE
			}
		} else {
			$script:INI_LIB_ERRORSTRING += "<Get-IniValue> section $section does not exist in $path"
			return $script:INI_LIB_FALSE
		}
	}
	$script:INI_LIB_ERRORSTRING += "<Get-IniValue> not found sections in $path"
	return $script:INI_LIB_FALSE
}

#--------------------------------------
# ���C��
#--------------------------------------
function Main()
{
    $url = Get-DBServerUrl
    $descriptor = Connect-DBServer $url

    $predefineDataList = Resolve-Path $predefineDataList
    Set-Location $predefineDataDir

    $dir =  Get-Location
    $files = Get-IniKeyList $predefineDataList 'CSV'
    $pathes = @()
    foreach ($key in $files) {
        $file = Get-IniValue $predefineDataList 'CSV' $key
        if([String]::IsNullOrEmpty($file)){ continue } 
    
        if ($file.Contains("{lang}")) {
            $file = $file.Replace("{lang}",$instLang)
        }
    
        if (-Not (Test-Path $file)) {
            Write-Host "$($file ) Not Found"
            continue
        }
        $file=Get-ChildItem $file -File
        if (-Not ($file.Extension -eq ".csv")) {
            Write-Host "$($file ) is not a csv."
            continue
        }
        $pathes += $file
    }

    foreach($csvFile in $pathes | ? {$_ -Is [IO.FileInfo]}){
        Write-Host "File Loading... $($csvFile)"
        $allRecordData = Import-Csv -LiteralPath $csvFile -Encoding UTF8

        $fileBaseName = (Get-Item $csvFile).BaseName
        Write-Host "Inserting records to $($fileBaseName)"

        if($script:resetAutoIncrement){
            $query = "ALTER TABLE $($fileBaseName) auto_increment = 1;"
            Invoke-SqlCmdToDBIgnoreError $descriptor $query
        }

        foreach($recordData in $allRecordData){
            $columns = ""
            $values = ""

            $keyValues = $recordData | Get-Member -MemberType 'NoteProperty' | `
                ForEach-Object -Process { $_.Definition.Substring($_.Definition.IndexOf(' ')+1) }
            $isFirst = $True
            foreach($keyValue in $keyValues){
                if($isFirst) {
                    $isFirst = $False
                }else{
                    $columns += ","
                    $values += ","
                }

                $kv = $keyValue -split '=', 2
                $columns += $kv[0]
                $values += $kv[1]
            }
            $query = "INSERT INTO $($fileBaseName) ($($columns)) VALUES ($($values));"
            Invoke-SqlCmdToDB $descriptor $query
        }
        Write-Host "Finish Inserting to $($fileBaseName)"
    }

    Disconnect-DBServer $descriptor
}

# �G���g���[�|�C���g
Initialize
Main
Finalize

Write-Host "Done"

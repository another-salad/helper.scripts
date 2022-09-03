# WIP
# Collects temperature sensor information from the endpoints in config.json and passes it across
# to another endpoint (also in config.json)

function getSensorData ($sensorEndpoints) {
    $allSensorData = @{}
    foreach ($sensor in $sensorEndpoints) {
        $data = Invoke-RestMethod -Uri $sensor
        $allSensorData[$data.loc] = $data.temp
    }
    return $allSensorData
}

$json = Get-Content .\config.json | out-string | ConvertFrom-Json
$returnedSensorData = getSensorData $json.sensors
foreach ($sensorData in $returnedSensorData.GetEnumerator()) {
    Write-Host "$($sensorData.Name): $($sensorData.Value)"
}

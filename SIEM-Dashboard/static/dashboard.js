async function fetchLogs() {
    const response = await fetch('/api/logs')
    const logs = await response.json()

    const table = document.getElementById('logTable')

    table.innerHTML = ""

    let alerts = 0

    logs.forEach(log => {
        if (log.level === "ALERT") alerts++

        table.innerHTML += `
            <tr>
                <td>${log.level}</td>
                <td>${log.message}</td>
            </tr>
        `
    })

    document.getElementById("alertCount").innerText = alerts
}

setInterval(fetchLogs, 2000)
fetchLogs()
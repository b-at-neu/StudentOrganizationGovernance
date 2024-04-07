export function post(url, data) {
    const XML = new XMLHttpRequest()
    XML.open("POST", url)
    XML.setRequestHeader("Content-Type", "application/json; charset=UTF-8")
    XML.setRequestHeader("X-CSRFToken", decodeURIComponent(document.cookie.split(';').map(c => c.trim()).filter(c => c.startsWith("csrftoken" + '='))[0].split('=')[1]))
    XML.send(JSON.stringify(data))
}
export async function post(url, data) {
    return fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
        headers: {
            "Content-type": "application/json; charset=UTF-8",
            "X-CSRFToken": decodeURIComponent(document.cookie.split(';').map(c => c.trim()).filter(c => c.startsWith("csrftoken" + '='))[0].split('=')[1]),
        }
    })
    .then((r) => r.json())
    .then((json) => json)
}
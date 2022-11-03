function uuid4() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
}

function acceptMassage(data) {
    let messageElement = document.querySelector(`.user-message[data-uuid="${data['uuid']}"] path.sended`)
    messageElement.setAttribute('class', 'sended')
}

function convertTZ(date, tzString) {
    return new Date((typeof date === "string" ? new Date(date) : date).toLocaleString("en-US", {timeZone: tzString}));
}

async function fetchSender(url, method, formData, successHandle, errorHandle) {
    try {
        let response
        if (method === 'GET') {
            response = await fetch(url, {
                method: method,
                mode: "no-cors"
            })
        } else {
            response = await fetch(url, {
                method: method,
                body: formData,
                mode: "no-cors"
            });
        }
        const result = await response.json();
        successHandle(result)
    } catch (e) {
        errorHandle(e)
    }
}
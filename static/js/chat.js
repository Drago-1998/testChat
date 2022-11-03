let nextPage = 1;
const chatInitDate = convertTZ(new Date(), 'utc');
const chatInitDateStr = moment(chatInitDate).format('YYYY-MM-DD HH:MM:ss');
const localTimeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
const PAGE_LIMIT = 25;

let chatElem = document.getElementById('chat-list')

// DOM Ready Listener

document.addEventListener('DOMContentLoaded', () => {
    loadMassages(nextPage)
})

// Send Message from user

function sendMessage(inputElemId) {
    let inputElem = document.getElementById(inputElemId)
    let message = inputElem.value
    let time = moment(new Date()).format('HH:mm')
    let clientUUId = uuid4()

    chatElem.innerHTML = userMessageRender(message, time, clientUUId, '') + chatElem.innerHTML
    let data = new FormData()
    data.append('csrfmiddlewaretoken', CSRF_TOKEN)
    data.append('text', message)
    data.append('user', CURRENT_USER_ID)
    data.append('room', +ROOM_ID)
    data.append('uuid', clientUUId)
    fetchSender('/api/v1/messages/', 'post', data, console.log, console.log)
    inputElem.value = ''
}

// Scrolling Loader

let scrollHandle = (e) => {

    let topScrollPosition = -(e.target.scrollTop - document.body.offsetHeight)
    let listHeight = e.target.scrollHeight

    if (topScrollPosition >= listHeight) {
        loadMassages(nextPage)
        chatElem.removeEventListener('scroll', scrollHandle)
    }
}


function messagesRender(data) {
    let messages = data['results']

    for (let message of messages) {
        if (message['user'] === CURRENT_USER_ID) {
            let date = convertTZ(new Date(message['created_at']), localTimeZone)
            let timeStr = moment(date).format('HH:mm')
            chatElem.innerHTML += userMessageRender(message['text'], timeStr, '', '', true)
        } else {
            let date = convertTZ(new Date(message['created_at']), localTimeZone)
            let timeStr = moment(date).format('HH:mm')
            chatElem.innerHTML += chatUserMessageRender(message['user_obj']['username'], message['text'], timeStr)
        }
    }
    nextPage = data['next_page']
    chatElem.addEventListener('scroll', scrollHandle)
}

function loadMassages(page) {
    let url = ''
    if (page === 1) {
        url = `/api/v1/messages/?room=${ROOM_ID}&created_at__lt=${chatInitDateStr}&limit=${PAGE_LIMIT}&ordering=-created_at`
    } else if (page) {
        url = `/api/v1/messages/?room=${ROOM_ID}&created_at__lt=${chatInitDateStr}&limit=${PAGE_LIMIT}&page=${page}&ordering=-created_at`
    } else {
        return 0
    }
    fetchSender(url, 'GET', new FormData(), messagesRender, console.error)
}

// Message Rendering

function userMessageRender(message, time, clientUUId = '', addClass = '', send = false) {
    let hideClass = ' d-none'
    if (send) {
        hideClass = ''
    }
    return `
     <div class="message user-message${addClass} arrow" data-uuid="${clientUUId}">
        <div class="message-body col-12">
            <p>
                ${message}
            </p>
            <div class="time">${time} <span class="status">
                <svg width="18" height="10" viewBox="0 0 18 10" fill="none"
                     xmlns="http://www.w3.org/2000/svg">
                <path d="M11.7931 1.00035L4.63338 8.87886L1.142 5.53954" stroke="#EF5DA8"
                      stroke-linecap="round"
                      stroke-linejoin="round"/>
                <path class="sended${hideClass}" d="M16.7401 1.00006L9.57997 8.87898L6.98385 6.42009" stroke="#EF5DA8"
                      stroke-linecap="round"
                      stroke-linejoin="round"/>
                </svg>
            </span></div>
        </div>
    </div>
    `
}

function chatUserMessageRender(username, message, time) {
    return `
     <div class="message chat-message arrow">
        <div class="message-body">
            <p class="user-name">${username}</p>
            <p>${message}</p>
            <div class="time">${time}</div>
        </div>
    </div>
    `
}

// WebSocket

const chatSocket = new WebSocket(
    'ws://'
    + '127.0.0.1:8000'
    + '/ws/chat/'
    + ROOM_NAME
    + '/'
);


chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    if (data['type'] === 'chat_massage') {
        let chatListElem = document.getElementById('chat-list')
        if (data['user_id'] === CURRENT_USER_ID) {
            acceptMassage(data)
        } else {
            let date = convertTZ(new Date(data['created']), localTimeZone)
            let timeStr = moment(date).format('HH:mm')
            chatListElem.innerHTML = chatUserMessageRender(data['username'], data['message'], timeStr) + chatListElem.innerHTML
        }
    } else if (data['type'] === 'notification') {
        document.getElementById('room-users-count').textContent = data['users_count']
    }
};

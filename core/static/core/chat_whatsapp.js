let currentRecipient = '';
let chatInput = $('#input');
let messageList = $('#messages');
let scenarioInput = $("#scenario-input")
let userList = []; // latest_message,username
const beginRegex = new RegExp("Beginne Szenario \\d+$")
const terminateRegex = new RegExp('Szenario \\d+ beendet$');

// this will be used to store the date of the last message
// in the message area
let lastDate = "";

function fetchUserList() {
    $.getJSON('/api/v1/user/', function (data) {
        userList = data;
        drawUserList();
    });
}

function drawUserList() {
    $('#user-list').empty();
    // sort users based on latest message timestamp
    userList.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    for (let i = 0; i < userList.length; i++) {
        const msg = userList[i]['latest_message'];
        const userItem = `
            <div class="chat-list-item d-flex flex-row w-100 p-2 border-bottom${currentRecipient === userList[i]['username'] ? " active" : ""}" 
                onclick="onClickUserList(this, '${userList[i]['username']}')">
                <img src="${static_url}/img/profilepic.png" alt="Profile Photo" class="img-fluid rounded-circle mr-2" style="height:50px;">
                <div class="w-50">
                    <div class="name">${userList[i]['username']}</div>
                    <div class="small last-message">${msg ? msg.substr(0, 50) : ""}</div>
                </div>
                <div class="flex-grow-1 text-right">
                    <div class="small time">${showDateUserlist(userList[i]['timestamp'])}</div>
                </div>
            </div>`;
        $(userItem).appendTo('#user-list');
    }
}

function getTime(dateString) {
    if (!dateString) return ''
    let date = new Date(dateString);
    let dualize = (x) => x < 10 ? "0" + x : x;
    return dualize(date.getHours()) + ":" + dualize(date.getMinutes());
}

function showDateUserlist(dateString) {
    let weekdaydate = showDatesWeekDays(dateString);
    if (weekdaydate === 'TODAY')
        return getTime(dateString)
    return weekdaydate
}

function showDatesWeekDays(dateString) {
    if (!dateString) return ''
    const dt = new Date(dateString)
    let days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    let date_weekday = dt.toLocaleDateString();
    if (dt.toDateString() == new Date().toDateString()) {
        date_weekday = 'TODAY';
    } else if (dt > new Date(Date.now() - 604800000)) {
        // if date is greater than last 7 days date
        date_weekday = days[dt.getDay()].toUpperCase()
    }
    return date_weekday;
}

function drawMessage(message) {
    let msgDate = showDatesWeekDays(message.timestamp);
    let messageItem = '';
    if (lastDate != msgDate) {
        messageItem += `<div class="mx-auto my-2 bg-info text-white small py-1 px-2 rounded">
            ${msgDate}
        </div>`;
        lastDate = msgDate;
    }
    messageItem += `
    <div class="align-self-${message.user === currentUser ? "end self" : "start"} p-1 my-1 mx-3 rounded bg-white shadow-sm message-item">
        <div class="options">
            <a href="#"><i class="fas fa-angle-down text-muted px-2"></i></a>
        </div>
        <div class="d-flex flex-row">
            <div class="body m-1 mr-2">${message.body}</div>
            <div class="time ml-auto small text-right flex-shrink-0 align-self-end text-muted" style="width:75px;">
                ${getTime(message.timestamp)}
            </div>
        </div>
    </div>`;
    // alert(messageItem)
    $(messageItem).appendTo('#messages');
}

function drawScenarioMessage(message) {
    let messageItem = '';
    messageItem += `
    <div class="align-self-center p-1 my-1 mx-3 rounded bg-warning shadow-sm message-item">
        <div class="options">
            <a href="#"><i class="fas fa-angle-down text-muted px-2"></i></a>
        </div>
        <div class="d-flex flex-row">
            <div class="body m-1 mr-2">${message.body}</div>
        </div>
    </div>`;
    // alert(messageItem)
    $(messageItem).appendTo('#messages');
}

function onClickUserList(elem, recipient) {
    currentRecipient = recipient;
    $("#name").text(recipient);
    $.getJSON(`/api/v1/scenario/?target=${recipient}`, function (data) {
        let result = data['results'][0];
        if (result != null && result.sid > 0) {
            changeScenarioControlStart(result.sid)
        } else {
            changeScenarioControlEnd()
        }
    });
    sid = getSid();
    $.getJSON(`/api/v1/message/?target=${recipient}&sid=${sid}`, function (data) {
        messageList.empty(); // .children('.message-item').remove();
        $(".overlay").addClass("d-none");
        $("#input-area").removeClass("d-none").addClass("d-flex");

        $(".chat-list-item").removeClass("active");
        $(elem).addClass("active");
        lastDate = "";
        for (let i = data['results'].length - 1; i >= 0; i--) {
            let result = data['results'][i];
            let msg = result.body;
            if (beginRegex.test(msg) || terminateRegex.test(msg)) {
                drawScenarioMessage(result)
            } else {
                drawMessage(result);
            }
        }
        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });
}

function updateUserList(data) {
    // add latest message to userlist
    // id, user, recipient, timestamp, body
    let data_username = data.user;
    if (data.user === currentUser) {
        data_username = data.recipient;
    }

    const obj = userList.find(v => v.username === data_username); obj.latest_message = data.body; obj.timestamp = data.timestamp;

    drawUserList();
}
function getMessageById(message) {
    const msg_id = JSON.parse(message).message;
    $.getJSON(`/api/v1/message/${msg_id}/`, function (data) {
        if (data.user === currentRecipient ||
            (data.recipient === currentRecipient && data.user == currentUser)) {
            checkScenario(data);
            updateUserList(data);
        }
        messageList.animate({ scrollTop: messageList.prop('scrollHeight') });
    });
}

function checkScenario(message) {
    if (beginRegex.test(message.body)) {
        changeScenarioControlStart(message.sid);
        drawScenarioMessage(message);
    } else if (terminateRegex.test(message.body)) {
        changeScenarioControlEnd(message.sid);
        drawScenarioMessage(message);
    } else {
        drawMessage(message);
    }
}

function sendMessage() {
    const body = chatInput.val();
    if (!containsEmoji(body)) {
        alert('No Emoji Label selected!');
        return;
    }
    sid = getSid()
    if (body.length > 0) {
        $.post('/api/v1/message/', {
            recipient: currentRecipient,
            sid: sid,
            body: body
        }).fail(function () {
            alert('Error! Check console!');
        });
        chatInput.val('');
    }
}

function getSid() {
    if ($("#scenario-btn-stop").is(":visible")) {
        return scenarioInput.val();
    }
    return 0;
}

function containsEmoji(msg) {
    var emojis = ["😂", "🥰", "😱", "😲", "😢", "🤢", "😡", "👀"]
    if (emojis.some(emoji => msg.includes(emoji))) {
        return true;
    } else {
        return false;
    }
}

let showProfileSettings = () => {
    $("#profile-settings").css("left", 0); //.style.left = 0;
    // DOM.profilePic.src = user.pic;
    // DOM.inputName.value = user.name;
};

let hideProfileSettings = () => {
    $("#profile-settings").css("left", "-110%");
    // DOM.username.innerHTML = user.name;
};

function beginScenario() {
    let number = parseInt(scenarioInput.val())
    if (validateInput(number)) {
        let terminate = confirm("Möchtest du Szenario " + number + " starten?");
        if (terminate) {
            changeScenarioControlStart(number);
            $.post('/api/v1/scenario/', {
                recipient: currentRecipient,
                sid: number
            }).fail(function () {
                alert('Error! Check console!');
                return;
            });
            $.post('/api/v1/message/', {
                recipient: currentRecipient,
                sid: number,
                body: "Beginne Szenario " + number
            }).fail(function () {
                alert('Error! Check console!');
            });
        }
    } else {
        alert("Scenario mit dieser ID ist nicht vorhanden.")
    }
}

function changeScenarioControlStart(number) {
    $("#scenario-btn-start").hide();
    $("#scenario-btn-stop").show();
    $("#scenario-input").val(number)
    $("#scenario-input").prop("disabled", true);
}

function validateInput(number) {
    if (isNaN(number) || number < scenarioInput.attr('min') || number > scenarioInput.attr('max')) {
        return false;
    } else {
        return true;
    }
}

function terminateScenario() {
    let number = parseInt(scenarioInput.val())
    let terminate = confirm("Möchtest du das Szenario wirklich beenden?");
    if (terminate) {
        changeScenarioControlEnd();
        $.post('/api/v1/scenario/', {
            recipient: currentRecipient,
            sid: 0
        }).fail(function () {
            alert('Error! Check console!');
            return;
        });
        $.post('/api/v1/message/', {
            recipient: currentRecipient,
            sid: number,
            body: "Szenario " + number + " beendet"
        }).fail(function () {
            alert('Error! Check console!');
        });
    }
}

function changeScenarioControlEnd() {
    $("#scenario-btn-stop").hide();
    $("#scenario-btn-start").show();
    $("#scenario-input").prop("disabled", false);
}

function typeInTextarea(el, newText) {
    var start = el.prop("selectionStart")
    var end = el.prop("selectionEnd")
    var text = el.val()
    var before = text.substring(0, start)
    var after = text.substring(end, text.length)
    el.val(before + newText + after)
    el[0].selectionStart = el[0].selectionEnd = start + newText.length
    el.focus()
}

$(document).ready(function () {
    fetchUserList();
    // let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);

    let wsStart = 'ws://';
    if (window.location.protocol == 'https:') {
        wsStart = 'wss://'
    }
    var socket = new WebSocket(wsStart + window.location.host + `/ws?session_key=${sessionKey}`)

    chatInput.keypress(function (e) {
        if (e.keyCode == 13) sendMessage();
    });

    socket.onmessage = function (e) {
        getMessageById(e.data);
    };






    /* if the user click the conversation or the type panel will also hide the 

    panel */
    $("#messages").click(function () {
        $(".emojiBar").fadeOut(120);
    });

    /* put emoji to text are*/

    $(".emoji_single").click(function () {
        let $this = $(this).html();
        typeInTextarea($("#input"), $this);
    });
});


function login(msg) {
    axios({
        url: "https://mwu8afyoej.execute-api.us-east-1.amazonaws.com/pro/chatbot",
        method: 'post',
        data: {
            "message": msg
        },
        headers: {
            "X-Api-Key": "ULWGhZU9di3ZNELXYJXdBwJY22E5xPS5z5ghwKCh"
        }

    }).then(response => {
        console.log(response);
        addMessage(response.data.body);
    }).catch(error => {
        console.log(error)
    })
}

function addMessage(message){
    var d = $("<div class = 'cus'>" + message + "</div>");
    var chatArea = $(".chatBody");
    chatArea.append(d);
    var container = $(".chatBody");
    container.scrollTop = container.scrollHeight;
}

function sendMessage() {
    var msg = $(".msg").val();
    if(msg===""){
        alert("please enter some thing!");
        return;
    }
    addMessage(msg);
    $(".msg").val(null);
    login(msg);
}

$(".msg").keydown(function () {
    if (event.keyCode == "13") {
        sendMessage();
    }
});

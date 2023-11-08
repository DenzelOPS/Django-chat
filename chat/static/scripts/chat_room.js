const name = document.querySelector("#username_send_container").getAttribute("data-room-id");
const chatRoomId = document.querySelector("#id_message_send_container").getAttribute("data-room-id");
const chatSocket = new WebSocket("ws://" + window.location.host + "/chat-room/"+chatRoomId+"/");

chatSocket.onopen = function (e) {
  console.log("The connection was set up successfully!");
  document.querySelector("#id_message_send_input").focus();
};

chatSocket.onclose = function (e) {
  console.log("The WebSocket connection was closed unexpectedly.");
};

document.querySelector("#id_message_send_input").onkeyup = function (e) {
  if (e.keyCode == 13) {
    document.querySelector("#id_message_send_button").click();
  }
};

document.querySelector("#id_message_send_button").onclick = function (e) {
  var messageInput = document.querySelector("#id_message_send_input").value;
  if (chatSocket.readyState === WebSocket.OPEN) {
    chatSocket.send(JSON.stringify({ message: messageInput, username: name }));
  } else {
    console.log("WebSocket is not open. Message not sent.");
  }
};

chatSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
  
      if (data.chat_history) {
          // Handle chat history here
          data.chat_history.forEach(function (messageData) {
              var div = document.createElement("div");
              div.innerHTML = messageData.username + " : " + messageData.message;
              div.classList.add("message");
              document.querySelector("#id_message_send_input").value = "";
              document.querySelector("#id_chat_item_container").appendChild(div);
          });
      } else {
          var div = document.createElement("div");
          div.innerHTML = data.username + " : " + data.message;
          div.classList.add("message");
          document.querySelector("#id_message_send_input").value = "";
          document.querySelector("#id_chat_item_container").appendChild(div);
      }
  };
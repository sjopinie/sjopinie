"use strict";

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

const send_vote = function (event) {
  let btn = event;
  if (btn.target) btn = event.target.parentElement;
  let opinion_id = btn.id.split("-")[2];
  let vote_type = btn.id.split("-")[1];
  let vote_value = 0;
  if (vote_type == "up") vote_value = 1;
  else if (vote_type == "down") vote_value = -1;
  console.log("Sending vote " + vote_value + " for opinion: " + opinion_id);
  let request_body = JSON.stringify({
    opinion: opinion_id,
    value: vote_value,
  });

  fetch("/api/vote/", {
    method: "POST",
    headers: {
      Accept: "application/json, text/plain",
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: request_body,
  }).then((res) => console.log("Vote sent. Response code", res.status));
};

const link_buttons = function () {
  let buttons = document.getElementsByClassName("vote-btn");
  for (let btn of buttons) {
    btn.onclick = send_vote;
  }
};

link_buttons();

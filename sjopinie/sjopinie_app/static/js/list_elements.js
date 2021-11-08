"use strict";

const gen_list_member = (subject) =>
  `<tr onclick="location.href='/subject/${subject.id}'"  style="cursor: pointer;">
      <td><a href="/subject/${subject.id}"
          >${subject.name}</a></td>
      <td></td>
    </tr>`; //TODO proper click location

const load_btn = document.querySelector("#load-list");
const subject_list = new Vue({
  el: "#list-view",
  delimiters: ["{+", "+}"],
  data: {
    loaded_elements: 0,
    list_body: "",
  },
});

const load_list = function () {
  fetch("/api/subjects")
    .then((response) => response.json())
    .then((list) => {
      subject_list.loaded_elements = list.length;
      subject_list.list_body = "";
      list.forEach((element) => {
        console.log(element);
        subject_list.list_body += gen_list_member(element);
      });
    });
};

load_btn.addEventListener("click", load_list);

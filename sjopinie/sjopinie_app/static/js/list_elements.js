"use strict";

const gen_list_member = (subject) =>
  `<tr onclick="location.href='/subject/${subject.id}'"  style="cursor: pointer;">
      <td><a href="/subject/${subject.id}"
          >${subject.name}</a></td>
      <td></td>
    </tr>`; //TODO proper click location

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
      subject_list.loaded_elements = list.count;
      subject_list.list_body = "";
      list.results.forEach((element) => {
        console.log(element);
        subject_list.list_body += gen_list_member(element);
      });
    });
};

load_list();

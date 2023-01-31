"use strict";

const gen_list_member = (subject) => {
  let tags = "";
  for (const tag of subject.tags) {
    tags = tags + tag.name + ", ";
  }

  return `<tr onclick="location.href='/subject/${subject.id}'"  style="cursor: pointer;">
      <td><a href="/subject/${subject.id}"
          >${subject.name}</a></td>
      <td>${tags}</td>
    </tr>`; //TODO proper click location
};

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

const tags_list = new Vue({
  el: "#tags-view",
  data: {
    tags_list_body: "",
  },
}); //TODO show only popular tags

const load_tag_list = function () {
  fetch("/api/tags/")
    .then((response) => response.json())
    .then((list) => {
      tags_list.tags_list_body = "";
      list.results.forEach(
        (tag) =>
          (tags_list.tags_list_body += `<li><a href="/search/${tag.name}">${tag.name}</a></li>`)
      );
    });
};

load_tag_list();
load_list();

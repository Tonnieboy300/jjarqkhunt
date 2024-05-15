let autocomplete;

function initAutocomplete() {
  autocomplete = new google.maps.places.Autocomplete(
    document.getElementById("addr"),
    ["formatted_address"]
  );
}

function matchTags(input) {
  if (input == "") {
    return [];
  }
  var pattern = new RegExp(input);
  return tagList.filter(function (term) {
    if (term.match(pattern)) {
      return term;
    }
  });
}

function cleanString(value) {
  //remove whitespace
  value = value.replace(/\s/g, "");
  //split each tag into its own string
  value = value.split(",");
  return value;
}

function tagAutocomplete(value) {
  tagBox = document.getElementById("tags");
  //force value to be lowercase
  value = value.toLowerCase();
  tagBox.value = tagBox.value.toLowerCase();
  value = cleanString(value);
  //only get the last value
  value = value[value.length - 1];
  console.log(value);
  completeBox = document.getElementById("tagAuto");
  completeBox.innerHTML = "";
  let results = "";
  let tags = matchTags(value);
  for (i = 0; i < tags.length; i++) {
    results +=
      "<li onclick=\"autofillTag('" + tags[i] + "')\">" + tags[i] + "</li>";
  }
  completeBox.innerHTML = "<ul>" + results + "</ul>";
}

function autofillTag(value) {
  tagBox = document.getElementById("tags");
  currentText = cleanString(tagBox.value);
  currentText[currentText.length - 1] = value;
  tagBox.value = "";
  for (const item of currentText) {
    tagBox.value += item + ", ";
  }
  tagAutocomplete("");
}

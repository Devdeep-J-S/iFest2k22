function toggleDisplay() {
  arg = event.target.getAttribute("arg");
  const targetData = document.getElementById(arg);
  if (targetData.style.display !== "none") {
    targetData.style.display = "none";
  } else {
    targetData.style.display = "flex";
  }
}

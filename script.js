document.getElementById("topsis-form").addEventListener("submit", function (e) {

  let weights = document.querySelector("input[name='weights']").value.trim();
  let impacts = document.querySelector("input[name='impacts']").value.trim();
  let errorBox = document.getElementById("error-message");

  errorBox.style.display = "none";
  errorBox.innerText = "";

  let weightsArray = weights.split(",");
  let impactsArray = impacts.split(",");

  if (weightsArray.length !== impactsArray.length) {
    e.preventDefault();
    errorBox.innerText = "Number of weights and impacts must match.";
    errorBox.style.display = "block";
    return;
  }

  for (let i = 0; i < impactsArray.length; i++) {
    if (impactsArray[i].trim() !== "+" && impactsArray[i].trim() !== "-") {
      e.preventDefault();
      errorBox.innerText = "Impacts must contain only '+' or '-' symbols.";
      errorBox.style.display = "block";
      return;
    }
  }
});

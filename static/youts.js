var youtsMetadata;
var currentToken = 0;

$(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() > $(document).height() - 950) {
        loadMore(40)
    }
});

$(document).ready(function() {
    youtsMetadata = fetch('/static/youts-metadata.json')
      .then(response => response.json())
      .then((data) => {
          youtsMetadata = data;
          loadMore(40);
      })
      .catch(error => console.log(error));
})

function loadMore(loadAmount) {
    var totalYouts = Object.keys(youtsMetadata).length
    
    if (totalYouts < currentToken + loadAmount) {
        loadAmount = totalYouts - currentToken
    }

    for (var i = currentToken; i < currentToken + loadAmount; i++) {
        yout = youtsMetadata[i]
        var traitsString = ``

        for (var index in yout.attributes) {
            var trait = yout.attributes[index];
            traitsString += `
                <p><b>${trait.trait_type}:</b> ${trait.value}</p>
            `
        }

        var cardString = `
            <div class="card">
                <div class="token-image">
                    <img src=${yout.image}>
                </div>
                <div class="token-traits">
                    <h1>Yout #${i}</h1>
                    ${traitsString}
            </div>
        `
        $("#tokens").append(cardString)
    }
    currentToken = currentToken + loadAmount;
}
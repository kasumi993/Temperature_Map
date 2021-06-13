fetch('../citation.json')
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    appendData(data);
  })
  .catch(function (err) {
    console.log(err);
  });

compteur=0;

function appendData(data) {
    setInterval(function() {
        document.getElementById('citations').innerHTML = data[compteur].citation;
        if (compteur==4){
            compteur=-1
        }
        compteur++;
    }, 5000);
    
}





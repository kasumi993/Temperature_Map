 // Creation d'une carte dans la balise div "map", et positionne la vue sur un point donné et un niveau de zoom
 var map = L.map('map').setView([46.5,2.5], 5);
 // Ajout d'une couche de dalles OpenStreetMap
 L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
 attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);
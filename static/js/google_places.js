// This example adds a search box to a map, using the Google Place Autocomplete
// feature. People can enter geographical searches. The search box will return a
// pick list containing a mix of places and predicted search terms.
// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">
function initAutocomplete() {
  let autocomplete;
  let address1Field;
  let address2Field;
  let postalField;
  
  const map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 39.9334, lng: 32.8597 },
    zoom: 13,
    mapTypeId: "roadmap",
  });
  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  google.maps.event.trigger(map, "resize")
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });
  let markers = [];
  google.maps.event.trigger(map, "resize")
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    let address1 = "";
    let postcode = "";
    const places = searchBox.getPlaces();
    console.log();
    document.querySelector("#formatted_address").value = "";
    document.querySelector("#name").value = "";
    document.querySelector("#formatted_phone_number").value = "";
    document.querySelector("#place_id").value = "";
    document.querySelector("#website").value = "";
    document.querySelector("#rating").value = "";
    document.querySelector("#type").value = "";
    document.querySelector("#photo").value = "";
    if (places.length == 0) {
      return;
    }

    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];

    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();

    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }

      const icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25),
      };

      // Create a marker for each place.
      markers.push(
        new google.maps.Marker({
          map,
          icon,
          title: place.name,
          position: place.geometry.location,
        })
      );
      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
    console.log(places)
    console.log(places[0].name)
    document.querySelector("#formatted_address").value = places[0].formatted_address;
    document.querySelector("#name").value = places[0].name;
    document.querySelector("#formatted_phone_number").value = places[0].formatted_phone_number;
    document.querySelector("#place_id").value = places[0].place_id;
    document.querySelector("#website").value = places[0].website;
    document.querySelector("#rating").value = places[0].rating; //htmle ekle
    document.querySelector("#type").value = places[0].types[0];//htmle ekle
    document.querySelector("#photo").value = places[0].photos[0].getUrl();
    document.querySelector("#longtitude").value = places[0].geometry.location.lng();
    document.querySelector("#latitude").value = places[0].geometry.location.lat();
  });

}




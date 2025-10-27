// Get current location functionality
async function getCurrentLocation() {
  const addressField = document.getElementById('delivery-address');
  const locationBtn = document.querySelector('.location-btn');
  
  if ('geolocation' in navigator) {
    locationBtn.innerHTML = '<i class="bi bi-arrow-repeat spin me-2"></i>Getting Location...';
    locationBtn.disabled = true;
    
    const options = {
      enableHighAccuracy: true,
      timeout: 10000,
      maximumAge: 0
    };
    
    navigator.geolocation.getCurrentPosition(
      async function(position) {
        const lat = position.coords.latitude;
        const lng = position.coords.longitude;
        
        console.log('Coordinates:', lat, lng);
        
        try {
          // Call reverse geocoding API to get readable address
          const address = await reverseGeocode(lat, lng);
          
          addressField.value = address;
          
          // Store coordinates in hidden fields if you need them
          if (document.getElementById('latitude')) {
            document.getElementById('latitude').value = lat;
          }
          if (document.getElementById('longitude')) {
            document.getElementById('longitude').value = lng;
          }
          
          locationBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Location Added';
          locationBtn.disabled = false;
          
          setTimeout(() => {
            locationBtn.innerHTML = '<i class="bi bi-geo-alt me-2"></i>Use Current Location';
          }, 2000);
          
        } catch (error) {
          console.error('Geocoding error:', error);
          addressField.value = `Coordinates: ${lat.toFixed(6)}, ${lng.toFixed(6)}\n(Unable to get address. Please enter manually)`;
          
          locationBtn.innerHTML = '<i class="bi bi-check-circle me-2"></i>Coordinates Added';
          locationBtn.disabled = false;
          
          setTimeout(() => {
            locationBtn.innerHTML = '<i class="bi bi-geo-alt me-2"></i>Use Current Location';
          }, 2000);
        }
      },
      function(error) {
        console.error('Geolocation error:', error);
        
        let errorMsg = 'Location access failed. ';
        switch(error.code) {
          case error.PERMISSION_DENIED:
            errorMsg += 'Please enable location permissions.';
            break;
          case error.POSITION_UNAVAILABLE:
            errorMsg += 'Location unavailable.';
            break;
          case error.TIMEOUT:
            errorMsg += 'Request timed out.';
            break;
        }
        
        alert(errorMsg);
        
        locationBtn.innerHTML = '<i class="bi bi-exclamation-triangle me-2"></i>Location Failed';
        setTimeout(() => {
          locationBtn.innerHTML = '<i class="bi bi-geo-alt me-2"></i>Use Current Location';
          locationBtn.disabled = false;
        }, 2000);
      },
      options
    );
  } else {
    alert('Geolocation is not supported by this browser.');
  }
}

// Reverse geocode coordinates to readable address
async function reverseGeocode(lat, lng) {
  // Using OpenStreetMap Nominatim API (Free, no API key needed)
  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`;
  
  const response = await fetch(url, {
    headers: {
      'User-Agent': 'GroceryApp/1.0' // Required by Nominatim
    }
  });
  
  if (!response.ok) {
    throw new Error('Geocoding service unavailable');
  }
  
  const data = await response.json();
  
  if (data && data.display_name) {
    // Return the formatted address
    return data.display_name;
  } else if (data && data.address) {
    // Build a custom formatted address from components
    const addr = data.address;
    let formattedAddress = '';
    
    if (addr.house_number) formattedAddress += addr.house_number + ' ';
    if (addr.road) formattedAddress += addr.road + ', ';
    if (addr.suburb) formattedAddress += addr.suburb + ', ';
    if (addr.city) formattedAddress += addr.city + ', ';
    if (addr.state) formattedAddress += addr.state + ' ';
    if (addr.postcode) formattedAddress += addr.postcode + ', ';
    if (addr.country) formattedAddress += addr.country;
    
    return formattedAddress || data.display_name;
  }
  
  throw new Error('No address found');
}
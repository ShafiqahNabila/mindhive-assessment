// Initialize the map
const map = L.map('map').setView([3.1390, 101.6869], 12); // Centered on Kuala Lumpur

// Add a tile layer (CartoDB Positron for a modern look)
L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors, © CartoDB'
}).addTo(map);

// Enable panning and zooming
map.dragging.enable();
map.touchZoom.enable();
map.doubleClickZoom.enable();
map.scrollWheelZoom.disable();

// Function to calculate distance between two coordinates (in kilometers)
function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371; // Radius of the Earth in km
    const dLat = (lat2 - lat1) * (Math.PI / 180);
    const dLon = (lon2 - lon1) * (Math.PI / 180);
    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in km
}

// Custom marker icon for Subway outlets
const subwayIcon = L.icon({
    iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png', // Green marker icon
    iconSize: [25, 41], // Default marker size
    iconAnchor: [12, 41], // Default anchor point
    popupAnchor: [1, -34] // Default popup anchor
});

// Calculate bounds to include all outlets
let outletBounds = L.latLngBounds();

// Fetch outlet data from the API
fetch('http://127.0.0.1:8000/outlets')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        const outlets = data.outlets;

        // Add markers for each outlet
        outlets.forEach(outlet => {
            const { latitude, longitude, name, address, operating_hours, waze_link } = outlet;

            // Check if latitude and longitude are valid
            if (latitude && longitude) {
                // Extend bounds to include each outlet
                outletBounds.extend([latitude, longitude]);

                // Add a marker with the custom Subway icon
                const marker = L.marker([latitude, longitude], { icon: subwayIcon }).addTo(map);

                // Add a popup with enhanced styling
                marker.bindPopup(`
                    <div style="text-align: center;">
                        <h3 style="margin: 0; color: #00704A;">${name}</h3>
                        <p style="margin: 5px 0; color: #555;">${address}</p>
                        <p style="margin: 5px 0; color: #555;">Operating Hours: ${operating_hours}</p>
                        <a href="${waze_link}" target="_blank" style="color: #00704A; text-decoration: none;">Open in Waze</a>
                    </div>
                `);

                // Check for intersecting outlets
                outlets.forEach(otherOutlet => {
                    if (otherOutlet.id !== outlet.id && otherOutlet.latitude && otherOutlet.longitude) {
                        const distance = calculateDistance(
                            latitude, longitude,
                            otherOutlet.latitude, otherOutlet.longitude
                        );
                        if (distance <= 5) {
                            // Add a small red circle to indicate intersection
                            L.circleMarker([otherOutlet.latitude, otherOutlet.longitude], {
                                radius: 6, // Smaller size for intersection circles
                                fillColor: 'red',
                                color: 'darkred',
                                weight: 1,
                                opacity: 1,
                                fillOpacity: 0.8
                            }).addTo(map);
                        }
                    }
                });
            } else {
                console.warn(`Skipping outlet ${outlet.id}: Invalid coordinates (${latitude}, ${longitude})`);
            }
        });

        // Set max bounds to include all outlets with padding
        map.setMaxBounds(outletBounds.pad(0.5)); // Add 50% padding
    })
    .catch(error => console.error('Error fetching outlet data:', error));

// Add a "Return to KL" button
const returnToKLButton = L.control({ position: 'topleft' });

returnToKLButton.onAdd = function (map) {
    const div = L.DomUtil.create('div', 'return-to-kl');
    div.innerHTML = '<button>Return to KL</button>';
    div.addEventListener('click', () => {
        map.flyTo([3.1390, 101.6869], 12); // Fly to KL center
    });
    return div;
};

returnToKLButton.addTo(map);

// Add zoom control
L.control.zoom({ position: 'topright' }).addTo(map);

// Add scale bar
L.control.scale({ position: 'bottomleft' }).addTo(map);

// Chatbot Functionality
document.getElementById('search-button').addEventListener('click', () => {
    const query = document.getElementById('search-box').value;
    handleQuery(query);
});

document.getElementById('search-box').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const query = document.getElementById('search-box').value;
        handleQuery(query);
    }
});

// Function to handle user queries
function handleQuery(query) {
    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = ''; // Clear previous results

    const normalizedQuery = query.toLowerCase().trim();

    fetch('http://127.0.0.1:8000/outlets')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log('API Response:', data); // Log the API response for debugging
            const outlets = data.outlets;

            if (normalizedQuery.includes('close the latest')) {
                const latestClosingOutlets = findOutletsThatCloseLatest(outlets);
                displayResults(latestClosingOutlets, 'Outlets that close the latest:');
            } else if (normalizedQuery.includes('how many outlets') && normalizedQuery.includes('bangsar')) {
                const bangsarOutlets = countOutletsInLocation(outlets, 'Bangsar');
                displayResults(bangsarOutlets, `Number of outlets in Bangsar: ${bangsarOutlets.length}`);
            } else {
                resultsDiv.innerHTML = '<p>Sorry, I couldn\'t understand your query. Try asking something like:<br>1. "Which outlets close the latest?"<br>2. "How many outlets are in Bangsar?"</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
            resultsDiv.innerHTML = `<p>Error: ${error.message}. Please try again later.</p>`;
        });
}

// Function to find outlets that have the latest closing hours
function findOutletsThatCloseLatest(outlets) {
    // Normalize and extract all closing times
    const closingTimes = outlets.map(outlet => {
        const time = getClosingTime(outlet.operating_hours);
        return convertTo24Hour(time); // Convert to 24-hour format for consistent comparison
    });

    // Find the latest closing time
    const latestClosingTime = closingTimes.reduce((latest, time) => {
        return time > latest ? time : latest;
    }, '00:00'); // Default to '00:00' if no valid times are found

    // Filter all outlets that match the latest closing time
    return outlets.filter(outlet => {
        const outletClosingTime = convertTo24Hour(getClosingTime(outlet.operating_hours));
        return outletClosingTime === latestClosingTime;
    });
}

// Function to extract closing time from operating hours
function getClosingTime(operatingHours) {
    const parts = operatingHours.split(' - ');
    if (parts.length === 2) {
        return parts[1].trim(); // Trim any extra spaces
    }
    return '00:00'; // Default value if operating hours are invalid
}

// Function to convert 12-hour time to 24-hour format
function convertTo24Hour(time) {
    const [timePart, modifier] = time.split(' ');
    let [hours, minutes] = timePart.split(':');
    if (modifier === 'PM' && hours !== '12') {
        hours = parseInt(hours, 10) + 12;
    }
    if (modifier === 'AM' && hours === '12') {
        hours = '00';
    }
    return `${hours}:${minutes}`;
}

// Function to count outlets in a specific location
function countOutletsInLocation(outlets, location) {
    return outlets.filter(outlet => 
        outlet.address.toLowerCase().includes(location.toLowerCase())
    );
}

// Function to display results
function displayResults(results, title) {
    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = `<h3>${title}</h3>`;

    if (results.length === 0) {
        resultsDiv.innerHTML += '<p>No results found.</p>';
    } else {
        const ul = document.createElement('ul');
        results.forEach(result => {
            const li = document.createElement('li');
            li.textContent = result.name;
            ul.appendChild(li);
        });
        resultsDiv.appendChild(ul);
    }
}
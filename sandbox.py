import folium

# Coordinates for Minneapolis
latitude = 44.9778
longitude = -93.2650
zoom = 12

# List of marker coordinates and colors
marker_data = [
    ((44.9778, -93.2650), 'blue'),  # Minneapolis, blue marker
    ((45.5200, -122.6819), 'green'),  # Portland, green marker
    ((34.0522, -118.2437), 'red')  # Los Angeles, red marker
]

# Create a black and white map
map = folium.Map(location=[latitude, longitude], zoom_start=zoom, tiles='Stamen Toner')

# Add markers with different colors
for marker_coord, color in marker_data:
    folium.Marker(marker_coord, icon=folium.Icon(color=color)).add_to(map)

# Save the map to an HTML file
map.save("custom_map.html")

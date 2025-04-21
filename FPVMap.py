import requests
import folium
import json

def main():
    # Define your bounding box: (south, west, north, east)
    bbox = (48.510600, 14.364291, 48.512721, 14.368304)

    # Overpass API query to get nodes and ways with house numbers
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["addr:housenumber"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      way["addr:housenumber"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out center;
    """

    # Send the request
    response = requests.post(overpass_url, data=overpass_query)
    data = response.json()

    # # Extract and print address data
    # print("Found addresses:")
    # for element in data["elements"]:
    #     tags = element.get("tags", {})
    #     house_number = tags.get("addr:housenumber")
    #     street = tags.get("addr:street")
    #     city = tags.get("addr:city")
    #     postcode = tags.get("addr:postcode")
    #
    #     if house_number and street:
    #         address = f"{street} {house_number}"
    #         if postcode and city:
    #             address += f", {postcode} {city}"
    #         elif city:
    #             address += f", {city}"
    #         print(address)

    # Initialize the folium map
    center_lat = (bbox[0] + bbox[2]) / 2
    center_lon = (bbox[1] + bbox[3]) / 2
    map_osm = folium.Map(location=[center_lat, center_lon], zoom_start=16)

    # Add circles for each address
    for element in data["elements"]:
        tags = element.get("tags", {})
        lat = element.get("lat") or element.get("center", {}).get("lat")
        lon = element.get("lon") or element.get("center", {}).get("lon")

        if lat and lon:
            house_number = tags.get("addr:housenumber", "")
            street = tags.get("addr:street", "")
            popup_text = f"{street} {house_number}".strip()
            folium.Circle(
                location=[lat, lon],
                radius=200,  # meters
                color='red',
                fill=True,
                fill_opacity=0.5,
                popup=popup_text
            ).add_to(map_osm)

    # Save the map to an HTML file
    map_osm.save("addresses_map.html")
    print("Map saved to addresses_map.html")


if __name__ == "__main__":
    main()
import { FLS } from "@js/common/functions.js";
import { setOptions, importLibrary } from "@googlemaps/js-api-loader";
import { MAP_STYLES, BREAKPOINTS, MAP_KEY } from "./_settings.js";

import "./map.scss";

function mapInit() {
  const SELECTORS = {
    section: "[data-fls-map]",
    marker: "[data-fls-map-marker]",
    map: "[data-fls-map-body]",
  };

  const $sections = document.querySelectorAll(SELECTORS.section);
  if (!$sections.length) return;

  const loadMap = async (onLoad) => {
    try {
      setOptions({
        apiKey: MAP_KEY,
        version: "weekly",
      });

      const { Map } = await importLibrary("maps");
      const marker = new Marker({
        map,
        position: { lat, lng },
        title,
      });

      onLoad({ Map });
    } catch (e) {
      FLS("_FLS_MAP_ERROR");
      console.log(e);
    }
  };

  const initMap = async ({
    api,
    lng,
    lat,
    markersData,
    zoom,
    maxZoom,
    $map,
  }) => {
    const mapOptions = {
      maxZoom,
      zoom,
      mapTypeControl: false,
      styles: MAP_STYLES,
      center: { lat, lng },
      disableDefaultUI: true,
    };

    const map = new api.Map($map, mapOptions);

    markersData.forEach(({ lat, lng, title, markerZoom, markerPopup }) => {
      const marker = new google.maps.Marker({
        map,
        position: { lat, lng },
        title,
      });

      marker.addListener("click", () => {
        if (markerZoom.enable) {
          map.setZoom(+markerZoom.value || 10);
        }

        if (markerPopup.enable && window.flsPopup) {
          window.flsPopup.open(markerPopup.value);
        }

        map.panTo(marker.getPosition());
      });
    });

    return map;
  };

  loadMap((api) => {
    $sections.forEach(($section) => {
      const $maps = $section.querySelectorAll(SELECTORS.map);
      if (!$maps.length) return;

      $maps.forEach(($map) => {
        const $markers = $map.parentElement.querySelectorAll(SELECTORS.marker);

        const markersData = Array.from($markers).map(($marker) => ({
          lng: parseFloat($marker.dataset.flsMapLng) || 0,
          lat: parseFloat($marker.dataset.flsMapLat) || 0,
          title: $marker.dataset.flsMapTitle,
          markerZoom: {
            enable: $marker.hasAttribute("data-fls-map-marker-zoom"),
            value: $marker.dataset.flsMapMarkerZoom,
          },
          markerPopup: {
            enable: $marker.hasAttribute("data-fls-map-marker-popup"),
            value: $marker.dataset.flsMapMarkerPopup,
          },
        }));

        initMap({
          api,
          $map,
          lng: parseFloat($map.dataset.flsMapLng) || 0,
          lat: parseFloat($map.dataset.flsMapLat) || 0,
          zoom: parseFloat($map.dataset.flsMapZoom) || 6,
          maxZoom: parseFloat($map.dataset.flsMapMaxZoom) || 18,
          markersData,
        });
      });
    });
  });
}

document.querySelector("[data-fls-map]")
  ? window.addEventListener("load", mapInit)
  : null;

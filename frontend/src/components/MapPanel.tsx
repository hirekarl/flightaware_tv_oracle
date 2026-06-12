import 'leaflet/dist/leaflet.css';
import L from 'leaflet';
import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerIcon2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';
import { useEffect, useRef, useState } from 'react';
import { JFK_AIRCRAFT } from '../mocks/jfkTelemetry';
import type { JFKAircraft } from '../mocks/jfkTelemetry';

delete (L.Icon.Default.prototype as unknown as Record<string, unknown>)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconUrl: markerIcon,
  iconRetinaUrl: markerIcon2x,
  shadowUrl: markerShadow,
});

const NUDGE = 0.00015;

function isInternational(ac: JFKAircraft): boolean {
  return (
    ac.altitudeFt > 30000 &&
    (!ac.origin.startsWith('K') || !ac.destination.startsWith('K'))
  );
}

function statusColor(ac: JFKAircraft): string {
  if (isInternational(ac)) return '#00CFFF';
  switch (ac.status) {
    case 'Taxiing':
      return '#FFFFFF';
    case 'On Approach':
      return '#39FF14';
    case 'On Time':
      return '#4A90D9';
    case 'Delayed':
      return '#F5A623';
    case 'Departed':
      return '#39FF14';
    case 'Landed':
      return '#888888';
  }
}

function makeIcon(ac: JFKAircraft): L.DivIcon {
  const color = statusColor(ac);
  return L.divIcon({
    className: '',
    html: `
      <div class="aircraft-marker">
        <div class="aircraft-icon" style="transform:rotate(${ac.heading}deg);color:${color};filter:drop-shadow(0 0 6px ${color});">✈</div>
        <div class="aircraft-label">${ac.flightId}</div>
      </div>`,
    iconSize: [40, 40],
    iconAnchor: [20, 20],
  });
}

function tooltipHtml(ac: JFKAircraft): string {
  return `<span>${ac.flightId}&nbsp;&nbsp;•&nbsp;&nbsp;${ac.aircraftType}</span><br/>${ac.originCity} → ${ac.destinationCity}<br/>Status: ${ac.status}<br/>ETA: ${ac.eta}<br/>Alt: ${ac.altitudeFt.toLocaleString()}ft&nbsp;&nbsp;•&nbsp;&nbsp;${ac.speedKnots}kts`;
}

const MARKER_STYLE = `
.aircraft-marker{display:flex;flex-direction:column;align-items:center;cursor:pointer;}
.aircraft-icon{font-size:20px;line-height:1;}
.aircraft-label{font-size:9px;font-family:monospace;color:#ffffff;margin-top:2px;text-shadow:0 0 3px #000000;white-space:nowrap;}
.leaflet-tooltip.aircraft-tooltip{background:#1a2f4a!important;border:1px solid #4A90D9!important;color:#ffffff!important;font-family:monospace!important;font-size:12px!important;padding:8px 12px!important;border-radius:4px!important;white-space:nowrap!important;box-shadow:0 0 12px rgba(74,144,217,0.4)!important;}
.leaflet-tooltip.aircraft-tooltip::before{border-top-color:#4A90D9!important;}
`;

export default function MapPanel() {
  const mapRef = useRef<L.Map | null>(null);
  const markerRefs = useRef<Record<string, L.Marker>>({});
  const [positions, setPositions] = useState<Record<string, JFKAircraft>>(() =>
    Object.fromEntries(JFK_AIRCRAFT.map((ac) => [ac.flightId, { ...ac }]))
  );

  useEffect(() => {
    if (mapRef.current) return;
    const container = document.getElementById('jfk-map');
    if (!container) return;

    let map: L.Map;
    try {
      map = L.map('jfk-map', {
        center: [40.6413, -73.7781],
        zoom: 13,
        minZoom: 13,
        maxZoom: 16,
        scrollWheelZoom: false,
        dragging: false,
        zoomControl: false,
        doubleClickZoom: false,
        touchZoom: false,
        keyboard: false,
        boxZoom: false,
      });

      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap contributors © CARTO',
      }).addTo(map);

      JFK_AIRCRAFT.forEach((ac) => {
        const marker = L.marker([ac.lat, ac.lon], { icon: makeIcon(ac) })
          .addTo(map)
          .bindTooltip(tooltipHtml(ac), {
            permanent: false,
            direction: 'top',
            offset: [0, -10],
            className: 'aircraft-tooltip',
          });
        markerRefs.current[ac.flightId] = marker;
      });

      mapRef.current = map;
    } catch {
      // Leaflet cannot initialize in non-browser environments (e.g. jsdom)
    }
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      setPositions((prev) => {
        const next = { ...prev };
        Object.values(next).forEach((pos) => {
          const headingRad = (pos.heading * Math.PI) / 180;
          const newLat = pos.lat + Math.cos(headingRad) * pos.speedKnots * NUDGE;
          const newLon = pos.lon + Math.sin(headingRad) * pos.speedKnots * NUDGE;
          const newHeading = pos.heading + (Math.random() - 0.5) * 3;
          next[pos.flightId] = {
            ...pos,
            lat: newLat,
            lon: newLon,
            heading: newHeading,
          };

          const marker = markerRefs.current[pos.flightId];
          if (marker) {
            marker.setLatLng([newLat, newLon]);
            marker.setIcon(makeIcon(next[pos.flightId]));
            marker.setTooltipContent(tooltipHtml(next[pos.flightId]));
          }
        });
        return next;
      });
    }, 10000);

    return () => clearInterval(intervalId);
  }, []);

  // suppress unused-variable warning — positions drives marker updates via setPositions
  void positions;

  return (
    <div data-testid="map-panel" style={{ width: '100%', height: '100%' }}>
      <style>{MARKER_STYLE}</style>
      <div
        id="jfk-map"
        style={{ width: '100%', height: '100%', background: '#0a1628' }}
      />
    </div>
  );
}

import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { useEffect, useRef } from 'react';
import { JFK_AIRCRAFT } from '../mocks/jfkTelemetry';
import type { JFKAircraft } from '../mocks/jfkTelemetry';
import type { FlightState } from '../types/flight';

interface Props {
  flights?: FlightState[];
}

function esc(s: string): string {
  return s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

const NUDGE = 0.00015;

// Exact FlightAware color palette applied per vector tile layer
const FA_STYLE: maplibregl.StyleSpecification = {
  version: 8,
  sources: {
    ofm: {
      type: 'vector',
      url: 'https://tiles.openfreemap.org/planet',
    },
  },
  layers: [
    { id: 'bg', type: 'background', paint: { 'background-color': '#294E8C' } },
    {
      id: 'water',
      type: 'fill',
      source: 'ofm',
      'source-layer': 'water',
      paint: { 'fill-color': '#1A3265' },
    },
    {
      id: 'waterway',
      type: 'line',
      source: 'ofm',
      'source-layer': 'waterway',
      paint: { 'line-color': '#1A3265', 'line-width': 1 },
    },
    {
      id: 'aeroway-apron',
      type: 'fill',
      source: 'ofm',
      'source-layer': 'aeroway',
      filter: ['==', ['get', 'class'], 'apron'],
      paint: { 'fill-color': '#3A3A50' },
    },
    {
      id: 'aeroway-runway',
      type: 'line',
      source: 'ofm',
      'source-layer': 'aeroway',
      filter: ['==', ['get', 'class'], 'runway'],
      paint: { 'line-color': '#4A5580', 'line-width': 4 },
    },
    {
      id: 'aeroway-taxiway',
      type: 'line',
      source: 'ofm',
      'source-layer': 'aeroway',
      filter: ['==', ['get', 'class'], 'taxiway'],
      paint: { 'line-color': '#4A5580', 'line-width': 1.5 },
    },
    {
      id: 'road',
      type: 'line',
      source: 'ofm',
      'source-layer': 'transportation',
      paint: { 'line-color': '#2A3E6B', 'line-width': 0.8, 'line-opacity': 0.7 },
    },
  ],
};

function statusColor(ac: JFKAircraft, live?: FlightState): string {
  if (live) {
    if (live.operationalStatus === 'CRITICAL') return '#FF3B3B';
    if (live.operationalStatus === 'WARNING') return '#FFB800';
    return '#39FF14';
  }
  if (ac.status === 'Taxiing' || ac.status === 'Landed') return '#FFD700';
  return '#39FF14';
}

function makeIconHtml(ac: JFKAircraft, live?: FlightState): string {
  const color = statusColor(ac, live);
  return `<div class="aircraft-marker">
    <div class="aircraft-icon" style="transform:rotate(${ac.heading}deg);color:${color};filter:drop-shadow(0 0 6px ${color});">✈</div>
    <div class="aircraft-label">${esc(ac.flightId)}</div>
  </div>`;
}

function tooltipHtml(ac: JFKAircraft, live?: FlightState): string {
  const statusLine = live
    ? `${esc(live.operationalStatus)}${live.deviationType !== 'NONE' ? ` · ${esc(live.deviationType.replace(/_/g, ' '))}` : ''}`
    : esc(ac.status);
  const aiLine =
    live && live.aiAnalysis.summaryTitle !== 'None'
      ? `<br/><span style="color:#00A0E2;font-style:italic">${esc(live.aiAnalysis.summaryTitle)}</span>`
      : '';
  return (
    `<span>${esc(ac.flightId)}&nbsp;&nbsp;•&nbsp;&nbsp;${esc(ac.aircraftType)}</span>` +
    `<br/>${esc(ac.originCity)} → ${esc(ac.destinationCity)}` +
    `<br/>Status: ${statusLine}` +
    `<br/>ETA: ${esc(ac.eta)}&nbsp;&nbsp;•&nbsp;&nbsp;Alt: ${ac.altitudeFt.toLocaleString()}ft` +
    aiLine
  );
}

const MARKER_STYLE = `
.aircraft-marker{display:flex;flex-direction:column;align-items:center;cursor:pointer;}
.aircraft-icon{font-size:20px;line-height:1;}
.aircraft-label{font-size:9px;font-family:monospace;color:#ffffff;margin-top:2px;text-shadow:0 0 3px rgba(0,0,0,0.8);white-space:nowrap;}
.kjfk-label{color:#ffffff;font-family:monospace;font-size:13px;font-weight:700;letter-spacing:0.1em;text-shadow:0 0 6px rgba(0,0,0,0.8);white-space:nowrap;pointer-events:none;}
.aircraft-popup .maplibregl-popup-content{background:#0C1929!important;border:1px solid #00A0E2!important;color:#ffffff!important;font-family:monospace!important;font-size:12px!important;padding:8px 12px!important;border-radius:4px!important;white-space:nowrap!important;box-shadow:0 0 12px rgba(0,160,226,0.4)!important;}
.aircraft-popup .maplibregl-popup-tip{border-top-color:#00A0E2!important;}
.maplibregl-popup-close-button{display:none;}
`;

export default function MapPanel({ flights = [] }: Props) {
  const mapRef = useRef<maplibregl.Map | null>(null);
  const markerRefs = useRef<Record<string, maplibregl.Marker>>({});
  const popupRefs = useRef<Record<string, maplibregl.Popup>>({});
  const positionsRef = useRef<Record<string, JFKAircraft>>(
    Object.fromEntries(JFK_AIRCRAFT.map((ac) => [ac.flightId, { ...ac }]))
  );
  // Always holds the latest live fleet keyed by flightId
  const liveFleetRef = useRef<Map<string, FlightState>>(new Map());

  // Sync live fleet ref and immediately re-color matching markers
  useEffect(() => {
    liveFleetRef.current = new Map(flights.map((f) => [f.flightId, f]));
    Object.values(positionsRef.current).forEach((pos) => {
      const marker = markerRefs.current[pos.flightId];
      if (marker) {
        marker.getElement().innerHTML = makeIconHtml(
          pos,
          liveFleetRef.current.get(pos.flightId)
        );
      }
    });
  }, [flights]);

  useEffect(() => {
    if (mapRef.current) return;
    const container = document.getElementById('jfk-map');
    if (!container) return;

    let map: maplibregl.Map | null = null;
    try {
      map = new maplibregl.Map({
        container: 'jfk-map',
        style: FA_STYLE,
        center: [-73.7781, 40.6413],
        zoom: 13,
        minZoom: 13,
        maxZoom: 16,
        interactive: false,
        attributionControl: false,
      });

      map.on('load', () => {
        if (!map) return;
        const liveMap = map;

        // KJFK airport label
        const kjfkEl = document.createElement('div');
        kjfkEl.className = 'kjfk-label';
        kjfkEl.textContent = 'KJFK';
        new maplibregl.Marker({ element: kjfkEl })
          .setLngLat([-73.7781, 40.6413])
          .addTo(liveMap);

        JFK_AIRCRAFT.forEach((ac) => {
          const live = liveFleetRef.current.get(ac.flightId);
          const el = document.createElement('div');
          el.innerHTML = makeIconHtml(ac, live);

          const popup = new maplibregl.Popup({
            closeButton: false,
            className: 'aircraft-popup',
            offset: 20,
          }).setHTML(tooltipHtml(ac, live));

          popupRefs.current[ac.flightId] = popup;

          el.addEventListener('mouseenter', () => {
            const m = markerRefs.current[ac.flightId];
            const currentPos = positionsRef.current[ac.flightId] ?? ac;
            const currentLive = liveFleetRef.current.get(ac.flightId);
            if (m) {
              popup
                .setHTML(tooltipHtml(currentPos, currentLive))
                .addTo(liveMap)
                .setLngLat(m.getLngLat());
            }
          });
          el.addEventListener('mouseleave', () => popup.remove());

          const marker = new maplibregl.Marker({ element: el })
            .setLngLat([ac.lon, ac.lat])
            .addTo(liveMap);

          markerRefs.current[ac.flightId] = marker;
        });

        mapRef.current = liveMap;
      });
    } catch {
      // MapLibre GL requires WebGL — not available in jsdom test environments
    }

    return () => {
      if (map) {
        map.remove();
        mapRef.current = null;
      }
    };
  }, []);

  useEffect(() => {
    const intervalId = setInterval(() => {
      const positions = positionsRef.current;
      Object.values(positions).forEach((pos) => {
        const headingRad = (pos.heading * Math.PI) / 180;
        const newLat = pos.lat + Math.cos(headingRad) * pos.speedKnots * NUDGE;
        const newLon = pos.lon + Math.sin(headingRad) * pos.speedKnots * NUDGE;
        const newHeading = pos.heading + (Math.random() - 0.5) * 3;
        const updated: JFKAircraft = {
          ...pos,
          lat: newLat,
          lon: newLon,
          heading: newHeading,
        };
        positions[pos.flightId] = updated;

        const live = liveFleetRef.current.get(pos.flightId);
        const marker = markerRefs.current[pos.flightId];
        const popup = popupRefs.current[pos.flightId];
        if (marker) {
          marker.setLngLat([newLon, newLat]);
          marker.getElement().innerHTML = makeIconHtml(updated, live);
        }
        if (popup) {
          popup.setHTML(tooltipHtml(updated, live));
        }
      });
    }, 30000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div data-testid="map-panel" style={{ width: '100%', height: '100%' }}>
      <style>{MARKER_STYLE}</style>
      <div
        id="jfk-map"
        style={{ width: '100%', height: '100%', background: '#062340' }}
      />
    </div>
  );
}

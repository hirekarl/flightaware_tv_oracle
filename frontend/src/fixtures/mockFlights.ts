import type { FlightState } from '../types/flight';

export interface MockFlightEntry extends FlightState {
  readonly departTime: string;
}

export const mockFlights: MockFlightEntry[] = [
  {
    flightId: 'AA123',
    aircraftType: 'B737',
    route: { departure: 'KIAD', destination: 'KIAH' },
    operationalStatus: 'NORMAL',
    deviationType: 'NONE',
    telemetry: { fuelRemainingMin: 180, altitude: 35000 },
    aiAnalysis: {
      summaryTitle: 'On track',
      rootCause: 'None',
      downstreamImpact: 'None',
      recommendedAction: 'Maintain current heading',
    },
    departTime: '11:00a MDT',
  },
  {
    flightId: 'UA456',
    aircraftType: 'A320',
    route: { departure: 'KPHX', destination: 'KDEN' },
    operationalStatus: 'WARNING',
    deviationType: 'GO_AROUND',
    telemetry: { fuelRemainingMin: 95, altitude: 28000 },
    aiAnalysis: {
      summaryTitle: 'Go-around initiated at KDEN',
      rootCause: 'Crosswind exceeds limits',
      downstreamImpact: 'Gate delay likely 20–30 min',
      recommendedAction: 'Hold pattern, notify gate ops',
    },
    departTime: '11:15a MDT',
  },
  {
    flightId: 'DL789',
    aircraftType: 'B788',
    route: { departure: 'KATL', destination: 'KORD' },
    operationalStatus: 'CRITICAL',
    deviationType: 'DIVERSION',
    telemetry: { fuelRemainingMin: 42, altitude: 31000 },
    aiAnalysis: {
      summaryTitle: 'Diverting to KMDW — low fuel',
      rootCause: 'Unanticipated headwinds consumed reserve',
      downstreamImpact: '3 connecting flights at risk',
      recommendedAction: 'Declare minimum fuel, coordinate KMDW crew',
    },
    departTime: '11:30a MDT',
  },
  {
    flightId: 'SW202',
    aircraftType: 'B737',
    route: { departure: 'KDFW', destination: 'KLAS' },
    operationalStatus: 'NORMAL',
    deviationType: 'NONE',
    telemetry: { fuelRemainingMin: 210, altitude: 37000 },
    aiAnalysis: {
      summaryTitle: 'On track',
      rootCause: 'None',
      downstreamImpact: 'None',
      recommendedAction: 'No action required',
    },
    departTime: '11:45a MDT',
  },
  {
    flightId: 'JB304',
    aircraftType: 'A321',
    route: { departure: 'KJFK', destination: 'KMIA' },
    operationalStatus: 'WARNING',
    deviationType: 'HOLDING_PATTERN',
    telemetry: { fuelRemainingMin: 78, altitude: 24000 },
    aiAnalysis: {
      summaryTitle: 'Holding at KMIA — congestion',
      rootCause: 'Ground stop in effect at destination',
      downstreamImpact: 'Arrival delay 35 min',
      recommendedAction: 'Monitor fuel state, advise cabin crew',
    },
    departTime: '12:00p MDT',
  },
  {
    flightId: 'NK501',
    aircraftType: 'A320',
    route: { departure: 'KBOS', destination: 'KBWI' },
    operationalStatus: 'CRITICAL',
    deviationType: 'GO_AROUND',
    telemetry: { fuelRemainingMin: 31, altitude: 18000 },
    aiAnalysis: {
      summaryTitle: 'Second go-around — critically low fuel',
      rootCause: 'ILS failure at KBWI, multiple missed approaches',
      downstreamImpact: 'Emergency fuel declaration imminent',
      recommendedAction: 'Divert KDCA immediately, notify ATC',
    },
    departTime: '12:15p MDT',
  },
];

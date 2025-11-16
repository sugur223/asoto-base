export type LocationType = 'online' | 'offline' | 'hybrid';
export type EventStatus = 'draft' | 'published' | 'cancelled' | 'completed';
export type ParticipantStatus = 'pending' | 'confirmed' | 'cancelled';

export interface Event {
  id: string;
  owner_id: string;
  title: string;
  description?: string | null;
  start_date: string;
  end_date?: string | null;
  location_type: LocationType;
  location_detail?: string | null;
  max_attendees?: number | null;
  tags: string[];
  status: EventStatus;
  created_at: string;
  updated_at: string;
}

export interface EventParticipant {
  id: string;
  event_id: string;
  user_id: string;
  status: ParticipantStatus;
  joined_at: string;
}

export interface CreateEventInput {
  title: string;
  description?: string;
  start_date: string;
  end_date?: string;
  location_type: LocationType;
  location_detail?: string;
  max_attendees?: number;
  tags?: string[];
}

export interface UpdateEventInput {
  title?: string;
  description?: string;
  start_date?: string;
  end_date?: string;
  location_type?: LocationType;
  location_detail?: string;
  max_attendees?: number;
  tags?: string[];
  status?: EventStatus;
}

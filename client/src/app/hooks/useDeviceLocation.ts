import axios from "axios";
import { useQuery } from "@tanstack/react-query";

export interface Location {
  latitude: number;
  longitude: number;
}


export function useDeviceLocation(phoneNumber: string | null) {
  return useQuery({
    queryKey: ['location', phoneNumber],
    queryFn: () => axios.get(`${process.env.NEXT_PUBLIC_API_URL}/devices/${phoneNumber}/location`).then(r => r.data),
    enabled: !!phoneNumber,
    refetchInterval: 30000,
  });


  }

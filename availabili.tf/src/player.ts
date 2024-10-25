export interface Player {
  steamId: number;
  name: string;
}

export interface PlayerTeamRole {
  steamId: number;
  name: string;
  role: string;
  main: boolean;
  availability: number;
  playtime: number;
}

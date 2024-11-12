export interface Player {
  steamId: number;
  name: string;
}

export interface PlayerTeamRoleFlat {
  steamId: string;
  name: string;
  role: string;
  isMain: boolean;
  availability: number;
  playtime: number;
}

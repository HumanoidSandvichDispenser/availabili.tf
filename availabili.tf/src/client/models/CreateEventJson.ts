/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerRoleSchema } from './PlayerRoleSchema';
export type CreateEventJson = {
    description: (string | null);
    includePlayersWithoutRoles?: boolean;
    name: string;
    playerRoles: Array<PlayerRoleSchema>;
    startTime: string;
};


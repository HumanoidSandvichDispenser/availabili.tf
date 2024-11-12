/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerSchema } from './PlayerSchema';
import type { RoleSchema } from './RoleSchema';
export type PlayerTeamAvailabilityRoleSchema = {
    availability: number;
    player: PlayerSchema;
    playtime: number;
    roles: Array<RoleSchema>;
};


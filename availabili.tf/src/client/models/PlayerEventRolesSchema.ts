/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerSchema } from './PlayerSchema';
import type { RoleSchema } from './RoleSchema';
export type PlayerEventRolesSchema = {
    hasConfirmed: boolean;
    player: PlayerSchema;
    playtime: number;
    role: (RoleSchema | null);
    roles: Array<RoleSchema>;
};


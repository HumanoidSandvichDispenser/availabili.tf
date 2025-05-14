/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleSchema } from './RoleSchema';
export type ViewTeamMembersResponse = {
    availability: Array<number>;
    createdAt: string;
    isAdmin?: boolean;
    isTeamLeader?: boolean;
    playtime: number;
    roles: Array<RoleSchema>;
    steamId: string;
    username: string;
};


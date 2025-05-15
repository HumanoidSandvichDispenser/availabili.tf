/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PlayerSchema } from './PlayerSchema';
export type GetUserResponse = {
    discordId?: (string | null);
    isAdmin?: boolean;
    realUser: (PlayerSchema | null);
    steamId: string;
    username: string;
};


/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AddPlayerJson } from '../models/AddPlayerJson';
import type { CreateTeamJson } from '../models/CreateTeamJson';
import type { EditMemberRolesJson } from '../models/EditMemberRolesJson';
import type { PutScheduleForm } from '../models/PutScheduleForm';
import type { ViewScheduleResponse } from '../models/ViewScheduleResponse';
import type { ViewTeamMembersResponseList } from '../models/ViewTeamMembersResponseList';
import type { ViewTeamResponse } from '../models/ViewTeamResponse';
import type { ViewTeamsResponse } from '../models/ViewTeamsResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import type { BaseHttpRequest } from '../core/BaseHttpRequest';
export class DefaultService {
    constructor(public readonly httpRequest: BaseHttpRequest) {}
    /**
     * debug_set_cookie <GET>
     * @returns void
     * @throws ApiError
     */
    public getApiDebugSetCookie(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/debug/set-cookie',
        });
    }
    /**
     * debug_set_cookie <POST>
     * @returns void
     * @throws ApiError
     */
    public postApiDebugSetCookie(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/debug/set-cookie',
        });
    }
    /**
     * logout <DELETE>
     * @returns void
     * @throws ApiError
     */
    public deleteApiLogin(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/login/',
        });
    }
    /**
     * index <GET>
     * @returns void
     * @throws ApiError
     */
    public getApiLogin(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/login/',
        });
    }
    /**
     * steam_authenticate <POST>
     * @returns void
     * @throws ApiError
     */
    public postApiLoginAuthenticate(): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/login/authenticate',
        });
    }
    /**
     * get <GET>
     * @param windowStart
     * @param teamId
     * @param windowSizeDays
     * @returns ViewScheduleResponse OK
     * @throws ApiError
     */
    public getApiSchedule(
        windowStart: string,
        teamId: number,
        windowSizeDays: number = 7,
    ): CancelablePromise<ViewScheduleResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/schedule/',
            query: {
                'windowStart': windowStart,
                'teamId': teamId,
                'windowSizeDays': windowSizeDays,
            },
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * put <PUT>
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public putApiSchedule(
        requestBody?: PutScheduleForm,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/schedule/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }
    /**
     * view_available <GET>
     * @param startTime
     * @param teamId
     * @returns void
     * @throws ApiError
     */
    public getApiScheduleViewAvailable(
        startTime: string,
        teamId: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/schedule/view-available',
            query: {
                'startTime': startTime,
                'teamId': teamId,
            },
        });
    }
    /**
     * create_team <POST>
     * @param requestBody
     * @returns ViewTeamResponse OK
     * @throws ApiError
     */
    public createTeam(
        requestBody?: CreateTeamJson,
    ): CancelablePromise<ViewTeamResponse> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/team/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * view_teams <GET>
     * @returns ViewTeamsResponse OK
     * @throws ApiError
     */
    public getTeams(): CancelablePromise<ViewTeamsResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/team/all/',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * delete_team <DELETE>
     * @param teamId
     * @returns any OK
     * @throws ApiError
     */
    public deleteTeam(
        teamId: string,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/team/id/{team_id}/',
            path: {
                'team_id': teamId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * view_team <GET>
     * @param teamId
     * @returns ViewTeamResponse OK
     * @throws ApiError
     */
    public getTeam(
        teamId: string,
    ): CancelablePromise<ViewTeamResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/team/id/{team_id}/',
            path: {
                'team_id': teamId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * edit_member_roles <PATCH>
     * @param teamId
     * @param targetPlayerId
     * @param requestBody
     * @returns void
     * @throws ApiError
     */
    public editMemberRoles(
        teamId: string,
        targetPlayerId: string,
        requestBody?: EditMemberRolesJson,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/team/id/{team_id}/edit-player/{target_player_id}',
            path: {
                'team_id': teamId,
                'target_player_id': targetPlayerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * add_player <PUT>
     * @param teamId
     * @param playerId
     * @param requestBody
     * @returns any OK
     * @throws ApiError
     */
    public createOrUpdatePlayer(
        teamId: string,
        playerId: string,
        requestBody?: AddPlayerJson,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'PUT',
            url: '/api/team/id/{team_id}/player/{player_id}/',
            path: {
                'team_id': teamId,
                'player_id': playerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * view_team_members <GET>
     * @param teamId
     * @returns ViewTeamMembersResponseList OK
     * @throws ApiError
     */
    public getTeamMembers(
        teamId: string,
    ): CancelablePromise<ViewTeamMembersResponseList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/team/id/{team_id}/players',
            path: {
                'team_id': teamId,
            },
            errors: {
                403: `Forbidden`,
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
}

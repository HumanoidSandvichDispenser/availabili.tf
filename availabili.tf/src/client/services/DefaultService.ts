/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AbstractTeamIntegrationSchema } from '../models/AbstractTeamIntegrationSchema';
import type { AddPlayerJson } from '../models/AddPlayerJson';
import type { CreateEventJson } from '../models/CreateEventJson';
import type { CreateTeamJson } from '../models/CreateTeamJson';
import type { EditMemberRolesJson } from '../models/EditMemberRolesJson';
import type { EventSchema } from '../models/EventSchema';
import type { EventSchemaList } from '../models/EventSchemaList';
import type { PlayerSchema } from '../models/PlayerSchema';
import type { PutScheduleForm } from '../models/PutScheduleForm';
import type { SetUsernameJson } from '../models/SetUsernameJson';
import type { TeamIntegrationSchema } from '../models/TeamIntegrationSchema';
import type { TeamIntegrationSchemaList } from '../models/TeamIntegrationSchemaList';
import type { TeamInviteSchema } from '../models/TeamInviteSchema';
import type { TeamInviteSchemaList } from '../models/TeamInviteSchemaList';
import type { ViewAvailablePlayersResponse } from '../models/ViewAvailablePlayersResponse';
import type { ViewScheduleResponse } from '../models/ViewScheduleResponse';
import type { ViewTeamMembersResponseList } from '../models/ViewTeamMembersResponseList';
import type { ViewTeamResponse } from '../models/ViewTeamResponse';
import type { ViewTeamScheduleResponse } from '../models/ViewTeamScheduleResponse';
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
     * get_team_events <GET>
     * @param teamId
     * @returns EventSchemaList OK
     * @throws ApiError
     */
    public getTeamEvents(
        teamId: number,
    ): CancelablePromise<EventSchemaList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/events/team/id/{team_id}',
            path: {
                'team_id': teamId,
            },
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * create_event <POST>
     * @param teamId
     * @param requestBody
     * @returns EventSchema OK
     * @throws ApiError
     */
    public postApiEventsTeamIdTeamId(
        teamId: number,
        requestBody?: CreateEventJson,
    ): CancelablePromise<EventSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/events/team/id/{team_id}',
            path: {
                'team_id': teamId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * get_user_events <GET>
     * @param userId
     * @returns void
     * @throws ApiError
     */
    public getApiEventsUserIdUserId(
        userId: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/events/user/id/{user_id}',
            path: {
                'user_id': userId,
            },
        });
    }
    /**
     * get_event <GET>
     * @param eventId
     * @returns EventSchema OK
     * @throws ApiError
     */
    public getEvent(
        eventId: number,
    ): CancelablePromise<EventSchema> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/events/{event_id}',
            path: {
                'event_id': eventId,
            },
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * set_event_players <PATCH>
     * @param eventId
     * @returns void
     * @throws ApiError
     */
    public patchApiEventsEventIdPlayers(
        eventId: number,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/events/{event_id}/players',
            path: {
                'event_id': eventId,
            },
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
     * get_user <GET>
     * @returns PlayerSchema OK
     * @throws ApiError
     */
    public getUser(): CancelablePromise<PlayerSchema> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/login/get-user',
            errors: {
                401: `Unauthorized`,
                422: `Unprocessable Entity`,
            },
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
     * get_team_availability <GET>
     * @param windowStart
     * @param teamId
     * @param windowSizeDays
     * @returns ViewTeamScheduleResponse OK
     * @throws ApiError
     */
    public getApiScheduleTeam(
        windowStart: string,
        teamId: number,
        windowSizeDays: number = 7,
    ): CancelablePromise<ViewTeamScheduleResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/schedule/team',
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
     * view_available_at_time <GET>
     * @param startTime
     * @param teamId
     * @returns ViewAvailablePlayersResponse OK
     * @throws ApiError
     */
    public viewAvailableAtTime(
        startTime: string,
        teamId: number,
    ): CancelablePromise<ViewAvailablePlayersResponse> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/schedule/view-available',
            query: {
                'startTime': startTime,
                'teamId': teamId,
            },
            errors: {
                422: `Unprocessable Entity`,
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
     * consume_invite <POST>
     * @param teamId
     * @param key
     * @returns void
     * @throws ApiError
     */
    public consumeInvite(
        teamId: string,
        key: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/team/id/{team_id}/consume-invite/{key}',
            path: {
                'team_id': teamId,
                'key': key,
            },
            errors: {
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
     * get_integrations <GET>
     * @param teamId
     * @returns TeamIntegrationSchemaList OK
     * @throws ApiError
     */
    public getIntegrations(
        teamId: string,
    ): CancelablePromise<TeamIntegrationSchemaList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/team/id/{team_id}/integrations',
            path: {
                'team_id': teamId,
            },
            errors: {
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * delete_integration <DELETE>
     * @param teamId
     * @param integrationId
     * @returns void
     * @throws ApiError
     */
    public deleteIntegration(
        teamId: string,
        integrationId: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/team/id/{team_id}/integrations/{integration_id}',
            path: {
                'team_id': teamId,
                'integration_id': integrationId,
            },
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * update_integration <PATCH>
     * @param teamId
     * @param integrationId
     * @param requestBody
     * @returns TeamIntegrationSchema OK
     * @throws ApiError
     */
    public updateIntegration(
        teamId: string,
        integrationId: string,
        requestBody?: AbstractTeamIntegrationSchema,
    ): CancelablePromise<TeamIntegrationSchema> {
        return this.httpRequest.request({
            method: 'PATCH',
            url: '/api/team/id/{team_id}/integrations/{integration_id}',
            path: {
                'team_id': teamId,
                'integration_id': integrationId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * create_integration <POST>
     * @param teamId
     * @param integrationType
     * @returns TeamIntegrationSchema OK
     * @throws ApiError
     */
    public createIntegration(
        teamId: string,
        integrationType: string,
    ): CancelablePromise<TeamIntegrationSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/team/id/{team_id}/integrations/{integration_type}',
            path: {
                'team_id': teamId,
                'integration_type': integrationType,
            },
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * get_invites <GET>
     * @param teamId
     * @returns TeamInviteSchemaList OK
     * @throws ApiError
     */
    public getInvites(
        teamId: string,
    ): CancelablePromise<TeamInviteSchemaList> {
        return this.httpRequest.request({
            method: 'GET',
            url: '/api/team/id/{team_id}/invite',
            path: {
                'team_id': teamId,
            },
            errors: {
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * create_invite <POST>
     * @param teamId
     * @returns TeamInviteSchema OK
     * @throws ApiError
     */
    public createInvite(
        teamId: string,
    ): CancelablePromise<TeamInviteSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/team/id/{team_id}/invite',
            path: {
                'team_id': teamId,
            },
            errors: {
                404: `Not Found`,
                422: `Unprocessable Entity`,
            },
        });
    }
    /**
     * revoke_invite <DELETE>
     * @param teamId
     * @param key
     * @returns void
     * @throws ApiError
     */
    public revokeInvite(
        teamId: string,
        key: string,
    ): CancelablePromise<void> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/team/id/{team_id}/invite/{key}',
            path: {
                'team_id': teamId,
                'key': key,
            },
            errors: {
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
     * remove_player_from_team <DELETE>
     * @param teamId
     * @param targetPlayerId
     * @returns any OK
     * @throws ApiError
     */
    public removePlayerFromTeam(
        teamId: string,
        targetPlayerId: string,
    ): CancelablePromise<any> {
        return this.httpRequest.request({
            method: 'DELETE',
            url: '/api/team/id/{team_id}/player/{target_player_id}/',
            path: {
                'team_id': teamId,
                'target_player_id': targetPlayerId,
            },
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
    /**
     * set_username <POST>
     * @param requestBody
     * @returns PlayerSchema OK
     * @throws ApiError
     */
    public setUsername(
        requestBody?: SetUsernameJson,
    ): CancelablePromise<PlayerSchema> {
        return this.httpRequest.request({
            method: 'POST',
            url: '/api/user/username',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Unprocessable Entity`,
            },
        });
    }
}

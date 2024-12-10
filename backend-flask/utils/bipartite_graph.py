from collections import deque, defaultdict

from models.player_team import PlayerTeam
from models.player_team_role import PlayerTeamRole

from collections import deque


class BipartiteGraph:
    graph: dict[int, list[PlayerTeamRole.Role]] = {}
    pair_u: dict[int, PlayerTeamRole.Role | None] = {}
    pair_v: dict[PlayerTeamRole.Role, int | None] = {}
    dist: dict[int | None, float] = {}
    U: set[int] = set()
    V: set[PlayerTeamRole.Role] = set()

    def __init__(
        self,
        ids_to_roles: dict[int, list[PlayerTeamRole.Role]],
        required_roles: list[PlayerTeamRole.Role],
    ):
        self.graph = self.build_graph(ids_to_roles, required_roles)
        self.pair_u = {}
        self.pair_v = {}
        self.dist = {}
        self.U = set(ids_to_roles.keys())
        self.V = set(
            role
            for roles in ids_to_roles.values()
            for role in roles
            if role in required_roles
        )

    def build_graph(
        self,
        ids_to_roles: dict[int, list[PlayerTeamRole.Role]],
        required_roles: list[PlayerTeamRole.Role],
    ):
        graph = {}
        for u, roles in ids_to_roles.items():
            graph[u] = [v for v in roles if v in required_roles]
        return graph

    def bfs(self):
        queue = deque()
        for u in self.U:
            if u not in self.pair_u:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float("inf")
        self.dist[None] = float("inf")

        while queue:
            u = queue.popleft()
            if self.dist[u] < self.dist[None]:
                for v in self.graph[u]:
                    if self.dist[self.pair_v.get(v, None)] == float("inf"):
                        self.dist[self.pair_v.get(v, None)] = self.dist[u] + 1
                        queue.append(self.pair_v.get(v, None))

        return self.dist[None] != float("inf")

    def dfs(self, u):
        if u is not None:
            for v in self.graph[u]:
                if self.dist[self.pair_v.get(v, None)] == self.dist[u] + 1:
                    if self.dfs(self.pair_v.get(v, None)):
                        self.pair_u[u] = v
                        self.pair_v[v] = u
                        return True
            self.dist[u] = float("inf")
            return False
        return True

    def hopcroft_karp(self):
        matching = 0
        while self.bfs():
            for u in self.U:
                if u not in self.pair_u:
                    if self.dfs(u):
                        matching += 1
        return matching

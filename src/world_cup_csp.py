import copy


class WorldCupCSP:
    def __init__(self, teams, groups, debug=False):
        """
        Inicializa el problema CSP para el sorteo del Mundial.
        :param teams: Diccionario con los equipos, sus confederaciones y bombos.
        :param groups: Lista con los nombres de los grupos (A-L).
        :param debug: Booleano para activar trazas de depuración.
        """
        self.teams = teams
        self.groups = groups
        self.debug = debug

        # Las variables son los equipos.
        self.variables = list(teams.keys())

        # El dominio de cada variable inicialmente son todos los grupos.
        self.domains = {team: list(groups) for team in self.variables}

    def get_team_confederation(self, team):
        return self.teams[team]["conf"]

    def get_team_pot(self, team):
        return self.teams[team]["pot"]

    def is_valid_assignment(self, group, team, assignment):
        """
        Verifica si asignar un equipo a un grupo viola
        las restricciones de confederación o tamaño del grupo.
        """
        in_group = [t for t, g in assignment.items() if g == group]
        if len(in_group) >= 4:
            return False

        pot = self.get_team_pot(team)
        for t in in_group:
            if self.get_team_pot(t) == pot:
                return False

        conf = self.get_team_confederation(team)
        confs_in_group = [self.get_team_confederation(t) for t in in_group]

        if conf == "UEFA":
            if confs_in_group.count("UEFA") >= 2:
                return False
        else:
            if conf in confs_in_group:
                return False

        return True

    def forward_check(self, assignment, domains):
        """
        Propagación de restricciones.
        Debe eliminar valores inconsistentes en dominios futuros.
        Retorna True si la propagación es exitosa, False si algún dominio queda vacío.
        """
        new_domains = copy.deepcopy(domains)

        for team in self.variables:
            if team in assignment:
                continue
            valid_groups = [
                g
                for g in new_domains[team]
                if self.is_valid_assignment(g, team, assignment)
            ]
            new_domains[team] = valid_groups
            if len(valid_groups) == 0:
                return False, new_domains

        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):
        """
        Heurística MRV (Minimum Remaining Values).
        Selecciona la variable no asignada con el dominio más pequeño.
        """
        unassigned = [v for v in self.variables if v not in assignment]
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(domains.get(v, [])))

    def backtrack(self, assignment, domains=None):
        """
        Backtracking search para resolver el CSP.
        """
        if domains is None:
            domains = copy.deepcopy(self.domains)

        if len(assignment) == len(self.variables):
            return assignment

        var = self.select_unassigned_variable(assignment, domains)
        if var is None:
            return None

        for group in list(domains[var]):
            if not self.is_valid_assignment(group, var, assignment):
                continue

            assignment[var] = group
            if self.debug:
                print(f"  Asignando {var} -> Grupo {group}")

            success, new_domains = self.forward_check(assignment, domains)
            if success:
                result = self.backtrack(assignment, new_domains)
                if result is not None:
                    return result

            del assignment[var]
            if self.debug:
                print(f"  Backtrack: quitando {var} de Grupo {group}")

        return None

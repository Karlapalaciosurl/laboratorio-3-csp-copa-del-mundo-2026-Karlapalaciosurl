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
        # TODO: implementar restricción de tamaño del grupo (máximo 4)
        # TODO: implementar restricción de que no puede haber dos equipos del mismo bombo
        # TODO: implementar restricción de confederaciones (máximo 1, excepto UEFA máximo 2)

        # Este es un valor de retorno por defecto, debes modificarlo
        confederation = self.get_team_confederation(team)
        pot = self.get_team_pot(team)
    
        # Equipos ya asignados a este grupo
        teams_in_group = [t for t, g in assignment.items() if g == group]
    
         # Restricción 1: máximo 4 equipos por grupo
        if len(teams_in_group) >= 4:
           return False
    
         # Restricción 2: implementar restricción de que no puede haber dos equipos del mismo bombo
        for t in teams_in_group:
            if self.get_team_pot(t) == pot:
               return False
    
        # Restricción 3: máximo 1 equipo por confederación, excepto UEFA que puede tener 2
        conf_count = sum(1 for t in teams_in_group if self.get_team_confederation(t) == confederation)
        if confederation == "UEFA":
           if conf_count >= 2:
              return False
        else:
            if conf_count >= 1:
               return False
    
        return True

    def forward_check(self, assignment, domains):
        """
        Propagación de restricciones.
        Debe eliminar valores inconsistentes en dominios futuros.
        Retorna True si la propagación es exitosa, False si algún dominio queda vacío.
        """
        # Hacemos una copia de los dominios actuales para modificarla de forma segura
        new_domains = copy.deepcopy(domains)

        for team in self.variables:
            if team not in assignment:
                # Filtrar grupos inválidos del dominio de cada variable no asignada
                new_domains[team] = [
                    group for group in new_domains[team]
                    if self.is_valid_assignment(group, team, assignment)
                ]
                # Si el dominio queda vacío, la propagación falla
                if not new_domains[team]:
                    return False, new_domains

        # TODO: implementar forward checking para filtrar grupos inválidos
        # en los dominios de las variables no asignadas.

        # Este es un valor de retorno por defecto, debes modificarlo
        return True, new_domains

    def select_unassigned_variable(self, assignment, domains):
        """
        Heurística MRV (Minimum Remaining Values).
        Selecciona la variable no asignada con el dominio más pequeño.
        """
        # TODO: implementar MRV

        # Este es un valor de retorno por defecto, debes modificarlo
        unassigned_vars = [v for v in self.variables if v not in assignment]
        if not unassigned_vars:
            return None

        return min(unassigned_vars, key=lambda v: len(domains[v]))

    def backtrack(self, assignment, domains=None):
        """
        Backtracking search para resolver el CSP.
        """
        if domains is None:
            domains = copy.deepcopy(self.domains)

        # Condición de parada: Si todas las variables están asignadas, retornamos la asignación.
        if len(assignment) == len(self.variables):
            return assignment

        # TODO: implementar algoritmo de backtracking
        # 1. Seleccionar variable con MRV
        # 2. Iterar sobre sus valores (grupos) posibles en el dominio
        # 3. Verificar si es válido, hacer la asignación y aplicar forward checking
        # 4. Llamada recursiva
        # 5. Deshacer la asignación si falla (backtrack)

        # Este es un valor de retorno por defecto, debes modificarlo
        # 1. Seleccionar variable con MRV
        team = self.select_unassigned_variable(assignment, domains)

        if team is None:
            return None
        
        # 2. Iterar sobre los grupos posibles en el dominio
        for group in domains[team]:
            # 3. Verificar si es válido
            if self.is_valid_assignment(group, team, assignment):

                # Hacer la asignación
                assignment[team] = group

                if self.debug:
                    print(f"  Asignando {team} Grupo {group}")

                # Aplicar forward checking
                success, new_domains = self.forward_check(assignment, domains)

                if success:
                    # 4. Llamada recursiva
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result
                    
                # 5. Deshacer la asignación (backtrack)
                if self.debug:
                    print(f"  Backtrack: deshaciendo {team} Grupo {group}")
                del assignment[team]
        return None


class EntityNotFound(Exception):
    def __init__(self, entity, reason):
        super().__init__(f'Entity {entity} not found: {reason}')

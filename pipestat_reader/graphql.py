from functools import partial

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType


class PipestatReader(dict):
    def __init__(self, pipestat_manager):
        self.pipestat_manager = pipestat_manager
        self.table_name = pipestat_manager.namespace
        self.table_model = pipestat_manager._get_orm(table_name=self.table_name)
        meta = type("Meta", (), {"model": self.table_model})
        self.SQLAlchemyObjectType = type(
            f"{self.table_name.capitalize()}SQLAlchemyObjectType",
            (SQLAlchemyObjectType,),
            {"Meta": meta},
        )

    def create_classes(self):
        resolver = partial(
            resolver_method, psm=self.pipestat_manager, table_model=self.table_model
        )
        return type(
            f"{self.table_name}Query",
            (graphene.ObjectType,),
            {
                f"{self.table_name}": graphene.List(self.SQLAlchemyObjectType),
                f"resolve_{self.table_name}": resolver,
            },
        )

    def generate_graphql_schema(self):
        return graphene.Schema(query=self.create_classes())


def resolver_method(self, info, psm, table_model):
    with psm.session as s:
        return s.query(table_model).all()

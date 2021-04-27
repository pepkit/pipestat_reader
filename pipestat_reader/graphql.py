import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from ._version import __version__
from .const import PACKAGE_NAME


class PipestatReader(dict):
    def __init__(self, pipestat_manager):
        self.pipestat_manager = pipestat_manager
        self.table_name = pipestat_manager.namespace
        self.table_model = pipestat_manager._get_orm(table_name=self.table_name)
        meta = type(
            "Meta",
            (),
            {
                "model": self.table_model,
                "interfaces": (relay.Node,),
                "description": f"'{self.table_name}' model generated with "
                f"`{PACKAGE_NAME} v{__version__}`",
            },
        )
        meta_filter = type(
            "Meta", (), {"model": self.table_model, "fields": {"name": [...]}}
        )
        self.SQLAlchemyObjectType = type(
            f"{self.table_name.capitalize()}SQLAlchemyObjectType",
            (SQLAlchemyObjectType,),
            {"Meta": meta},
        )
        self.filter = type(
            f"{self.table_name.capitalize()}Filter",
            (FilterSet,),
            {"Meta": meta_filter},
        )

    @property
    def query(self):

        return type(
            f"{self.table_name}Query",
            (graphene.ObjectType,),
            {
                f"{self.table_name}": FilterableConnectionField(
                    self.SQLAlchemyObjectType.connection, filters=self.filter()
                ),
                "node": relay.Node.Field(),
            },
        )

    def generate_graphql_schema(self):
        return graphene.Schema(query=self.query)


# def resolver_method(self, info, psm, table_model):
#     with psm.session as s:
#         return s.query(table_model).all()

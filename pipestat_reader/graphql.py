from typing import Dict, List, Optional, Tuple, Union

import graphene
import pipestat
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType
from graphene_sqlalchemy_filter import FilterableConnectionField, FilterSet

from ._version import __version__
from .const import PACKAGE_NAME


class PipestatReader(dict):
    def __init__(self, pipestat_managers: List[pipestat.PipestatManager]):
        self.pipestat_managers_dict = {psm.namespace: psm for psm in pipestat_managers}
        for namespace, pipestat_manager in self.pipestat_managers_dict.items():
            self.setdefault(namespace, {})
            self[namespace]["pipestat_manager"] = pipestat_manager
            self[namespace]["table_name"] = pipestat_manager.namespace
            self[namespace]["table_model"] = pipestat_manager._get_orm(
                table_name=self[namespace]["table_name"]
            )
            meta = type(
                "Meta",
                (),
                {
                    "model": self[namespace]["table_model"],
                    "interfaces": (relay.Node,),
                    "description": f"'{self[namespace]['table_name']}' model generated with "
                    f"`{PACKAGE_NAME} v{__version__}`",
                },
            )
            meta_filter = type(
                "Meta",
                (),
                {"model": self[namespace]["table_model"], "fields": {"name": [...]}},
            )
            self[namespace]["SQLAlchemyObjectType"] = type(
                f"{self[namespace]['table_name'].capitalize()}SQLAlchemyObjectType",
                (SQLAlchemyObjectType,),
                {"Meta": meta},
            )
            self[namespace]["filter"] = type(
                f"{self[namespace]['table_name'].capitalize()}Filter",
                (FilterSet,),
                {"Meta": meta_filter},
            )

    @property
    def query(self):
        attrs = {"node": relay.Node.Field()}
        for namespace in self.pipestat_managers_dict.keys():
            attrs.update(
                {
                    f"{namespace}": FilterableConnectionField(
                        self[namespace]["SQLAlchemyObjectType"].connection,
                        filters=self[namespace]["filter"](),
                    )
                }
            )
        return type(
            f"{'__'.join(list(self.pipestat_managers_dict.keys()))}Query",
            (graphene.ObjectType,),
            attrs,
        )

    def generate_graphql_schema(self):
        return graphene.Schema(query=self.query)


# def resolver_method(self, info, psm, table_model):
#     with psm.session as s:
#         return s.query(table_model).all()

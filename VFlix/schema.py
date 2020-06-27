import graphene
import VFlix.vfapp.schema

class Query(VFlix.vfapp.schema.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query)
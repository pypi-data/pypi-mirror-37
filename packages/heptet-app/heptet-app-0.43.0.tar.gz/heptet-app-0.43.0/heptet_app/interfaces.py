from zope.interface import Interface


class IGeneratorContext(Interface):
    pass


class IEntryPointView(Interface):
    pass


class IProcess(Interface):
    pass


# class ICollectorContext(Interface):
#     pass


class IObject(Interface):
    pass


class IVariableType(Interface):
    pass


class IEntryPoint(IObject):
    pass


class ITemplateSource(Interface):
    pass


class ITemplate(Interface):
    pass


class ITemplateVariable(Interface):
    pass


class ICollector(Interface):
    pass


class IBuilder(Interface):
    pass


class IRelationshipSelect(Interface):
    pass


class INamespaceStore(Interface):
    pass


# does it make sense to use 'key' here? no
class IMapperInfo(Interface):
    pass


class ISqlAlchemySession(object):
    pass


# @implementer(IInterface)
class IResource(Interface):
    pass


class IFormContext(Interface):
    pass


class IResourceManager(Interface):
    pass


class IEntryPointGenerator(Interface):
    pass


class IEntryPointMapperAdapter(Interface):
    pass
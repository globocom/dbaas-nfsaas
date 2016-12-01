
class FaaSAPIError(EnvironmentError):
    pass


class ExportAPIError(FaaSAPIError):
    pass


class CreateExportAPIError(ExportAPIError):
    pass


class DeleteExportAPIError(ExportAPIError):
    pass


class AccessAPIError(FaaSAPIError):
    pass


class CreateAccessAPIError(AccessAPIError):
    pass


class DeleteAccessAPIError(AccessAPIError):
    pass


class ListAccessAPIError(AccessAPIError):
    pass


class SnapshotAPIError(FaaSAPIError):
    pass


class CreateSnapshotAPIError(SnapshotAPIError):
    pass


class DeleteSnapshotAPIError(SnapshotAPIError):
    pass


class RestoreSnapshotAPIError(SnapshotAPIError):
    pass


class QuotaAPIError(FaaSAPIError):
    pass


class ResizeAPIError(QuotaAPIError):
    pass

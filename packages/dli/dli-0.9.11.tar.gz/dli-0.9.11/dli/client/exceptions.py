class DatalakeException(Exception):
    pass


class DatasetNotFoundException(DatalakeException):
    pass


class DatafileNotFoundException(DatalakeException):
    pass


class PackageNotFoundException(DatalakeException):

    def __init__(self, package_id=None, message=None):
        if not package_id and not message:
            message = "Package not found"

        self.message = (
            message or 'Package with id {} not found'.format(package_id)
        )

        super(PackageNotFoundException, self).__init__(self.message)


class InvalidPayloadException(DatalakeException):
    pass


class S3FileDoesNotExist(DatalakeException):
    def __init__(self, file_path):
        self.message = (
            "Either file at path `%s` does not exist / Potential issue with the bucket policy."
            "Please reach out to Datalake Tech Data Ops user for resolution." % file_path
        )

        super(S3FileDoesNotExist, self).__init__(self.message)


class DownloadDestinationNotValid(DatalakeException):
    """
    Raised when a download destination is not a directory
    """
    pass


class DownloadFailed(DatalakeException):
    pass


class NoAccountSpecified(DatalakeException):

    def __init__(self, accounts):
        self.accounts = accounts
        self.message = (
            "Unable to default the account for access_manager, tech_data_ops and/or manager "
            "due to multiple accounts being attached to this API key. "
            "Your accounts are: %s" % [(a.id, a.name) for a in accounts]
        )
        super(NoAccountSpecified, self).__init__(self.message)


class UnAuthorisedAccessException(DatalakeException):
    pass


class InsufficientPrivilegesException(DatalakeException):
    def __init__(self, message=None):
        self.message = (
            message or 'Insufficient privileges to perform this action'
        )

        super(InsufficientPrivilegesException, self).__init__(self.message)


class NoPackageIdSpecifiedException(DatalakeException):
    def __init__(self):
        self.message = "Package Id is required"
        super(NoPackageIdSpecifiedException, self).__init__(self.message)

def is_boto_client_access_denied_error(e):
    # s3fs wraps the boto ClientError under OSError with no particular code. Hence the check
    return isinstance(e, OSError) and 'AccessDenied' in str(e.strerror)

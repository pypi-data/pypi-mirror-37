# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from google.cloud.spanner_admin_instance_v1.proto import spanner_instance_admin_pb2 as google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2
from google.iam.v1 import iam_policy_pb2 as google_dot_iam_dot_v1_dot_iam__policy__pb2
from google.iam.v1 import policy_pb2 as google_dot_iam_dot_v1_dot_policy__pb2
from google.longrunning import operations_pb2 as google_dot_longrunning_dot_operations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


class InstanceAdminStub(object):
  """Cloud Spanner Instance Admin API

  The Cloud Spanner Instance Admin API can be used to create, delete,
  modify and list instances. Instances are dedicated Cloud Spanner serving
  and storage resources to be used by Cloud Spanner databases.

  Each instance has a "configuration", which dictates where the
  serving resources for the Cloud Spanner instance are located (e.g.,
  US-central, Europe). Configurations are created by Google based on
  resource availability.

  Cloud Spanner billing is based on the instances that exist and their
  sizes. After an instance exists, there are no additional
  per-database or per-operation charges for use of the instance
  (though there may be additional network bandwidth charges).
  Instances offer isolation: problems with databases in one instance
  will not affect other instances. However, within an instance
  databases can affect each other. For example, if one database in an
  instance receives a lot of requests and consumes most of the
  instance resources, fewer resources are available for other
  databases in that instance, and their performance may suffer.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.ListInstanceConfigs = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/ListInstanceConfigs',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstanceConfigsRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstanceConfigsResponse.FromString,
        )
    self.GetInstanceConfig = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/GetInstanceConfig',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.GetInstanceConfigRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.InstanceConfig.FromString,
        )
    self.ListInstances = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/ListInstances',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstancesRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstancesResponse.FromString,
        )
    self.GetInstance = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/GetInstance',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.GetInstanceRequest.SerializeToString,
        response_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.Instance.FromString,
        )
    self.CreateInstance = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/CreateInstance',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.CreateInstanceRequest.SerializeToString,
        response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
    self.UpdateInstance = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/UpdateInstance',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.UpdateInstanceRequest.SerializeToString,
        response_deserializer=google_dot_longrunning_dot_operations__pb2.Operation.FromString,
        )
    self.DeleteInstance = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/DeleteInstance',
        request_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.DeleteInstanceRequest.SerializeToString,
        response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
        )
    self.SetIamPolicy = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/SetIamPolicy',
        request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.SetIamPolicyRequest.SerializeToString,
        response_deserializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.FromString,
        )
    self.GetIamPolicy = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/GetIamPolicy',
        request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.GetIamPolicyRequest.SerializeToString,
        response_deserializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.FromString,
        )
    self.TestIamPermissions = channel.unary_unary(
        '/google.spanner.admin.instance.v1.InstanceAdmin/TestIamPermissions',
        request_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsRequest.SerializeToString,
        response_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsResponse.FromString,
        )


class InstanceAdminServicer(object):
  """Cloud Spanner Instance Admin API

  The Cloud Spanner Instance Admin API can be used to create, delete,
  modify and list instances. Instances are dedicated Cloud Spanner serving
  and storage resources to be used by Cloud Spanner databases.

  Each instance has a "configuration", which dictates where the
  serving resources for the Cloud Spanner instance are located (e.g.,
  US-central, Europe). Configurations are created by Google based on
  resource availability.

  Cloud Spanner billing is based on the instances that exist and their
  sizes. After an instance exists, there are no additional
  per-database or per-operation charges for use of the instance
  (though there may be additional network bandwidth charges).
  Instances offer isolation: problems with databases in one instance
  will not affect other instances. However, within an instance
  databases can affect each other. For example, if one database in an
  instance receives a lot of requests and consumes most of the
  instance resources, fewer resources are available for other
  databases in that instance, and their performance may suffer.
  """

  def ListInstanceConfigs(self, request, context):
    """Lists the supported instance configurations for a given project.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetInstanceConfig(self, request, context):
    """Gets information about a particular instance configuration.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ListInstances(self, request, context):
    """Lists all instances in the given project.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetInstance(self, request, context):
    """Gets information about a particular instance.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CreateInstance(self, request, context):
    """Creates an instance and begins preparing it to begin serving. The
    returned [long-running operation][google.longrunning.Operation]
    can be used to track the progress of preparing the new
    instance. The instance name is assigned by the caller. If the
    named instance already exists, `CreateInstance` returns
    `ALREADY_EXISTS`.

    Immediately upon completion of this request:

    * The instance is readable via the API, with all requested attributes
    but no allocated resources. Its state is `CREATING`.

    Until completion of the returned operation:

    * Cancelling the operation renders the instance immediately unreadable
    via the API.
    * The instance can be deleted.
    * All other attempts to modify the instance are rejected.

    Upon completion of the returned operation:

    * Billing for all successfully-allocated resources begins (some types
    may have lower than the requested levels).
    * Databases can be created in the instance.
    * The instance's allocated resource levels are readable via the API.
    * The instance's state becomes `READY`.

    The returned [long-running operation][google.longrunning.Operation] will
    have a name of the format `<instance_name>/operations/<operation_id>` and
    can be used to track creation of the instance.  The
    [metadata][google.longrunning.Operation.metadata] field type is
    [CreateInstanceMetadata][google.spanner.admin.instance.v1.CreateInstanceMetadata].
    The [response][google.longrunning.Operation.response] field type is
    [Instance][google.spanner.admin.instance.v1.Instance], if successful.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def UpdateInstance(self, request, context):
    """Updates an instance, and begins allocating or releasing resources
    as requested. The returned [long-running
    operation][google.longrunning.Operation] can be used to track the
    progress of updating the instance. If the named instance does not
    exist, returns `NOT_FOUND`.

    Immediately upon completion of this request:

    * For resource types for which a decrease in the instance's allocation
    has been requested, billing is based on the newly-requested level.

    Until completion of the returned operation:

    * Cancelling the operation sets its metadata's
    [cancel_time][google.spanner.admin.instance.v1.UpdateInstanceMetadata.cancel_time], and begins
    restoring resources to their pre-request values. The operation
    is guaranteed to succeed at undoing all resource changes,
    after which point it terminates with a `CANCELLED` status.
    * All other attempts to modify the instance are rejected.
    * Reading the instance via the API continues to give the pre-request
    resource levels.

    Upon completion of the returned operation:

    * Billing begins for all successfully-allocated resources (some types
    may have lower than the requested levels).
    * All newly-reserved resources are available for serving the instance's
    tables.
    * The instance's new resource levels are readable via the API.

    The returned [long-running operation][google.longrunning.Operation] will
    have a name of the format `<instance_name>/operations/<operation_id>` and
    can be used to track the instance modification.  The
    [metadata][google.longrunning.Operation.metadata] field type is
    [UpdateInstanceMetadata][google.spanner.admin.instance.v1.UpdateInstanceMetadata].
    The [response][google.longrunning.Operation.response] field type is
    [Instance][google.spanner.admin.instance.v1.Instance], if successful.

    Authorization requires `spanner.instances.update` permission on
    resource [name][google.spanner.admin.instance.v1.Instance.name].
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def DeleteInstance(self, request, context):
    """Deletes an instance.

    Immediately upon completion of the request:

    * Billing ceases for all of the instance's reserved resources.

    Soon afterward:

    * The instance and *all of its databases* immediately and
    irrevocably disappear from the API. All data in the databases
    is permanently deleted.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SetIamPolicy(self, request, context):
    """Sets the access control policy on an instance resource. Replaces any
    existing policy.

    Authorization requires `spanner.instances.setIamPolicy` on
    [resource][google.iam.v1.SetIamPolicyRequest.resource].
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetIamPolicy(self, request, context):
    """Gets the access control policy for an instance resource. Returns an empty
    policy if an instance exists but does not have a policy set.

    Authorization requires `spanner.instances.getIamPolicy` on
    [resource][google.iam.v1.GetIamPolicyRequest.resource].
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def TestIamPermissions(self, request, context):
    """Returns permissions that the caller has on the specified instance resource.

    Attempting this RPC on a non-existent Cloud Spanner instance resource will
    result in a NOT_FOUND error if the user has `spanner.instances.list`
    permission on the containing Google Cloud Project. Otherwise returns an
    empty set of permissions.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InstanceAdminServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'ListInstanceConfigs': grpc.unary_unary_rpc_method_handler(
          servicer.ListInstanceConfigs,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstanceConfigsRequest.FromString,
          response_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstanceConfigsResponse.SerializeToString,
      ),
      'GetInstanceConfig': grpc.unary_unary_rpc_method_handler(
          servicer.GetInstanceConfig,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.GetInstanceConfigRequest.FromString,
          response_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.InstanceConfig.SerializeToString,
      ),
      'ListInstances': grpc.unary_unary_rpc_method_handler(
          servicer.ListInstances,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstancesRequest.FromString,
          response_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.ListInstancesResponse.SerializeToString,
      ),
      'GetInstance': grpc.unary_unary_rpc_method_handler(
          servicer.GetInstance,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.GetInstanceRequest.FromString,
          response_serializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.Instance.SerializeToString,
      ),
      'CreateInstance': grpc.unary_unary_rpc_method_handler(
          servicer.CreateInstance,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.CreateInstanceRequest.FromString,
          response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
      ),
      'UpdateInstance': grpc.unary_unary_rpc_method_handler(
          servicer.UpdateInstance,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.UpdateInstanceRequest.FromString,
          response_serializer=google_dot_longrunning_dot_operations__pb2.Operation.SerializeToString,
      ),
      'DeleteInstance': grpc.unary_unary_rpc_method_handler(
          servicer.DeleteInstance,
          request_deserializer=google_dot_cloud_dot_spanner_dot_admin_dot_instance__v1_dot_proto_dot_spanner__instance__admin__pb2.DeleteInstanceRequest.FromString,
          response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
      ),
      'SetIamPolicy': grpc.unary_unary_rpc_method_handler(
          servicer.SetIamPolicy,
          request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.SetIamPolicyRequest.FromString,
          response_serializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.SerializeToString,
      ),
      'GetIamPolicy': grpc.unary_unary_rpc_method_handler(
          servicer.GetIamPolicy,
          request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.GetIamPolicyRequest.FromString,
          response_serializer=google_dot_iam_dot_v1_dot_policy__pb2.Policy.SerializeToString,
      ),
      'TestIamPermissions': grpc.unary_unary_rpc_method_handler(
          servicer.TestIamPermissions,
          request_deserializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsRequest.FromString,
          response_serializer=google_dot_iam_dot_v1_dot_iam__policy__pb2.TestIamPermissionsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'google.spanner.admin.instance.v1.InstanceAdmin', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

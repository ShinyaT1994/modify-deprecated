import aws_cdk as core
import aws_cdk.assertions as assertions

from modify_deprecated_api.modify_deprecated_api_stack import ModifyDeprecatedApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in modify_deprecated_api/modify_deprecated_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ModifyDeprecatedApiStack(app, "modify-deprecated-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })

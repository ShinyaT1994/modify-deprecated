#!/usr/bin/env python3
import os

import aws_cdk as cdk

from modify_deprecated_api.modify_deprecated_api_stack import ModifyDeprecatedApiStack


app = cdk.App()
ModifyDeprecatedApiStack(app, "ModifyDeprecatedApiStack")

app.synth()

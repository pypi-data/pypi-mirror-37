Terrastack
========================

This simple project provides a way to define terrastack specifications through the Python language,
which in turn can be used to output Terraform json specifications.

The library itself does not try to create abstractions for every type of resource and attribute that
can be defined in Terraform. The goal for the API is to be as thin as possible - with the help of
using standard python objects and kwarg handling. Sacrificing type safety in order to be feature
compatible with Terraform.

Example use:
```
import terrastack as ts

stack = ts.Stack()
stack.extend(ts.Provider("aws",
    region  = "eu-west-1",
    version = "1.30.0",
))

# extend supports variable number of components
stack.extend(
    ts.Resource("aws_instance", "my-instance-1",
        ami="some-ami",
    ),
    ts.Resource("aws_instance", "my-instance-2",
        ami="some-ami",
    ),
    ts.Output("my_output", "some_value"),
)

print(stack.render_json())

# output:
        {
            "output": {
                "my_output": {
                    "value": "some_value"
                }
            },
            "provider": [
                {
                    "aws": {
                        "region": "eu-west-1",
                        "version": "1.30.0"
                    }
                }
            ],
            "resource": {
                "aws_instance": {
                    "my-instance-1": {
                        "ami": "some-ami"
                    },
                    "my-instance-2": {
                        "ami": "some-ami"
                    }
                }
            }
        }
```

from unittest import mock

from boto3 import client, resource
from moto import mock_aws

from prowler.providers.aws.services.ec2.ec2_service import EC2
from prowler.providers.aws.services.elbv2.elbv2_service import ELBv2

from tests.providers.aws.utils import (
    AWS_REGION_EU_WEST_1,
    AWS_REGION_EU_WEST_1_AZA,
    AWS_REGION_EU_WEST_1_AZB,
    set_mocked_aws_provider,
)

EXAMPLE_AMI_ID = "ami-12c6146b"


class Test_ec2_instance_not_directly_publicly_accessible_via_elbv2:
    @mock_aws
    def test_no_ec2_no_elbv2(self):
        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 0
    
    @mock_aws
    def test_no_ec2_public_elbv2_with_sg(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="sg01", Description="Test security group for load balancer"
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internet-facing",
            SecurityGroups=[security_group.id],
            Type="application",
        )["LoadBalancers"][0]


        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 0

    @mock_aws
    def test_no_ec2_with_private_elbv2_with_sg(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="sg01", Description="Test security group for load balancer"
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internal",
            SecurityGroups=[security_group.id],
            Type="application",
        )["LoadBalancers"][0]


        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 0

    @mock_aws
    def test_no_ec2_with_public_elbv2_without_sg(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)


        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internet-facing",
            Type="application",
        )["LoadBalancers"][0]


        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 0

    @mock_aws
    def test_no_ec2_with_private_elbv2_without_sg(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)


        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internal",
            Type="application",
        )["LoadBalancers"][0]


        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 0

    @mock_aws
    def test_ec2_behind_public_elbv2(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="a-security-group", Description="First One"
        )

        security_group2 = ec2.create_security_group(
            GroupName="a-security-group2", Description="Second one"
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internet-facing",
            SecurityGroups=[security_group.id],
            Type="application",
        )["LoadBalancers"][0]

        target_group = conn.create_target_group(
            Name="a-target",
            Protocol="HTTP",
            Port=80,
            VpcId=vpc.id,
            HealthCheckProtocol="HTTP",
            HealthCheckPath="/",
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType="instance",
        )["TargetGroups"][0]

        iam = client("iam", "us-west-1")
        profile_name = "fake_profile"
        iam.create_instance_profile(
            InstanceProfileName=profile_name,
        )

        ec2_client = client("ec2", region_name=AWS_REGION_EU_WEST_1)
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group2.id,
            IpPermissions=[
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                }
            ],
        )

        instance = ec2.create_instances(
            ImageId=EXAMPLE_AMI_ID,
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={"Name": profile_name},
            SecurityGroupIds=[security_group2.id],
        )[0]

        conn.register_targets(
            TargetGroupArn=target_group["TargetGroupArn"],
            Targets=[
                {"Id": instance.id},
            ],
        )

        conn.create_listener(
            LoadBalancerArn=lb["LoadBalancerArn"],
            Protocol="HTTP",
            Port=80,
            DefaultActions=[
                {"Type": "forward", "TargetGroupArn": target_group["TargetGroupArn"]}
            ],
        )

        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "FAIL"
            assert (
                result[0].status_extended
                == f"EC2 Instance {instance.id} is publicly accesible through an Internet facing Load Balancer '{lb["DNSName"]}'."
            )
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == instance.id
            assert (
                result[0].resource_arn
                == f"arn:{aws_provider.identity.partition}:ec2:{AWS_REGION_EU_WEST_1}:{aws_provider.identity.account}:instance/{instance.id}"
            )
            assert result[0].resource_tags is None
    
    @mock_aws
    def test_ec2_private_sg_behind_public_elbv2(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)
        ec2_client = client("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="a-security-group", Description="First One"
        )

        security_group2 = ec2.create_security_group(
            GroupName="a-security-group2", Description="Second one"
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internet-facing",
            SecurityGroups=[security_group.id],
            Type="application",
        )["LoadBalancers"][0]

        target_group = conn.create_target_group(
            Name="a-target",
            Protocol="HTTP",
            Port=80,
            VpcId=vpc.id,
            HealthCheckProtocol="HTTP",
            HealthCheckPath="/",
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType="instance",
        )["TargetGroups"][0]

        iam = client("iam", "us-west-1")
        profile_name = "fake_profile"
        iam.create_instance_profile(
            InstanceProfileName=profile_name,
        )

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group2.id,
            IpPermissions=[
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "203.0.113.0/24"}],
                }
            ],
        )

        instance = ec2.create_instances(
            ImageId=EXAMPLE_AMI_ID,
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={"Name": profile_name},
            SecurityGroupIds=[security_group2.id],
        )[0]

        conn.register_targets(
            TargetGroupArn=target_group["TargetGroupArn"],
            Targets=[
                {"Id": instance.id},
            ],
        )

        conn.create_listener(
            LoadBalancerArn=lb["LoadBalancerArn"],
            Protocol="HTTP",
            Port=80,
            DefaultActions=[
                {"Type": "forward", "TargetGroupArn": target_group["TargetGroupArn"]}
            ],
        )

        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"EC2 Instance {instance.id} is not publicly accesible through an Internet facing Load Balancer."
            )
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == instance.id
            assert (
                result[0].resource_arn
                == f"arn:{aws_provider.identity.partition}:ec2:{AWS_REGION_EU_WEST_1}:{aws_provider.identity.account}:instance/{instance.id}"
            )
            assert result[0].resource_tags is None

    @mock_aws
    def test_ec2_behind_private_elbv2(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)
        ec2_client = client("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="a-security-group", Description="First One"
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            SecurityGroups=[security_group.id],
            Scheme="internal",
            Type="application",
        )["LoadBalancers"][0]

        target_group = conn.create_target_group(
            Name="a-target",
            Protocol="HTTP",
            Port=80,
            VpcId=vpc.id,
            HealthCheckProtocol="HTTP",
            HealthCheckPath="/",
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType="instance",
        )["TargetGroups"][0]

        security_group_instance = ec2.create_security_group(
            GroupName="sg01_instance",
            Description="Test security group for EC2 instance",
        )

        iam = client("iam", "us-west-1")
        profile_name = "fake_profile"
        iam.create_instance_profile(
            InstanceProfileName=profile_name,
        )

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_instance.id,
            IpPermissions=[
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "203.0.113.0/24"}],
                }
            ],
        )

        instance = ec2.create_instances(
            ImageId=EXAMPLE_AMI_ID,
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={"Name": profile_name},
            SecurityGroupIds=[security_group_instance.id]
        )[0]

        conn.register_targets(
            TargetGroupArn=target_group["TargetGroupArn"],
            Targets=[
                {"Id": instance.id},
            ],
        )

        conn.create_listener(
            LoadBalancerArn=lb["LoadBalancerArn"],
            Protocol="HTTP",
            Port=80,
            DefaultActions=[
                {"Type": "forward", "TargetGroupArn": target_group["TargetGroupArn"]}
            ],
        )

        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"EC2 Instance {instance.id} is not publicly accesible through an Internet facing Load Balancer."
            )
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == instance.id
            assert (
                result[0].resource_arn
                == f"arn:{aws_provider.identity.partition}:ec2:{AWS_REGION_EU_WEST_1}:{aws_provider.identity.account}:instance/{instance.id}"
            )
            assert result[0].resource_tags is None


    @mock_aws
    def test_ec2_public_sg_behind_public_elbv2_private_sg(self):
        conn = client("elbv2", region_name=AWS_REGION_EU_WEST_1)
        ec2 = resource("ec2", region_name=AWS_REGION_EU_WEST_1)
        ec2_client = client("ec2", region_name=AWS_REGION_EU_WEST_1)

        security_group = ec2.create_security_group(
            GroupName="a-security-group", Description="First One"
        )

        security_group2 = ec2.create_security_group(
            GroupName="a-security-group2", Description="Second one"
        )

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group.id,
            IpPermissions=[
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "203.0.113.0/24"}],
                }
            ],
        )

        vpc = ec2.create_vpc(CidrBlock="172.28.7.0/24", InstanceTenancy="default")
        subnet1 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.192/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZA,
        )
        subnet2 = ec2.create_subnet(
            VpcId=vpc.id,
            CidrBlock="172.28.7.0/26",
            AvailabilityZone=AWS_REGION_EU_WEST_1_AZB,
        )

        lb = conn.create_load_balancer(
            Name="my-lb",
            Subnets=[subnet1.id, subnet2.id],
            Scheme="internet-facing",
            SecurityGroups=[security_group.id],
            Type="application",
        )["LoadBalancers"][0]

        target_group = conn.create_target_group(
            Name="a-target",
            Protocol="HTTP",
            Port=80,
            VpcId=vpc.id,
            HealthCheckProtocol="HTTP",
            HealthCheckPath="/",
            HealthCheckIntervalSeconds=30,
            HealthCheckTimeoutSeconds=5,
            HealthyThresholdCount=5,
            UnhealthyThresholdCount=2,
            TargetType="instance",
        )["TargetGroups"][0]

        iam = client("iam", "us-west-1")
        profile_name = "fake_profile"
        iam.create_instance_profile(
            InstanceProfileName=profile_name,
        )

        ec2_client.authorize_security_group_ingress(
            GroupId=security_group2.id,
            IpPermissions=[
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0"}],
                }
            ],
        )

        instance = ec2.create_instances(
            ImageId=EXAMPLE_AMI_ID,
            MinCount=1,
            MaxCount=1,
            IamInstanceProfile={"Name": profile_name},
            SecurityGroupIds=[security_group2.id],
        )[0]

        conn.register_targets(
            TargetGroupArn=target_group["TargetGroupArn"],
            Targets=[
                {"Id": instance.id},
            ],
        )

        conn.create_listener(
            LoadBalancerArn=lb["LoadBalancerArn"],
            Protocol="HTTP",
            Port=80,
            DefaultActions=[
                {"Type": "forward", "TargetGroupArn": target_group["TargetGroupArn"]}
            ],
        )

        aws_provider = set_mocked_aws_provider(
            [AWS_REGION_EU_WEST_1]
        )

        with mock.patch(
            "prowler.providers.common.provider.Provider.get_global_provider",
            return_value=aws_provider,
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.elbv2_client",
            new=ELBv2(aws_provider),
        ), mock.patch(
            "prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_client",
            new=EC2(aws_provider),
        ):
            # Test Check
            from prowler.providers.aws.services.ec2.ec2_instance_not_directly_publicly_accessible_via_elbv2.ec2_instance_not_directly_publicly_accessible_via_elbv2 import (
                ec2_instance_not_directly_publicly_accessible_via_elbv2,
            )

            check = ec2_instance_not_directly_publicly_accessible_via_elbv2()
            result = check.execute()

            assert len(result) == 1
            assert result[0].status == "PASS"
            assert (
                result[0].status_extended
                == f"EC2 Instance {instance.id} is not publicly accesible through an Internet facing Load Balancer."
            )
            assert result[0].region == AWS_REGION_EU_WEST_1
            assert result[0].resource_id == instance.id
            assert (
                result[0].resource_arn
                == f"arn:{aws_provider.identity.partition}:ec2:{AWS_REGION_EU_WEST_1}:{aws_provider.identity.account}:instance/{instance.id}"
            )
            assert result[0].resource_tags is None
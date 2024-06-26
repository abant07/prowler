from typing import Optional

from pydantic import BaseModel

from prowler.lib.logger import logger
from prowler.lib.scan_filters.scan_filters import is_resource_filtered
from prowler.providers.aws.lib.service.service import AWSService


################### ELB
class ELB(AWSService):
    def __init__(self, provider):
        # Call AWSService's __init__
        super().__init__(__class__.__name__, provider)
        self.loadbalancers = []
        self.__threading_call__(self.__describe_load_balancers__)
        self.__threading_call__(self.__describe_load_balancer_attributes__)
        self.__describe_tags__()

    def __describe_load_balancers__(self, regional_client):
        logger.info("ELB - Describing load balancers...")
        try:
            describe_elb_paginator = regional_client.get_paginator(
                "describe_load_balancers"
            )
            for page in describe_elb_paginator.paginate():
                for elb in page["LoadBalancerDescriptions"]:
                    arn = f"arn:{self.audited_partition}:elasticloadbalancing:{regional_client.region}:{self.audited_account}:loadbalancer/{elb['LoadBalancerName']}"
                    if not self.audit_resources or (
                        is_resource_filtered(arn, self.audit_resources)
                    ):
                        listeners = []
                        for listener in elb["ListenerDescriptions"]:
                            listeners.append(
                                Listener(
                                    port=listener.get("Listener", {}).get(
                                        "LoadBalancerPort", 0
                                    ),
                                    protocol=listener.get("Listener", {}).get(
                                        "Protocol", ""
                                    ),
                                    instance_port=listener.get("Listener", {}).get(
                                        "InstancePort", 0
                                    ),
                                    instance_protocol=listener.get("Listener", {}).get(
                                        "InstanceProtocol", ""
                                    ),
                                    policies=listener.get("PolicyNames", []),
                                )
                            )

                        instance_ids = []
                        for instance_attached in elb["Instances"]:
                            instance_ids.append(instance_attached["InstanceId"])

                        self.loadbalancers.append(
                            LoadBalancer(
                                name=elb["LoadBalancerName"],
                                arn=arn,
                                dns=elb["DNSName"],
                                region=regional_client.region,
                                scheme=elb["Scheme"],
                                listeners=listeners,
                                security_groups=elb["SecurityGroups"],
                                instances_ids=instance_ids,
                                public=(
                                    True
                                    if elb["Scheme"] == "internet-facing"
                                    and len(elb["SecurityGroups"]) == 1
                                    else False
                                ),
                            )
                        )

        except Exception as error:
            logger.error(
                f"{regional_client.region} -- {error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )

    def __describe_load_balancer_attributes__(self, regional_client):
        logger.info("ELB - Describing attributes...")
        try:
            for lb in self.loadbalancers:
                if lb.region == regional_client.region:
                    attributes = regional_client.describe_load_balancer_attributes(
                        LoadBalancerName=lb.name
                    )["LoadBalancerAttributes"]
                    if "AccessLog" in attributes:
                        lb.access_logs = attributes["AccessLog"]["Enabled"]

        except Exception as error:
            logger.error(
                f"{regional_client.region} -- {error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )

    def __describe_tags__(self):
        logger.info("ELB - List Tags...")
        try:
            for lb in self.loadbalancers:
                regional_client = self.regional_clients[lb.region]
                response = regional_client.describe_tags(LoadBalancerNames=[lb.name])[
                    "TagDescriptions"
                ][0]
                lb.tags = response.get("Tags")
        except Exception as error:
            logger.error(
                f"{regional_client.region} -- {error.__class__.__name__}[{error.__traceback__.tb_lineno}]: {error}"
            )


class Listener(BaseModel):
    port: int
    protocol: str
    instance_port: int
    instance_protocol: str
    policies: list[str]


class LoadBalancer(BaseModel):
    name: str
    dns: str
    arn: str
    region: str
    scheme: str
    access_logs: Optional[bool]
    listeners: list[Listener]
    tags: Optional[list] = []
    security_groups: list[str]
    instances_ids: list[str]
    public: bool

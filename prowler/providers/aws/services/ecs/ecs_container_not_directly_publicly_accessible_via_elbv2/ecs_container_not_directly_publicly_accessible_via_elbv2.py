from prowler.lib.check.models import Check, Check_Report_AWS
from prowler.providers.aws.services.ec2.ec2_client import ec2_client
from prowler.providers.aws.services.ec2.lib.security_groups import check_security_group
from prowler.providers.aws.services.ecs.ecs_client import ecs_client
from prowler.providers.aws.services.elbv2.elbv2_client import elbv2_client


class ecs_container_not_directly_publicly_accessible_via_elbv2(Check):
    def execute(self):
        findings = []

        for cluster in ecs_client.clusters.values():
            for service_arn, service in cluster.services.items():
                report = Check_Report_AWS(self.metadata())
                report.resource_arn = service_arn
                report.resource_tags = service.tags
                report.status = "PASS"
                report.status_extended = f"ECS Container '{service_arn}' is not publicly accesible through an Internet facing Load Balancer."

                for target_group in elbv2_client.target_groups:
                    if (
                        target_group.target_type == "ip"
                        and target_group.arn
                        in service.load_balancers_target_groups  # I CANT VERIFY THE IP OF THE SERVICE and (service.ipv4 in target_group.targets or service.ipv6 in target_group.targets)
                    ):
                        for lb in elbv2_client.loadbalancersv2:
                            listen_port = None
                            if lb.arn == target_group.load_balancer_arn and lb.public:
                                # Find for the container listener port
                                for listener in lb.listeners:
                                    for rule in listener.rules:
                                        for action in getattr(rule, "actions", []):
                                            if action.get("Type", "") == "forward" and (
                                                any(
                                                    tg.get("TargetGroupArn", "")
                                                    == target_group.arn
                                                    for tg in action["ForwardConfig"][
                                                        "TargetGroups"
                                                    ]
                                                )
                                                if "TargetGroups"
                                                in action.get("ForwardConfig", {})
                                                else action.get("TargetGroupArn", "")
                                                == target_group.arn
                                            ):
                                                listen_port = listener.port
                                                break
                                # Check for lb security groups in every sg
                                if listen_port != None: # i added this in case listen port is 0
                                    safe_sgs = []
                                    for sg in ec2_client.security_groups:
                                        if (
                                            sg.id
                                            in lb.security_groups
                                            # or sg.id in service.security_groups # FOR SOME REASON THIS IS NOT WORKING, THE SG IS SAFE BUT STILL BEING ACCESIBLE
                                        ):
                                            for rule in sg.ingress_rules:
                                                if check_security_group(
                                                    ingress_rule=rule,
                                                    protocol=rule.get(
                                                        "IpProtocol", "tcp"
                                                    ),
                                                    ports=[listen_port],
                                                    any_address=True,
                                                ):
                                                    safe_sgs.append(False)
                                                    break
                                                #i changed this else statment and move it inside the for loop
                                                else:
                                                    safe_sgs.append(True)
                                    # If there is not any security group safe, the service is publicly accessible
                                    if len(safe_sgs) == 0: # i added this condition in the case of default sgs are restricting access
                                        report.status = "FAIL"
                                        report.status_extended = f"ECS Container '{service_arn}' is publicly accesible through an Internet facing Load Balancer '{lb.name}'."
                                    if not any(safe_sgs):
                                        report.status = "FAIL"
                                        report.status_extended = f"ECS Container '{service_arn}' is publicly accesible through an Internet facing Load Balancer '{lb.name}'."

                findings.append(report)

        return findings

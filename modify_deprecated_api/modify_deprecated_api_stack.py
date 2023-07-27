from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_rds as rds,
)
from constructs import Construct

class ModifyDeprecatedApiStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(self, "MyVPC",
            max_azs=2
        )

        # RDSのセキュリティグループの作成
        rds_security_group = ec2.SecurityGroup(
            self, 
            "RdsSecurityGroup",
            vpc=vpc,
            description="Allow Lambda access to RDS"
        )
        
        # # RDS Instanceの設定値を定義
        # instance_props = rds.InstanceProps(
        #     vpc=vpc,
        #     allow_major_version_upgrade=False,
        #     auto_minor_version_upgrade=True,
        #     instance_type=ec2.InstanceType.of(
        #         ec2.InstanceClass.BURSTABLE3,
        #         ec2.InstanceSize.MEDIUM,
        #     ),
        #     publicly_accessible=False,
        #     security_groups=[rds_security_group],
        # )
        
        # # DB Clusterを作成
        
        # db_cluster = rds.DatabaseCluster(
        #     self,
        #     'AuroraDatabaseCluster',
        #     engine=rds.DatabaseClusterEngine.aurora_postgres(
        #         version=rds.AuroraPostgresEngineVersion.VER_14_5
        #     ),
        #     instance_props=instance_props,
        #     cluster_identifier='aurora-postgres-cluster',
        #     deletion_protection=True,
        #     instances=1,
        #     storage_encrypted=True,
        # )
        
        cluster_name = 'aurora-postgres-cluster'
        # DB Cluster作成
        db_cluster = rds.DatabaseCluster(
            self,
            'AuroraDatabaseCluster',
            engine=rds.DatabaseClusterEngine.aurora_postgres(
                version=rds.AuroraPostgresEngineVersion.VER_14_5
            ),
            cluster_identifier=cluster_name,
            deletion_protection=True,
            security_groups=[rds_security_group],
            storage_encrypted=True,
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(
                subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
            ),
            writer=rds.ClusterInstance.provisioned(
                'Instance1',   # Writer instance must be named 'Instance1'.
                instance_type=ec2.InstanceType.of(
                    ec2.InstanceClass.BURSTABLE3,
                    ec2.InstanceSize.MEDIUM,
                ),
                is_from_legacy_instance_props=True,    # For migrating existing clusters.
                allow_major_version_upgrade=False,
                auto_minor_version_upgrade=True,
                instance_identifier=f'{cluster_name}instance1',    # 指定しないとリソース作り直しとなる
                publicly_accessible=False,
            )
        )



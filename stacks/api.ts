import { StackContext, use } from "sst/constructs";
import * as apprunner from "aws-cdk-lib/aws-apprunner";
import { IAM } from "./iam";
import {
  AWS_ACCOUNT,
  AWS_REGION,
  INTERNAL_CONFIGURATION_ARN,
  INTERNAL_VPC_CONNECTOR_ARN,
  INTERNAL_VPC_ENDPOINT_ARN,
  INTERNAL_VPC_ID,
  SECRET_ARN_PROD,
  SECRET_ARN_UAT,
} from "./constants";

export function API({ app, stack }: StackContext) {
  const { SampleGabBEAppRunnerInstanceRoleArn } = use(IAM);
  const imageIdentifier = `${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com/sample-gab-be:${stack.stage}`;
  const accessRoleArn = `arn:aws:iam::${AWS_ACCOUNT}:role/service-role/AppRunnerECRAccessRole`;
  const serviceName = `sample-gab-be-${stack.stage}`;
  const secret = stack.stage === "prod" ? SECRET_ARN_PROD : SECRET_ARN_UAT;

  const api = new apprunner.CfnService(stack, "sample-gab-be", {
    sourceConfiguration: {
      authenticationConfiguration: {
        accessRoleArn,
      },
      autoDeploymentsEnabled: true,
      imageRepository: {
        imageIdentifier,
        imageRepositoryType: "ECR",
        imageConfiguration: {
          port: "5000",
          runtimeEnvironmentSecrets: [
            {
              name: "DB_URL",
              value: `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${secret}:db_url::`,
            },
            {
              name: "AX_SO_API",
              value: `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${secret}:AX_SO_API::`,
            },
            {
              name: "AWS_SECRET_ACCESS_KEY",
              value: `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${secret}:AWS_SECRET_ACCESS_KEY::`,
            },
            {
              name: "AWS_ACCESS_KEY_ID",
              value: `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${secret}:AWS_ACCESS_KEY_ID::`,
            },
          ],
          runtimeEnvironmentVariables: [
            {
              name: "AWS_DEFAULT_REGION",
              value: `${AWS_REGION}`,
            },
          ],
        },
      },
    },
    autoScalingConfigurationArn: INTERNAL_CONFIGURATION_ARN,
    instanceConfiguration: {
      cpu: "1 vCPU",
      memory: "2 GB",
      instanceRoleArn: SampleGabBEAppRunnerInstanceRoleArn,
    },
    networkConfiguration: {
      egressConfiguration: {
        egressType: "VPC",
        vpcConnectorArn: INTERNAL_VPC_CONNECTOR_ARN,
      },
      ingressConfiguration: {
        isPubliclyAccessible: false,
      },
    },
    serviceName,
  });

  new apprunner.CfnVpcIngressConnection(stack, "api-vpc-ingress-connection", {
    ingressVpcConfiguration: {
      vpcEndpointId: INTERNAL_VPC_ENDPOINT_ARN,
      vpcId: INTERNAL_VPC_ID,
    },
    serviceArn: api.attrServiceArn,
  });

  stack.addOutputs({
    id: api.attrServiceId,
    name: api.serviceName,
    arn: api.attrServiceArn,
  });
}

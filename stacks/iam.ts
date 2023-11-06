import { StackContext } from "sst/constructs";
import * as iam from "aws-cdk-lib/aws-iam";
import {
  AWS_ACCOUNT,
  AWS_REGION,
  SECRET_ARN_PROD,
  SECRET_ARN_UAT,
} from "./constants";

export function IAM({ stack }: StackContext) {
  let instanceRole;

  if (stack.stage === "develop") {
    instanceRole = new iam.Role(
      stack,
      "SampleGabBEDevelopAppRunnerInstanceRole",
      {
        assumedBy: new iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
        description:
          "Role assumed for Sample Gab Backend Develop App Runner Services",
        roleName: "SampleGabBEDevelopAppRunnerInstanceRole",
        inlinePolicies: {
          SecretManagerPolicy: new iam.PolicyDocument({
            assignSids: true,
            statements: [
              new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                actions: ["secretsmanager:GetSecretValue"],
                resources: [
                  `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${SECRET_ARN_UAT}`,
                ],
              }),
            ],
          }),
        },
      }
    );
  } else {
    instanceRole = new iam.Role(
      stack,
      "SampleGabBEProdAppRunnerInstanceRole",
      {
        assumedBy: new iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
        description:
          "Role assumed for Sample Gab Backend Prod App Runner Services",
        roleName: "SampleGabBEProdAppRunnerInstanceRole",
        inlinePolicies: {
          SecretManagerPolicy: new iam.PolicyDocument({
            assignSids: true,
            statements: [
              new iam.PolicyStatement({
                effect: iam.Effect.ALLOW,
                actions: ["secretsmanager:GetSecretValue"],
                resources: [
                  `arn:aws:secretsmanager:${AWS_REGION}:${AWS_ACCOUNT}:secret:${SECRET_ARN_PROD}`,
                ],
              }),
            ],
          }),
        },
      }
    );
  }

  return {
    SampleGabBEAppRunnerInstanceRoleArn: instanceRole.roleArn,
  };
}

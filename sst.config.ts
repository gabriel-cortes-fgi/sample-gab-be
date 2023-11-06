import { SSTConfig } from "sst";
import { IAM } from "./stacks/iam";
import { API } from "./stacks/api";
import { AWS_REGION } from "./stacks/constants";

export default {
  config(_input) {
    return {
      name: "sample-gab-be",
      region: AWS_REGION,
    };
  },
  stacks(app) {
    app.stack(IAM).stack(API);
  },
} satisfies SSTConfig;

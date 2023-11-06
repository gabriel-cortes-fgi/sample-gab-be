import { SSTConfig } from "sst";
import { AWS_REGION } from "./stacks/constants";
import { IAM } from "./stacks/iam";
import { API } from "./stacks/api";

export default {
  config(_input) {
    return {
      name: "sample-gab-be",
      region: AWS_REGION,
    };
  },
  stacks(app) {
    app.stack(function Site({ stack }) {
      app.stack(IAM).stack(API);
    });
  },
} satisfies SSTConfig;

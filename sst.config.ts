import { SSTConfig } from "sst";
import { IAM } from "./stacks/iam";
import { API } from "./stacks/api";

export default {
  config(_input) {
    return {
      name: "sample-gab-be",
      region: "us-east-1",
    };
  },
  stacks(app) {
    app.stack(IAM).stack(API);
  },
} satisfies SSTConfig;

#!/usr/bin/env python3
import os

import aws_cdk as cdk

from rtbf_news_scraper_aws.rtbf_news_scraper_aws_stack import RtbfNewsScraperAwsStack


app = cdk.App()
RtbfNewsScraperAwsStack(app, "RtbfNewsScraperAwsStack")
app.synth()


def main():
    app = cdk.App()
    RtbfNewsScraperAwsStack(app, "RtbfNewsScraperAwsStack")
    app.synth()

if __name__ == "__main__":
    main()
# Serverless Global Resume Application with Real-Time Visitor Alerts

## Project Overview
A highly available, fault-tolerant, and cost-optimized serverless web application hosting a professional portfolio/resume. The architecture leverages AWS edge routing for low-latency global delivery and utilizes an event-driven backend to securely track and notify the administrator of visitor metrics in real time.

## Architecture Breakdown & Component Strategy

*   **Content Delivery Network (CDN):** **Amazon CloudFront** is deployed as the global edge routing tier. This ensures microsecond latency for global visitors via Edge Locations and reduces direct read requests to the origin storage.
*   **Object Storage (Origin):** **Amazon S3** hosts the static frontend assets (HTML5, CSS3, JavaScript). Public access to the bucket is blocked entirely, enforcing secure access exclusively via CloudFront Origin Access Control (OAC).
*   **API Edge Ingestion:** **Amazon API Gateway** exposes a secure, public HTTPS endpoint that triggers the asynchronous backend metrics pipeline whenever the frontend loads.
*   **Serverless Compute:** **AWS Lambda** executes the backend logic natively without server management overhead. It intercepts the API payload, increments the metric, and interfaces with the notification layer.
*   **Event Notification:** **Amazon SNS (Simple Notification Service)** serves as the pub/sub notification broker, securely routing structured email alerts to the administrator via SMTP endpoints (Gmail).

## Key Architectural Decisions & SAA-C03 Alignment
*   **High Availability:** By relying entirely on Amazon CloudFront and Amazon S3, the application achieves static 99.99% availability globally without maintaining elastic server infrastructure (EC2).
*   **Security Posture:** Enforced Principle of Least Privilege by configuring restrictive IAM execution roles for the Lambda function and establishing strict S3 bucket policies to block public traffic.
*   **Cost Optimization:** The stack operates entirely within the AWS Free Tier baseline, eliminating idle computing costs by utilizing an on-demand billing structure.
